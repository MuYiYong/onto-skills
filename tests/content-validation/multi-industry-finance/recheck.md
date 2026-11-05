# Narrow recheck of finance findings F1–F4

All four findings are addressed in the current standalone packages. No remaining substantive gap was found within this requested recheck scope.

- **F1:** Transaction now has a nonnull unit distinct from currency; its application constraint forbids adding unlike amount units without conversion.
- **F2:** change_kind, revises_ref and reverses_ref retain source/event/version identity. REVISES_TRANSACTION and REVERSES_TRANSACTION provide the two explicit relationship types. The constraint/method require the appropriate references and reject missing, ambiguous, inconsistent, self/cyclic links. Independent compensation needs a selected authorized amount-effect policy; it is no longer conflated with same-event reversed status.
- **F3:** The method now requires source-confirmed correction/status ordering, preserves opaque version labels, and blocks tied/unknown/inconsistent/cyclic ordering. The earlier task can be expressed with E1/v2 correction→v1 and E1/v3 status_update→v2. Following that explicit chain preserves 70.00 / 75.00 / 30.00 CNY/yuan; no independent compensation or negative payment was invented.
- **F4:** TransformationRun now has nonnull business_as_of, independently preserving business cutoff alongside knowledge_cutoff and executed_at.

Using `/data/onto-skills/.venv/bin/python`, jsonschema Draft202012Validator with FormatChecker validated both frozen adapted output models and both current package models against the respective current bundled schemas: **4 passes, zero errors**. The original host-Python dependency limitation is resolved for this narrow check; the historical verification.json remains unchanged.

The recheck records 21 passed bounded checks, current-versus-frozen package hashes, the explicit Task B revision edges, exact schema validation results and all 14 original artifact hashes in recheck.json. All original review artifacts remain byte-identical. Only recheck.json and this recheck.md were added; package sources were not edited.

This is a narrow read-only model/method review with a synthetic consumer calculation. JSON Schema proves structure, not semantic constraint execution, legal/regulatory correctness, native database behavior or an independent compensation policy. No central fixtures, repository tests, network or production operations were used.
