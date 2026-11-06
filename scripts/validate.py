"""Development-only asset checks. Never installs, updates or executes a skill."""
import json
from html import unescape
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
import re
import sys
from urllib.parse import unquote, urlsplit

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import FormatError

ROOT = Path(__file__).resolve().parents[1]
NAME = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
LINK = re.compile(r'''!?\[[^\]]*\]\(\s*(?:<([^>]+)>|([^\s)]+))(?:\s+(?:"[^"]*"|'[^']*'))?\s*\)''')
LINK_DEFINITION = re.compile(r'^\s{0,3}\[[^\]]+\]:\s*(?:<([^>]+)>|(\S+))', re.M)
RESOURCE = re.compile(r'`((?:references|assets|examples|scripts)/[^`\s]+)`')


class UniqueLoader(yaml.SafeLoader):
    """Reject ambiguous duplicate mapping keys rather than silently accepting the last."""


def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise yaml.constructor.ConstructorError(None, None, 'duplicate key', key_node.start_mark)
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


class HtmlResources(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        self.links.extend(value for name, value in attrs if name in ('href', 'src') and value)


def metadata(path):
    text = path.read_text(encoding='utf-8')
    match = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)', text, re.S)
    if not match:
        raise ValueError('missing YAML frontmatter')
    return yaml.load(match[1], Loader=UniqueLoader), text[match.end():]


def resource_errors(path, root, code_resources=True):
    errors = []
    text = path.read_text(encoding='utf-8')
    # Both Markdown links and executable/reference examples must close inside the package.
    html = HtmlResources()
    html.feed(text)
    links = [a or b for a, b in LINK.findall(text) + LINK_DEFINITION.findall(text)]
    links += html.links + (RESOURCE.findall(text) if code_resources else [])
    for raw in links:
        raw = unquote(unescape(raw))
        if re.match(r'^[A-Za-z]:[\\/]', raw):
            errors.append(f'{path}: absolute resource {raw}')
            continue
        url = urlsplit(raw)
        if url.scheme in ('https', 'http', 'mailto'):
            continue  # Optional source citations, not required online knowledge services.
        if url.scheme or url.netloc:
            errors.append(f'{path}: unsupported resource URI {raw}')
            continue
        target = url.path
        if not target:
            continue
        if PurePosixPath(target).is_absolute() or '\\' in target:
            errors.append(f'{path}: absolute/nonportable resource {raw}')
            continue
        resolved = (path.parent / target).resolve()
        if not resolved.is_relative_to(root.resolve()):
            errors.append(f'{path}: resource escapes package: {raw}')
        elif not resolved.exists():
            errors.append(f'{path}: missing resource: {raw}')
    return errors


def validate_skill(directory):
    directory = Path(directory)
    if directory.is_symlink():
        return [f'{directory}: source package root must not be a symlink']
    errors = []
    entry = directory / 'SKILL.md'
    if not entry.is_file():
        return [f'{entry}: missing SKILL.md']
    try:
        meta, body = metadata(entry)
        if not isinstance(meta, dict):
            return [f'{entry}: YAML metadata must be a mapping']
        name = meta.get('name')
        if not isinstance(name, str) or len(name) > 64 or not NAME.fullmatch(name) or name != directory.name:
            errors.append(f'{entry}: invalid/mismatched name')
        desc = meta.get('description')
        if not isinstance(desc, str) or not 1 <= len(desc.strip()) <= 1024:
            errors.append(f'{entry}: invalid description')
        if not body.strip():
            errors.append(f'{entry}: empty workflow')
    except (ValueError, yaml.YAMLError, TypeError) as exc:
        return [f'{entry}: YAML/frontmatter error: {exc}']
    for path in directory.rglob('*'):
        if path.is_symlink():
            errors.append(f'{path}: symlinks are not distributable resources')
        elif path.suffix == '.md' and path.is_file():
            errors.extend(resource_errors(path, directory))
    return errors


def validate_model(model, ready=False):
    schema = json.loads((ROOT / 'schemas/graph-model.schema.json').read_text())
    errors = [f'model/{"/".join(map(str, e.absolute_path))}: {e.message}'
              for e in Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(model)]
    if errors:
        return errors

    def unique(items, field, context):
        values = [item[field] for item in items]
        if len(values) != len(set(values)):
            errors.append(f'{context}: duplicate {field}')
        return set(values)

    source_ids = unique(model['source_catalog'], 'id', 'sources')
    nodes = unique(model['node_types'], 'name', 'nodes')
    edges = unique(model['edge_types'], 'name', 'edges')
    if nodes & edges:
        errors.append('model: node/edge names collide')
    constraint_ids = unique(model['constraints'], 'id', 'constraints')
    unique(model['mappings'], 'id', 'mappings')
    subjects = {'model'} | {'node:' + n for n in nodes} | {'edge:' + n for n in edges}

    def provenance(item, context):
        for source in item['source_ids']:
            if source not in source_ids:
                errors.append(f'{context}: unknown source {source}')

    for kind in ('node_types', 'edge_types'):
        for item in model[kind]:
            ctx = f'{kind}/{item["name"]}'
            provenance(item, ctx)
            names = unique(item['properties'], 'name', ctx + '/properties')
            props = {p['name']: p for p in item['properties']}
            subjects.update('property:' + item['name'] + '.' + n for n in names)
            if len(item['primary_key']) != len(set(item['primary_key'])):
                errors.append(f'{ctx}: duplicate primary key component')
            for key in item['primary_key']:
                if key not in props:
                    errors.append(f'{ctx}: unknown primary key {key}')
                elif props[key]['nullable'] or props[key]['multivalued'] or props[key]['logical_type'] == 'json':
                    errors.append(f'{ctx}: identity {key} must be nonnull scalar')
            for prop in props.values():
                provenance(prop, ctx + '/' + prop['name'])
            if kind == 'edge_types':
                if item['from'] not in nodes or item['to'] not in nodes:
                    errors.append(f'{ctx}: unknown endpoint')
                temporal = item['temporal']
                required = {'none': [], 'event_time': ['start'], 'valid_time': ['start', 'end'],
                            'bitemporal': ['start', 'end', 'observed_at']}[temporal['kind']]
                for field in required:
                    key = temporal[field]
                    if key is None:
                        errors.append(f'{ctx}: required temporal {field} is missing')
                for field in ('start', 'end', 'observed_at'):
                    key = temporal[field]
                    if key is None:
                        continue
                    if key not in props or props[key]['logical_type'] != 'datetime' or props[key]['multivalued']:
                        errors.append(f'{ctx}: invalid temporal {field} field {key}')
                    elif field in ('start', 'observed_at') and props[key]['nullable']:
                        errors.append(f'{ctx}: temporal {field} must be nonnull')
                if temporal['end'] is not None and temporal['start'] == temporal['end']:
                    errors.append(f'{ctx}: temporal start and end must be distinct')
                if temporal['kind'] == 'none' and any(temporal[f] is not None for f in ('start','end','observed_at')):
                    errors.append(f'{ctx}: nontemporal edge declares temporal fields')
    for c in model['constraints']:
        provenance(c, 'constraint/' + c['id'])
        if c['subject'] not in subjects:
            errors.append(f'constraint/{c["id"]}: unknown subject')
        if ready and c['enforcement'] == 'unresolved':
            errors.append(f'constraint/{c["id"]}: unresolved enforcement blocks handoff')
    for m in model['mappings']:
        if m['source_id'] not in source_ids:
            errors.append(f'mapping/{m["id"]}: unknown source')
        if m['target'] is not None and m['target'] not in subjects:
            errors.append(f'mapping/{m["id"]}: unknown target')
        if m['status'] == 'unmapped' and m['target'] is not None:
            errors.append(f'mapping/{m["id"]}: unmapped term has target')
        if m['status'] != 'unmapped' and m['target'] is None:
            errors.append(f'mapping/{m["id"]}: mapped term requires target')
        if set(m['constraint_ids']) - constraint_ids:
            errors.append(f'mapping/{m["id"]}: unknown constraint reference')
    if ready and model['unresolved']:
        errors.append('model: unresolved design decisions block handoff')
    if ready and model['target']['database'] != 'unspecified' and model['target']['version'] == 'unspecified':
        errors.append('model: selected target requires an explicit version for handoff')
    return errors


def validate_knowledge(asset, catalog):
    errors = []
    schema = json.loads((ROOT / 'schemas/graph-model.schema.json').read_text())
    source_schema = schema['$defs']['source']
    if not isinstance(catalog, dict) or not isinstance(catalog.get('sources'), list):
        return ['knowledge: source catalog must contain a sources list']
    ids = []
    for source in catalog['sources']:
        failures = list(Draft202012Validator(source_schema, format_checker=FormatChecker()).iter_errors(source))
        errors.extend('knowledge source: ' + e.message for e in failures)
        if not failures:
            ids.append(source['id'])
    if len(ids) != len(set(ids)):
        errors.append('knowledge: duplicate source ID')
    if not isinstance(asset, dict):
        return errors + ['knowledge asset must be an object']
    for field in ('id', 'name', 'version', 'license', 'scope', 'authority'):
        if not isinstance(asset.get(field), str) or not asset[field].strip():
            errors.append(f'knowledge: missing/invalid {field}')
    try:
        FormatChecker().check(asset.get('updated_at'), 'date')
        if not isinstance(asset.get('updated_at'), str):
            raise ValueError('date must be a string')
    except (ValueError, TypeError, FormatError) as exc:
        errors.append(f'knowledge: invalid updated_at: {exc}')

    sources = {s['id']: s for s in catalog['sources']
               if isinstance(s, dict) and isinstance(s.get('id'), str)}
    # Only the selected catalogue itself is exempt from record grounding.
    is_catalog = asset == catalog
    if not is_catalog and asset.get('standards_policy') != 'standards-first-v1':
        errors.append('knowledge: missing/invalid standards_policy')

    def grounding(record):
        ctx = f'knowledge/{record.get("id")}'
        basis = record.get('standard_basis', [])
        gap = record.get('standard_gap')
        if not isinstance(basis, list):
            errors.append(f'{ctx}: standard_basis must be a list')
            basis = []
        if gap is not None and (not isinstance(gap, str) or not gap.strip()):
            errors.append(f'{ctx}: standard_gap must explain the missing or local authority')
        if not basis and not (isinstance(gap, str) and gap.strip()):
            errors.append(f'{ctx}: standard_basis or explicit standard_gap required')
        direct_support = False
        for citation in basis:
            if not isinstance(citation, dict):
                errors.append(f'{ctx}: standard_basis citation must be an object')
                continue
            ref = citation.get('source_id')
            source = sources.get(ref) if isinstance(ref, str) else None
            refs = record.get('source_ids')
            if source is None or not isinstance(refs, list) or ref not in refs:
                errors.append(f'{ctx}: standard_basis source must occur in record source_ids')
                continue
            if any(not isinstance(citation.get(k), str) or not citation[k].strip()
                   for k in ('locator', 'scope')):
                errors.append(f'{ctx}: standard_basis requires locator and bounded scope')
            relation = citation.get('relation')
            if relation not in ('supports', 'background'):
                errors.append(f'{ctx}: invalid standard_basis relation')
            if source.get('kind') not in ('official-standard', 'industry-common'):
                errors.append(f'{ctx}: standard_basis requires a publisher standard or sourced background')
            if relation == 'supports':
                if source.get('kind') != 'official-standard':
                    errors.append(f'{ctx}: direct standard support requires official-standard source')
                else:
                    direct_support = True
        if record.get('classification') == 'official-standard' and not direct_support:
            errors.append(f'{ctx}: official-standard record requires direct standard support')
        status = record.get('standard_status')
        if status not in ('standard-backed', 'nonstandard-modeling'):
            errors.append(f'{ctx}: missing/invalid standard_status')
        if status == 'standard-backed' and not direct_support:
            errors.append(f'{ctx}: standard-backed status requires direct bounded support')
        if status == 'nonstandard-modeling' and not (isinstance(gap, str) and gap.strip()):
            errors.append(f'{ctx}: nonstandard-modeling status requires an explicit reason')

    def visit(value):
        if isinstance(value, dict):
            # Only source entries in the selected catalogue use kind as an
            # exemption. A knowledge record cannot opt out by adding that key.
            if 'id' in value and (not is_catalog or 'kind' not in value):
                if value.get('classification') not in {'official-standard', 'industry-common', 'project-curated', 'model-inference'}:
                    errors.append(f'knowledge/{value.get("id")}: missing/invalid classification')
                refs = value.get('source_ids')
                if not isinstance(refs, list) or not refs or any(not isinstance(x, str) or x not in ids for x in refs):
                    errors.append(f'knowledge/{value.get("id")}: missing/unknown source_ids')
                if not is_catalog:
                    grounding(value)
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)
    visit(asset)
    return errors


def knowledge_catalog(path, root):
    """Find a development source index in the asset's closest knowledge scope."""
    knowledge = (Path(root) / 'knowledge').absolute()
    path = Path(path).absolute()
    if not path.resolve().is_relative_to(knowledge.resolve()):
        raise ValueError('knowledge asset escapes knowledge tree')
    for parent in path.parents:
        if not parent.is_relative_to(knowledge):
            break
        candidate = parent / 'standards/sources.json'
        if candidate.exists() or candidate.is_symlink():
            if candidate.is_symlink() or not candidate.resolve().is_relative_to(knowledge.resolve()):
                raise ValueError('source catalog symlink or path escapes knowledge tree')
            if not candidate.is_file():
                raise ValueError('source catalog must be a file')
            return candidate
    raise ValueError('missing knowledge source catalog in asset scope')


def validate_repository(root):
    root = Path(root)
    errors = []
    skills = sorted((root / 'skills').glob('*/*/SKILL.md'))
    if not skills:
        errors.append('skills: empty inventory')
    names = []
    for entry in skills:
        if entry.parent.parent.is_symlink():
            errors.append(f'{entry.parent.parent}: source category must not be a symlink')
        errors.extend(validate_skill(entry.parent))
        names.append(entry.parent.name)
    if len(names) != len(set(names)):
        errors.append('skills: duplicate installed names')
    for path in root.rglob('*.md'):
        if '.git' not in path.parts:
            errors.extend(resource_errors(path, root, code_resources=False))
    for path in root.rglob('*graph-model.json'):
        try:
            errors.extend(f'{path}: {e}' for e in validate_model(json.loads(path.read_text())))
        except (ValueError, OSError) as exc:
            errors.append(f'{path}: {exc}')
    for path in (root / 'knowledge').rglob('*.json'):
        try:
            asset = json.loads(path.read_text())
            catalog = json.loads(knowledge_catalog(path, root).read_text())
            errors.extend(f'{path}: {e}' for e in validate_knowledge(asset, catalog))
        except (ValueError, OSError) as exc:
            errors.append(f'{path}: {exc}')
    # A controlled, explicit source-to-package snapshot map, not a registry or dependency resolver.
    snapshots = root / 'tests/content-validation/snapshots.json'
    if snapshots.is_file():
        for record in json.loads(snapshots.read_text()):
            original = root / record['source']
            for dest in record['copies']:
                if not (root / dest).is_file() or (root / dest).read_bytes() != original.read_bytes():
                    errors.append(f'{dest}: stale standalone knowledge snapshot')
    return errors


if __name__ == '__main__':
    failures = validate_repository(ROOT)
    if failures:
        print('\n'.join(failures))
        sys.exit(1)
    print('PASS: skills, resource closure, knowledge provenance, snapshots and graph models')
