# Healthcare synthetic care-pathway data model

This original example models data evidence across two encounters using a deliberately pinned published HL7® FHIR® R4 4.0.1 baseline. It supplies no care recommendation, real patient information, terminology code list or complete FHIR conformance claim. HL7 and FHIR are registered trademarks of Health Level Seven International; use does not imply endorsement.

- [input.json](input.json): wholly synthetic partial-resource export with explicit server/version/current claims, patient mapping evidence and local authorization/view policy.
- [graph-model.json](graph-model.json): complete Graph Model Specification 1.0 structure, 9 node types and 20 edge types; neutral target and explicit mapping losses/unresolved deployment requirements.
- [acceptance.json](acceptance.json): 17 positive/negative cases with exact expected IDs, counts and states. Null conclusions mean unassessed, never zero/normal/negative.

The standalone scenario bundles byte-identical files and a local operation contract. Requests and event documentation are separate: revoked ServiceRequest does not create a completed Procedure; not-done remains documentation. Observation entered-in-error is invalid evidence; unknown value and absent result are separate. Opaque record versions, repeat encounters, coding versions, quantities, clocks, identity evidence and authorized exact-version retraction remain explicit.

Static/offline example checks establish only bounded data semantics. They do not prove clinical correctness, full FHIR/profile/terminology conformance, native database execution, privacy/compliance controls or GUI/platform behavior. No database operations are included.
