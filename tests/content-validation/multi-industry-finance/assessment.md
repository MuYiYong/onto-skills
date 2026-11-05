# Independent finance package forward review

Reviewed frozen copies of exactly two standalone packages in `/tmp/onto-finance-independent-review.C7m9qe`: `financial-regulatory-reporting` and `related-party-transaction-modeling`. I read their entrypoints, local domain/source/method/specification references and example graph-model structure. I did not read central fixtures, repository tests, parent conclusions, other skills, or either package's existing input/acceptance examples. No network, production, database, external agents or source edits were used. Inputs were authored afresh from the assigned task; exact scheduling instants and yuan units are explicitly labeled synthetic assumptions.

## Task A: reporting result

| Run | Selected source versions | Sum | Submission acceptance |
| --- | --- | --- | --- |
| known_at 2026-11-01 | SYS/K1/v1=80; SYS/K2/v1=20 | 100.00 CNY, unit yuan | S2 has local check passed + transport received; current business-accepted submission remains S1 |
| known_at 2026-11-03 | SYS/K1/v2=90; SYS/K2/v1=20 | 110.00 CNY, unit yuan | New run and hypothetical S3 draft do not change accepted state |
| Nov3, selected K1/v2 has no unit | Same source versions, but unit unknown | blocked; value=null, no partial total | No publishable replacement fact |

Exact K2/v1 replay is ignored; there are three unique source versions and two selected source business records. Version labels are not sorted. K1/v2 is not known on Nov1 although its business effective time is Oct31. Each run retains business instant, knowledge cutoff, input snapshot hash, per-version contribution and fact/context/submission keys. C1, the individual scope, DEMO-R1 synthetic definition version, instant 2026-10-31, timezone, dimensions, CNY and yuan remain explicit.

The supplied prior acceptance establishes current submission ID S1, but its amount/payload/lineage were not supplied. I therefore leave the current accepted amount unknown rather than substituting the newly calculated S2 value. SUPERSEDES, transport receipt and local validation do not imply S2 business acceptance. No regulator template ID, mandatory threshold, formula, deadline or submission channel was invented.

Actual artifacts: `task-a-input.json`, `task-a-missing-unit-input.json`, `task-a-results.json`, `task-a-graph-model.json`, `task-a-evidence-graph.json`.

## Task B: related-party result

Explicit confirmed assessments CTRL-R-BANK and CTRL-R-VENDOR are effective from Jan1, observed Jan2, ongoing by an explicit null-end convention, supported by EV-R-BANK and EV-R-VENDOR. For tradeOct31 they establish a bounded common-controller candidate path BANK ← R → VENDOR at all three knowledge cutoffs. That is a candidate under `demonstration-confirmed-control-only`, not a complete legal determination. BANK and OTHER remain distinct and `not_demonstrated`: shared contact is neither confirmed control evidence nor identity equivalence.

| known_at | Selected event versions | Current executed candidate events | Candidate occurrence amount | Explicit internal consolidated disclosure display | Bank regulatory view |
| --- | --- | --- | --- | --- | --- |
| Nov1 | E1/v1=40; E2/v1=30 | E1, E2 | 70.00 CNY/yuan | 0.00 under supplied {BANK,VENDOR} scope | retains 70.00; no automatic accounting-scope exemption |
| Nov3 | E1/v2=45; E2/v1=30 | E1, E2 | 75.00 CNY/yuan | 0.00 | retains 75.00 |
| Nov5 | E1/v3 reversed, source amount45; E2/v1=30 | E2 | 30.00 CNY/yuan | 0.00 | retains 30.00 |

E2 is distinct despite identical endpoints. E1 versions never sum together. Reversed v3 is the current state of the same E1 event; it contributes zero to this executed-occurrence view, with v1/v2/v3 and correction references retained. It does not become a new negative payment, delete history, or erase the BANK/VENDOR candidate relationship.

The financial-disclosure adjustment is shown separately with the raw candidate relation and underlying amounts retained. Its zero displayed amount follows the package's bounded synthetic scope rule, not independently verified accounting/legal requirements. The bank regulatory view does not inherit that exclusion. Ownership percentages, including 60%×60%, are not a universal control test: the unsupported claim produces no confirmed control assessment. Review remains pending; transaction classification, thresholds, procedures and legal duties remain unresolved.

Actual artifacts: `task-b-input.json`, `task-b-results.json`, `task-b-graph-model.json`, `task-b-evidence-graph.json`.

## Concrete findings and consumer choices

1. **F1 / medium: sample related-party graph cannot retain the amount unit required by its own method.** `related-party-transaction-modeling/references/method.md:13` requires original currency and amount unit; `examples/graph-model.json:348` Transaction has amount/currency/status but no unit property. A consumer following only the sample model cannot preserve the supplied yuan unit or distinguish yuan from thousand-yuan transactions. My output model adds `Transaction.unit` explicitly as a consumer adaptation, attributed to project modeling inference. The reviewed package remains unchanged.
2. **F2 / medium: explicit correction/reversal linkage is promised but absent from the sample graph.** The same method line13 requires reversal/cancellation to point back to the original event, but Transaction has no correction/reversal reference and the supplied edge inventory has no corresponding edge. SYS/E1 groups this task's versions, so the requested cutoff totals are resolvable; an independently identified reversal event cannot express its target using that sample alone. I retain `corrects_version` in the synthetic evidence/output and flag the missing graph extension rather than claiming the package supplies it.
3. **F3 / low: related-party version-selection order is underspecified for conflicting/tied observations.** The method says to select one correction version at known_at but does not prescribe authoritative source ordering or tied-observation handling as explicitly as the reporting method does. This task explicitly identifies v2 as a later correction and v3 as reversal, so the results are unambiguous. The independent calculation chooses latest observed eligible version and rejects ties; that conservative choice is recorded, not presented as a legal or generally sufficient source-order rule.
4. **F4 / low: reporting run business instant is indirect in the sample model.** Reporting method fixes business as_of per run, while TransformationRun properties include knowledge_cutoff but no as_of. The instant is recoverable through a produced fact's ReportContext.period_end in this task. I preserve it explicitly in run output metadata and flag that a general reusable run model should either carry as_of or constrain/refer to its contexts consistently.

The package source catalogue expressly records CAS36 original-page access limitations. I preserved that uncertainty and made no fresh legal-source verification because this independent review was offline by instruction.

## Verification actually performed

`python3 independent_review.py` executed 17 independent checks successfully. These cover the assigned calculations plus no accepted-amount invention, replay deduplication, same-version conflict rejection, opaque version labels, missing-unit blocking, late control evidence, missing supporting evidence, correction/reversal selection, weak-contact identity boundaries, scope separation and refusal to infer control from percentages. Exact checks/results are in `verification.json`; the reproducible script is saved alongside the outputs.

Both output model JSON files were serialized/read by the script, and model fields/relationships were manually reviewed against the copied local specification. Automated JSON Schema validation was attempted using the host Python and could not run because `jsonschema` is unavailable; no dependency was installed. There is no claim of a schema-validation pass, native database behavior, complete regulator/XBRL/accounting conformance or legal correctness. Package file hashes in `reviewed-files.json` pin the actual consulted copies; repository source may subsequently change independently.
