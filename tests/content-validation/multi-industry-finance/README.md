# Independent finance forward review

Dated2026-11-06; fresh synthetic reporting and related-party tasks were performed from frozen independent package copies without consulting central fixtures, repository tests or packaged acceptance/input cases. The original [assessment](assessment.md), task inputs, evidence graphs, output models, [17 checks](verification.json), reproduction script and consulted-file manifest are preserved unchanged. Those findings concern the then-frozen packages.

The review identified missing amount-unit and revision-link fields, source-order clarification and a run business cutoff. All four were addressed in current source. The separate [narrow recheck](recheck.md) records21 passed bounded checks, including four actual schema validations using the repository venv; its [JSON record](recheck.json) binds the current consulted files and preserves all14 original artifact hashes. The original host-Python missing-jsonschema limitation remains in the historical verification instead of being rewritten.

The original output models are consumer adaptations of the earlier model, not current package snapshots. Their schema pass does not add the later source fields retroactively. Reproduction instructions create a fresh calculation; changed source models need new hashes and must not replace dated originals. The [receipt](receipt.json) binds all stored artifacts and current finance package bytes.

These are synthetic consumer checks and model/method review, not full legal/regulatory/accounting/FHIR/XBRL validation, live filing, database or production execution. The parent full asset validator also accepts both saved adapted graph models. Temporary paths in unchanged historical records only identify the original execution workspace.
