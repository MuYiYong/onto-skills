# Task B — bounded FIBO Loan alignment

## Evidence boundary

This proposal uses only the copied fibo-ontology package. It is a **bounded candidate alignment**, not a fresh parsing of official FIBO files or a proof of full standard conformance. The package includes an index and curated method/example, but does not distribute the original Loans.rdf or imports closure.

Packaged provenance identifies repository revision `33a92cd34285d532c158da97bb42add089f135d3`, source path `LOAN/LoansGeneral/Loans.rdf`, SHA-256 `87024035dac38303e21738879202d87f0f37c1347a16119f9ec2b4e37e124f05`, and ontology version IRI `https://spec.edmcouncil.org/fibo/ontology/LOAN/20251201/LoansGeneral/Loans/`. The source catalogue additionally records AboutFIBOProd versionIRI `20261001`; that catalogue-level release marker must not replace the more specific observed ontology version. Retrieval date `2026-11-05` is provenance metadata, not the ontology version.

The index reports that Loans.rdf alone was parsed and imports were listed but not recursively loaded or reasoned. This trial reads that report; it has not independently reproduced the parse or hash. Source URI and standard term IRI remain separate.

## Business scope and retained subset

Assume the enterprise LoanContract represents a periodically repaid loan, with stable scoped loan_id and principal_amount/currency describing principal. The field names alone do not prove these definitions. Confirm loan kind and whether principal means original contractual principal, current principal or another measure before final approval.

Retain the candidate class:

- Loan: `https://spec.edmcouncil.org/fibo/ontology/LOAN/LoansGeneral/Loans/Loan`.

Record both observed direct parent classes without silently discarding them:

- CreditAgreementRepaidPeriodically: `https://spec.edmcouncil.org/fibo/ontology/FBC/DebtAndEquities/Debt/CreditAgreementRepaidPeriodically`.
- DebtInstrument: `https://spec.edmcouncil.org/fibo/ontology/FBC/FinancialInstruments/FinancialInstruments/DebtInstrument`.

Record the observed restriction summary `hasPrincipalAmount some MonetaryAmount`. The package does not give exact property or MonetaryAmount IRIs, domain/range declarations, their parent axioms, or import ontology IRIs in this bounded entry. Do not fabricate those identities or pretend their full closure was obtained. Retain symbolic references for review and mark the required imported definitions as not acquired.

The packaged example also states `hasGuarantor` qualified minimum 0. That lower bound does **not** require a guarantor to exist. Guarantees are outside this business scope; no guarantor fact or missing-guarantor error is introduced.

## Enterprise extension and graph mapping

Use an explicitly enterprise-owned namespace, here proposed as `urn:enterprise:loan-model:` pending ownership confirmation. Its terms are extensions, not additions to or redefinitions of standard FIBO IRIs.

| Enterprise element | Proposed graph representation | Standard alignment and status |
|---|---|---|
| LoanContract | LoanContract node | Candidate approximation to FIBO Loan, conditional on periodically repaid loan scope; no owl:equivalentClass assertion. |
| loan_id | Non-null single-valued identifier; key scoped by enterprise/source namespace | Preserves enterprise identity. This is an enterprise extension, not a FIBO-defined primary key or an OWL identity entailment. |
| principal_amount | Decimal property | Part of an approximation to the observed principal-amount restriction. Its numeric semantics and precision require business confirmation. |
| currency | Currency identifier/code property paired with principal_amount | Preserves the supplied denomination after validation; the package provides no exact currency property alignment, so no standard IRI is invented. |
| Two parent-class references | Explicit mapping records with provenance | Retain hierarchy meaning in documentation. Parent types/axioms are not implemented or materialized in this flat property graph, so their runtime mapping is unmapped. |
| MonetaryAmount object | Not instantiated in the requested flat model | Its identity, class membership, relationships and quantity reasoning are lost. Mapping is approximated, with loss explicitly accepted or revisited. |

No relationship entity is required by these three enterprise fields alone. If amount identity, provenance, multiple amounts or monetary-object semantics becomes a business question, introduce a separate amount object and align it after obtaining its exact standard definition. This is a possible later requirement, not an implemented hidden feature.

## Retained meaning, losses and execution

Retained: a traceable candidate Loan classification; the recorded periodically-repaid credit-agreement and debt-instrument parent meanings; the fact that the observed Loan restriction is existential over a MonetaryAmount; enterprise loan identity and principal denomination as business data. Retaining references in mapping documentation does not implement their OWL entailments.

Approximated/lost: flattening MonetaryAmount to amount/currency loses amount-object identity and object relationships; the graph does not derive inherited financial classifications or implement their full axioms; no full repayment schedule, imported constraints, standard property hierarchy or monetary reasoning is represented. Guarantee semantics beyond the recorded non-requirement are out of scope.

The observed `someValuesFrom` is an existential OWL restriction. It is not identical to a closed-world database requirement that both input fields be present. For this enterprise model, separately approve application checks for required loan_id, stable scoped uniqueness, valid decimal precision, required currency, and the chosen definition of principal (including whether negative amounts are valid for corrections). Such checks are enterprise policy and must not be presented as all of FIBO's axioms. Missing data under open-world OWL does not alone prove inconsistency, and distinct names do not establish distinct individuals. Domain/range axioms infer types rather than acting as ordinary SQL check constraints.

Application validation can enforce approved field/key policy. Business review accepts scope and mapping losses. No native database constraint, OWL reasoner or standard-equivalence behavior is proven. The local method is guidance, not an executable parser/reasoner.

## Included, excluded and not acquired

Included: the recorded Loan IRI, both parent IRIs, the principal-amount restriction summary, guarantee minimum-0 interpretation, provenance and enterprise-field mappings.

Intentionally excluded: guarantee modelling, repayment schedules, unrelated FIBO domains and financial-instrument queries outside the stated LoanContract scope. These exclusions limit which questions the model can answer.

Not acquired: original Loans.rdf in this package; recursively resolved imports; the complete property/class/axiom closure; exact principal/currency/MonetaryAmount term definitions; transitive parent restrictions; and a second-version ontology snapshot. No version-difference result can be computed from one curated observation.

Before a final standards-conformant mapping, obtain the exact approved FIBO version and its imports closure; parse classes/properties/domain/range/subclass/restrictions; reconcile principal and currency semantics; decide how much amount/hierarchy semantics to preserve; and explicitly accept the remaining loss. Full standard parsing, consistency and reasoning have **not** been proven by the package or by this trial. No network, database or model API was used.

Sources used: copied SKILL.md, references/fibo-index.json, references/sources.json, references/method.md and examples/worked-example.md; references/gql-handoff.md was read only to confirm the boundary of optional external syntax generation.
