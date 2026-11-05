# Onto Skills maintenance

This repository distributes skill assets, knowledge and documentation-only packs.
Do not add a CLI product, installer, registry, resolver, UI or knowledge runtime.
Do not copy nebula-gql-skills instructions, references, scripts or grammar.
Ontology design is database-neutral; route verified GQL generation externally.

Every skills/<category>/<name>/ directory is directly installable and self-contained.
Keep all required resources inside it. Use relative links, unique standard names,
explicit source provenance and a bundled license. Do not require another skill.
Keep finance/scenario knowledge out of generic core methods.

When local planning files exist, resolve the selected plan before continuing.
Local agent worklogs are intentionally excluded from published source.
Do not overwrite unrelated edits. Do not commit, push, publish or deploy unless asked.

For asset changes run `python3 scripts/validate.py` and
`python3 -m unittest discover -s tests -v` with requirements-dev.txt installed.
Native Codex checks are opt-in: `python3 tests/compatibility/codex_probe.py`.
Static checks do not prove ontology correctness, CC-Switch GUI or macOS behavior.
