# Onto Skills Implementation Plan

**Goal:** Complete the supplied phase-one skills asset repository and evidence-backed compatibility report.

**Architecture:** Self-contained skill directories, centrally curated knowledge, documentation-only packs, neutral JSON model handoff. Development validators have no installation or service functions.

**Tech Stack:** Markdown, JSON, JSON Schema, Python 3.10+, PyYAML and jsonschema for development checks only.

**Spec:** [design.md](design.md) and the user's complete development brief; this is the initial implementation record. Current acceptance is in [acceptance.md](acceptance.md); local agent phase logs are not published.

## Global Constraints

- No CLI product, installer, registry, resolver, runtime, UI or GQL grammar copy.
- Every skill works from its own directory, offline for supplied-input tasks.
- Seven core, four finance and two scenario skills; future industries are roadmap only.
- Explicitly distinguish official sources, common knowledge, project curation and model inference.
- No commits, pushes or publication without explicit user authorization; do not alter existing user skill installations.

## Review Focus

- Missing optional GQL skills must preserve model output and give installation guidance.
- Traversal/symlink/absolute references must fail isolation checks.
- OWL inference must not become a falsely database-enforced validation constraint.
- Shared identifiers and temporal overlap must not become automatic identity or fraud conclusions.
- Weak/static compatibility evidence must not be reported as native GUI/macOS proof.

### Task 1: Contracts and asset gates

Files: docs/*-specification.md, schemas/graph-model.schema.json, scripts/validate.py, tests/*.

- [x] Write focused tests for malformed metadata, resource escape and broken model identity/endpoints/constraint traceability; observe failures before implementation.
- [x] Implement `validate_skill(Path) -> list[str]`, `validate_model(dict) -> list[str]`, `validate_repository(Path) -> list[str]`; use real YAML/JSON Schema parsing and semantic cross-reference checks.
- [x] Run `python3 -m unittest discover -s tests -v` and `python3 scripts/validate.py`; all errors have paths and reasons.

### Task 2: Core assets

Files: skills/core/{ontology-modeling,industry-knowledge-discovery,entity-relationship-modeling,property-graph-mapping,ontology-validation,ontology-documentation,ontology-evolution}/.

- [x] Author specific invocation descriptions, inputs, executable workflows and output contracts with skill-local references/examples.
- [x] Check independent copies and model templates; inspect semantic quality beyond headings.

### Task 3: Financial knowledge and assets

Files: knowledge/finance/*; skills/finance/{finance-domain-knowledge,fibo-ontology,banking-business-model,credit-risk-knowledge}/.

- [x] Capture official FIBO/OWL and banking sources; write original licensed summaries and typed provenance.
- [x] Author independent finance workflows and examples; separate standards and design advice.
- [x] Validate source IDs, provenance fields and skill-local snapshot equality.

### Task 4: Scenarios and pack

Files: skills/scenarios/{multi-lending-detection,fraud-network-modeling}/; packs/finance-ontology/; examples/finance/.

- [x] Model event identity, valid and observed time, deduplication, identity confidence and evidence-backed risk hypotheses.
- [x] Supply business description, data schema, concepts, FIBO alignment, full model, loss report, GQL handoff and semantic acceptance procedure.
- [x] Demonstrate bottom-up, top-down and merged output without requiring GQL for design.

### Task 5: Compatibility and delivery

Files: tests/compatibility/*, docs/compatibility.md, README.md, CONTRIBUTING.md, CHANGELOG.md, LICENSE, .github/workflows/validate.yml.

- [x] Query actual Codex skills/list from isolated native runtime; copy one/all skills and read resources without repository dependence.
- [x] Inspect CC-Switch discovery/install/update/sync implementation and record exact unverified native GUI/macOS items.
- [x] Run all validators and negative tests, obtain fresh review, fix meaningful findings and audit all brief requirements.

The initial implementation ran inline in the isolated project workspace. Subsequent source publication requires explicit user authorization and verification of the published commit.
