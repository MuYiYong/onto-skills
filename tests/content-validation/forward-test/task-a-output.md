# Task A — neutral temporal lending model and risk candidates

## Scope and assumptions

This is a database-neutral model and manual analysis of user-supplied synthetic facts, not an implemented database or an automated credit decision. The analysis time is **2026-02-01**. Use a demonstration rule of **at least two distinct independent lending institutions with concurrently effective loans**; the threshold is not a regulatory or approval rule.

Treat B1/B2/B3 and L1/L2 as distinct, stable synthetic identities. For this exercise, a loan's supplied valid interval means an effective loan relationship; actual outstanding balance and settlement criteria remain unprovided. Interpret Z's null end as “not ended” only conditionally; a production feed must distinguish that meaning from “unknown end.” The current multi-institution conclusion for B2 remains negative even if its active status is uncertain. Dates are supplied at day precision; timezone and exact instants must be agreed before implementation.

## Concepts and keys

| Concept | Stable key and scope | Meaning and relevant attributes |
|---|---|---|
| Borrower | borrower_namespace + borrower_id | Verified business party in the borrower role; B1/B2/B3 use a synthetic namespace. Record party_type and identity_evidence. Sharing a phone does not redefine this key. |
| Lender | institution_namespace + lender_id | Independent institution at an agreed legal entity/group/branch granularity; L1/L2 are distinct only under the exercise assumption. Keep effective institution crosswalks. |
| Loan | source_system + loan_id, or an explicitly verified canonical loan key | Loan contract/obligation rather than an inquiry, application, credit limit or payment event. Store valid_from, valid_to, end_status, observed_at, status, source_record_id; amounts/currency only when supplied. X/Y/Z are user labels, not invented production IDs. |
| Disbursement | source_system + disbursement_record_id | One real funding event, with event_time, observed_at, amount/currency and reversal reference when available. The second disbursement for Z has its own event key and still refers to Loan Z. Its source ID and event time are currently unknown. |
| CreditInquiry | source_system + inquiry_record_id | Inquiry event with event_time, observed_at, purpose and participation roles. B3's 2026-01-30 L2 inquiry is not a loan. Its ID is not supplied. |
| Phone | token_namespace + phone_token | P represents a normalized/tokenized identifier, not a person. Token scope must prevent unrelated namespaces from being merged. |
| LoanApplication | source_system + application_record_id | Separate requested-credit event; not instantiated because none is supplied. |
| CreditFacility | source_system + facility_id | Granted credit arrangement/limit with its own validity; not instantiated or added to funded amounts. |
| Repayment | source_system + repayment_record_id | Actual payment/reversal event, separate from repayment schedules; not instantiated because none is supplied. |
| Account | institution_id + account_namespace + account_token | Optional relationship entity for shared or receiving accounts; no account facts are supplied. |

Business keys and source observation identities serve different purposes. A repeated import of the same (source_system, record_id) is idempotent; a new observation of the same Loan updates its provenance/history rather than creating another loan. Cross-source identity reconciliation requires evidence and must retain its decision history.

## Relationships and cardinality

All relationship instances have stable relation_id scoped by source, with source_record_id, observed_at and evidence reference. Cardinalities below describe only this bounded single-borrower, single-lender case.

| Directed relationship | Bounded cardinality and time |
|---|---|
| Borrower -BORROWS-> Loan | One borrower per supplied loan; a borrower can have many loans. Loan validity controls the effective loan relationship. Joint borrowing remains out of scope. |
| Lender -PROVIDES-> Loan | One lender per supplied loan; lender can provide many loans. Syndication and assignments need a separate participation model if introduced. |
| Loan -HAS_DISBURSEMENT-> Disbursement | One loan per event; many actual events per loan. Event time is on Disbursement, so two Z events are not collapsed by matching endpoints. |
| Loan -HAS_REPAYMENT-> Repayment | One loan per payment event; event time is on Repayment; reversals identify the original record. |
| CreditInquiry -INQUIRY_SUBJECT-> Borrower | The B3 inquiry concerns B3. |
| CreditInquiry -AT_LENDER-> Lender | Links the supplied “at L2” fact without inventing whether L2 initiated, performed or received the inquiry. Refine to the corresponding explicit role once confirmed. |
| Borrower -USES_PHONE-> Phone | Many-to-many binding with valid_from, valid_to, observed_at, matching method, confidence and evidence. Exact January start/end dates have not been supplied. |
| Borrower -APPLIES-> LoanApplication -SUBMITTED_TO-> Lender | Separate event path; no instances claimed. |
| Borrower -HAS_FACILITY-> CreditFacility <-GRANTS- Lender | Effective arrangement, independent from Loan/Disbursement. Loan -DRAWS_ON-> CreditFacility only if supported by source evidence. |
| Borrower -USES_ACCOUNT-> Account; Disbursement -PAYS_TO-> Account | Optional binding/receiving paths; no instances claimed. Account sharing alone does not establish identity. |

The known fact paths are B1-BORROWS-X<-PROVIDES-L1, B1-BORROWS-Y<-PROVIDES-L2, B2-BORROWS-Z<-PROVIDES-L1, two distinct Z-HAS_DISBURSEMENT event paths, and a historical B1-USES_PHONE-P<-USES_PHONE-B2 path. B3's historical loan and L2 inquiry remain separate paths.

## Temporal, evidence and computation rules

1. Use half-open validity intervals: active(loan,t) iff valid_from <= t and (end_status = open or t < valid_to). Null may be treated as open only after the source contract confirms that meaning; an unknown end produces an uncertain active classification.
2. First select effective qualifying loans, then project canonical independent lender identities and count distinct lenders per borrower. Repeated disbursements and repeated imported records do not add institutions. Applications, facilities and inquiries do not enter that count.
3. For a whole-window overlap question, partition at loan start/end boundaries and inspect concurrent lender sets. “Appeared within January” and “coexisted at one instant” are different questions. Non-overlapping sequential loans do not satisfy concurrent exposure.
4. Keep event_time (what happened), valid time (when a state/binding held) and observed_at (when a record became known) separate. The supplied facts permit an effective-date reconstruction; they cannot answer “what was known on 2026-02-01” without observed_at and revision history. A late-arriving record retains its actual effective time. A single observed_at does not provide a full transaction-time interval; preserve correction history or add recorded_to if required.
5. A phone association candidate requires overlap of both party-to-phone bindings and the chosen analysis window. “Shares P during January” supports historical association evidence, but no continuing binding on February 1 is established. Do not invent exact January boundaries, infer identity equality or infer fraud.
6. Keep raw source IDs, record types, participation roles, times, matching evidence and rejection/correction history for every derived candidate. Mark computed results as model-inference; the synthetic input facts remain user-asserted evidence. Preserve exculpatory evidence and open questions with the candidate.
7. Amount aggregation requires a common as_of, currency and actual outstanding-balance definition. Do not add facility limits to disbursement amounts, or sum all disbursements as though they were current balances. No monetary exposure score is calculated here.
8. Application checks enforce identity, interval consistency, deduplication, institution reconciliation and candidate computation. Business review approves thresholds and matching policy. No database-enforced constraint or native runtime behavior is claimed.

## As-of results

| Borrower | Effective institution evidence on 2026-02-01 | Result under demonstration rule |
|---|---|---|
| B1 | X/L1: 2026-01-01 <= t < 2026-03-01; Y/L2: 2026-01-15 <= t < 2026-02-15 | **Multi-institution review candidate**: distinct set {L1,L2}, count 2. The loans overlap on [2026-01-15,2026-02-15). This is a candidate under the supplied interval semantics, not proof of unpaid balances or fraud. |
| B2 | Z/L1: active if null means open; distinct set {L1}, count 1 | **No multi-institution candidate.** The second Z disbursement is another event on one loan at one lender. Its unknown event date prevents event-order conclusions. If null means unknown, active status is uncertain, but there is still no supplied second lender. |
| B3 | L1 loan ended 2025-12-31, so not active on t; L2 inquiry occurred 2026-01-30 | **No multi-institution candidate.** Zero supplied current loan institutions. The inquiry does not supply an L2 loan. |

B1/B2 receive a separate **historical shared-phone association for review during January**, conditional on source evidence for simultaneous binding. Exact overlap must be documented. It does not transfer B1's L2 loan to B2, merge B1/B2 or establish a current shared-phone edge at the February 1 snapshot.

Useful negative checks: two same-lender loans still count one lender; two Z disbursements still count one lender; an inquiry does not add a lender; an ended loan does not count at t; phone reuse without overlapping bindings does not count as simultaneous sharing.

## Open questions and delivery status

Confirm the business threshold; legal entity/group/branch granularity and effective institution crosswalk; whether “valid loan” requires positive unpaid balance; what null ends mean; exact date/timezone and end semantics; source IDs and observed_at; the two disbursement dates/status/reversals; the exact phone binding intervals, token namespace, confidence and permissible association purpose; inquiry participation roles; and any joint/assigned/syndicated loans. The neutral model is a reviewable draft, not ready for production decisions.

If NebulaGraph Graph Type DDL is requested with no GQL capability available, deliver this model and state that verified Graph Type DDL generation is unavailable in this isolated environment. Obtain the target NebulaGraph version and use the upstream nebula-gql-skills capability only after confirming the installed release explicitly supports Graph Type DDL: https://github.com/MuYiYong/nebula-gql-skills. Do not assume query generation or procedure generation covers DDL, and do not synthesize syntax from memory. Hand off keys, logical types, directions, temporal policy, execution locations and unresolved semantics. Recheck returned DDL against them and report real execution separately. No skill installation, DDL generation or database execution occurred here.

Sources used: the copied multi-lending-detection SKILL.md, bundled domain/method/source index, graph specification/schema, and worked examples. Financial and OWL references are provenance pointers; the temporal policy and demonstration risk rule are packaged project-curated advice, not official FIBO or regulatory definitions.
