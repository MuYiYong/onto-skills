"""Independent synthetic forward test; reads only copied standalone packages."""
from pathlib import Path
from copy import deepcopy
from datetime import datetime
from decimal import Decimal
import hashlib
import json

ROOT=Path.cwd(); OUT=ROOT/'outputs';OUT.mkdir(exist_ok=True)
def dump(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def instant(s):return datetime.fromisoformat(s.replace('Z','+00:00'))
def money(value):return format(value,'.2f')
def selected_versions(records,cutoff,identity,version):
    seen={};replays=0
    for row in records:
        key=tuple(row[k] for k in identity+[version])
        if key in seen:
            if seen[key]!=row:raise ValueError('same-version-payload-conflict:'+str(key))
            replays+=1
        else:seen[key]=row
    groups={}
    for row in seen.values():
        if instant(row['observed_at'])<=instant(cutoff):groups.setdefault(tuple(row[k] for k in identity),[]).append(row)
    result=[]
    for key,rows in groups.items():
        latest=max(instant(r['observed_at']) for r in rows)
        winners=[r for r in rows if instant(r['observed_at'])==latest]
        if len(winners)!=1:raise ValueError('ambiguous-source-order:'+str(key))
        result.append(winners[0])
    return sorted(result,key=lambda r:tuple(r[k] for k in identity)),replays,len(seen)

# Task A input uses the task's facts; exact times/unit/definition ids below are
# explicitly synthetic choices, not inferred regulator template requirements.
a={
'id':'independent-task-a','classification':'project-curated','synthetic':True,
'assumptions':[
'Baseline amounts are expressed in whole yuan of currency CNY; task gave CNY amounts but no separate unit, so yuan is an explicit synthetic assumption, not a regulatory requirement.',
'Date-only task statements are assigned example Asia/Shanghai instants. No extra source arrives on the selected cutoff days, so start/end-of-day choices do not change these results.',
'DEMO-R1 and metric DEMO-R1:loanBalance definition synthetic-1 are user-task identifiers, not a real Chinese regulator report/template/threshold.',
'S1 has supplied prior business acceptance; its reported amount and source lineage were not supplied and remain unknown.',
'Locally created RUN-A-NOV3/S3 are a design draft only, with no new submitted/received/accepted event.'
],
'reporting_entity':{'namespace':'independent-synthetic','entity_id':'C1','legal_name':'Synthetic C1'},
'report_definition':{'jurisdiction':'CN-regulator-unspecified','report_code':'DEMO-R1','template_version':'synthetic-1','frequency':'unspecified'},
'metric_definition':{'metric_id':'DEMO-R1:loanBalance','definition_version':'synthetic-1','meaning':'Task-supplied instant loan balance','unit':'yuan','aggregation':'sum-selected-active-balance-records','rule_reference':'synthetic-task-only'},
'context':{'context_id':'CTX-C1-DEMO-R1-20261031','entity_id':'C1','scope':'individual-C1','period_kind':'instant','period_start':None,'period_end':'2026-10-31T23:59:59+08:00','timezone':'Asia/Shanghai','dimensions':{}},
'known_at_runs':['2026-11-01T18:00:00+08:00','2026-11-03T18:00:00+08:00'],
'source_records':[],
'submissions':[{'submission_id':'S1','revision':1,'scope_key':'C1|DEMO-R1|synthetic-1|CTX-C1-DEMO-R1-20261031','payload_hash':None,'historical_amount':None},{'submission_id':'S2','revision':2,'scope_key':'C1|DEMO-R1|synthetic-1|CTX-C1-DEMO-R1-20261031','supersedes':'S1','payload_hash':'computed-from-run-a-nov1'}],
'validation_checks':[{'check_id':'LOCAL-S2','submission_id':'S2','kind':'local-business-check','rule_version':'synthetic-check-1','checked_at':'2026-11-01T10:00:00+08:00','result':'passed'}],
'receipts':[{'receipt_id':'BUSINESS-S1','submission_id':'S1','kind':'business','received_at':'2026-11-01T09:00:00+08:00','status':'accepted','evidence':'Task-supplied prior acceptance; timestamp is a synthetic scheduling choice.'},{'receipt_id':'TRANSPORT-S2','submission_id':'S2','kind':'transport','received_at':'2026-11-01T11:00:00+08:00','status':'received','evidence':'Task-supplied transport receipt; timestamp is a synthetic scheduling choice.'}],
'unresolved':['Actual regulator/agency, official template/metric version, governance owner, lawful reporting unit, applicable calendar/deadline and quality formulas.','S1 exact accepted payload amount/lineage and its payload hash are not supplied.']}
def ar(record_id,version,amount,observed):return {'source_system':'SYS','record_id':record_id,'source_version':version,'event_time':'2026-10-31T23:59:59+08:00','observed_at':observed,'amount':amount,'unit':'yuan','currency':'CNY','status':'active'}
a['source_records']=[ar('K1','v1','80','2026-10-31T18:00:00+08:00'),ar('K1','v2','90','2026-11-02T10:00:00+08:00'),ar('K2','v1','20','2026-10-31T18:00:00+08:00')]
a['source_records'].append(deepcopy(a['source_records'][2]))
dump(OUT/'task-a-input.json',a)

def evaluate_a(data,cutoff,run_id,submission_id):
    rows,replays,unique=selected_versions(data['source_records'],cutoff,['source_system','record_id'],'source_version')
    rows=[r for r in rows if instant(r['event_time'])<=instant(data['context']['period_end']) and r['status']=='active']
    missing=[r['source_system']+'/'+r['record_id']+'/'+r['source_version'] for r in rows if not r.get('unit')]
    currencies={r['currency'] for r in rows};units={r.get('unit') for r in rows}
    blocked=bool(missing) or len(currencies)!=1 or units!={data['metric_definition']['unit']}
    contributions=[{'source_record_key':[r['source_system'],r['record_id'],r['source_version']],'amount':money(Decimal(r['amount'])),'currency':r['currency'],'unit':r.get('unit'),'conversion_reference':'same-unit' if r.get('unit')=='yuan' else None} for r in rows]
    total=None if blocked else money(sum((Decimal(r['amount']) for r in rows),Decimal('0')))
    state={'S1':'business-accepted','S2':'transport-received-business-pending'}
    return {'run_id':run_id,'logic_version':'independent-selected-instant-balance-1','as_of':data['context']['period_end'],'known_at':cutoff,'input_snapshot_hash':digest(data['source_records']),'selected_source_versions':[c['source_record_key'] for c in contributions],'duplicate_replays_ignored':replays,'unique_source_version_count':unique,'source_contributions':contributions,'reported_fact':{'submission_id':submission_id,'fact_id':'loanBalance','metric_key':['DEMO-R1:loanBalance','synthetic-1'],'context_id':data['context']['context_id'],'value':total,'currency':'CNY','unit':'yuan','status':'blocked' if blocked else 'present','nil_reason':'missing source unit: '+','.join(missing) if missing else None},'lineage_paths':[{'from':c['source_record_key'],'via':run_id,'fact_key':[submission_id,'loanBalance'],'submission':submission_id,'contribution':c['amount'],'unit':c['unit']} for c in contributions],'submission_state':state,'current_business_accepted_submission_id':'S1','current_accepted_amount':None,'accepted_amount_unknown_reason':'S1 payload amount was not supplied; calculated S2/draft S3 must not be substituted.','s2_supersedes_s1':True,'business_acceptance_not_inferred_from':['passed local check','transport receipt received','SUPERSEDES edge'],'blocked_publication':blocked}
ra1=evaluate_a(a,a['known_at_runs'][0],'RUN-A-NOV1','S2');ra3=evaluate_a(a,a['known_at_runs'][1],'RUN-A-NOV3','S3-DRAFT')
am=deepcopy(a)
for row in am['source_records']:
    if row['record_id']=='K1' and row['source_version']=='v2':row['unit']=None
ram=evaluate_a(am,am['known_at_runs'][1],'RUN-A-MISSING-UNIT','S3-BLOCKED')
dump(OUT/'task-a-missing-unit-input.json',am)
dump(OUT/'task-a-results.json',{'nov1':ra1,'nov3_new_run':ra3,'nov3_missing_unit':ram})
ma=json.load(open(ROOT/'financial-regulatory-reporting/examples/graph-model.json'))
ma['model_id']='independent-demo-r1-lineage';ma['description']='Synthetic C1 DEMO-R1 instant loanBalance lineage; no regulator-specific template or legal requirement inferred.'
ma['assumptions']=a['assumptions'];ma['unresolved']=a['unresolved']+['TransformationRun in the supplied model has no direct business as_of property; in this adapted design as_of is recoverable through ReportedFact→ReportContext.period_end, and run metadata explicitly retains the selected instant. This difference is recorded rather than concealed.']
dump(OUT/'task-a-graph-model.json',ma)

# Task B: distinct source event identity, temporal confirmed-control evidence,
# three immutable versions of E1, E2 distinct, and separate scope views.
b={
'id':'independent-task-b','classification':'project-curated','synthetic':True,
'regime':'demonstration-confirmed-control-only','rule_version':'synthetic-control-1',
'as_of_trade':'2026-10-31T13:00:00+08:00','knowledge_cutoffs':['2026-11-01T18:00:00+08:00','2026-11-03T18:00:00+08:00','2026-11-05T18:00:00+08:00'],
'assumptions':['All identities/evidence are invented for this task. Party namespace is independent-synthetic.','valid_to=null explicitly means ongoing, not an unknown end. Confirmed control is supplied evidence, not inferred from ownership.','Amounts are whole yuan of CNY as an explicit synthetic assumption; the packaged Transaction model omits a unit property, recorded as finding F1.','E1/v3 reversed is a newer state of the SAME event E1, not a separate negative-cash event; original source amount remains 45. Only current executed occurrence amounts are summed.','Date-only task dates receive example Asia/Shanghai instants; those choices do not affect selection in the supplied dates.','The consolidated disclosure variation is the package local demonstration rule for explicitly supplied scope, not a complete CAS36 legal determination.'],
'parties':[{'namespace':'independent-synthetic','party_id':i,'party_kind':'legal_entity','display_name':'Synthetic '+i} for i in ['R','BANK','VENDOR','OTHER']],
'controls':[{'assessment_id':'CTRL-R-'+target,'controller':'R','controlled':target,'regime':'demonstration-confirmed-control-only','basis':'explicit-confirmed-task-evidence','status':'confirmed','valid_from':'2026-01-01T00:00:00+08:00','valid_to':None,'observed_at':'2026-01-02T09:00:00+08:00','evidence_id':'EV-R-'+target} for target in ['BANK','VENDOR']],
'evidence':[{'evidence_id':'EV-R-'+target,'kind':'synthetic-confirmed-control-evidence','content':'Task supplies explicit confirmed R control of '+target,'content_hash':digest({'task_control':'R->'+target}),'status':'current','authority':'Synthetic task evidence only; not a legal source document'} for target in ['BANK','VENDOR']],
'weak_links':[{'evidence_id':'CONTACT-BANK-OTHER','left':'BANK','right':'OTHER','kind':'shared_contact','contact_token':'invented-contact-token','status':'current','observed_at':'2026-01-02T09:00:00+08:00'}],
'ownership_positions':[],
'unsupported_ownership_claim':{'claim':'Every ownership percentage implies control; indirect percentages may be multiplied to establish control.','supplied_control_evidence':None,'example_percentages':['1','60','60'],'requested_determination':'No confirmed control can be produced solely by this unsupported claim.'},
'financial_disclosure_scope':{'basis':'financial_statement','entities':['BANK','VENDOR'],'scope_source':'explicit-task-supplied-consolidated-scope','scope_version':'synthetic-1'},
'bank_regulatory_view':{'basis':'regulatory','bank':'BANK','automatic_consolidation_exemption':False},
'amount_basis':'current-executed-occurrence-amounts-not-contract-or-balance',
'review_decision':{'decision':'pending','reviewer_role':None,'policy_version':'actual-governance-version-unresolved'},
'unresolved':['Actual applicability of the 2025 Chinese bank/insurance rule, full related-party definition, transaction classification, thresholds, governance procedure and reporting/disclosure duties.','Authoritative current accounting standard/interpretations and complete disclosure requirements have not been independently verified; copied package explicitly records CAS36 original-page access limitation.'],
 'transactions':[]}
def tr(v,amount,obs,status='executed',txid='E1'):
    return {'source_system':'SYS','tx_id':txid,'tx_version':v,'from_party':'BANK','to_party':'VENDOR','event_time':b['as_of_trade'],'observed_at':obs,'amount':amount,'currency':'CNY','unit':'yuan','status':status,'corrects_version':None if v=='v1' else 'v1' if v=='v2' else 'v2'}
b['transactions']=[tr('v1','40','2026-10-31T18:00:00+08:00'),tr('v2','45','2026-11-02T10:00:00+08:00'),tr('v1','30','2026-10-31T18:00:00+08:00',txid='E2'),tr('v3','45','2026-11-04T10:00:00+08:00','reversed')]
dump(OUT/'task-b-input.json',b)

def active_controls(data,known):
    trade=instant(data['as_of_trade']);cutoff=instant(known)
    evidence={e['evidence_id']:e for e in data['evidence']}
    return [c for c in data['controls'] if c['status']=='confirmed' and c['regime']==data['regime'] and instant(c['valid_from'])<=trade and (c['valid_to'] is None or trade<instant(c['valid_to'])) and instant(c['observed_at'])<=cutoff and evidence.get(c['evidence_id'],{}).get('status')=='current']

def relation(data,left,right,known):
    controls=active_controls(data,known)
    graph={}
    for c in controls:graph.setdefault(c['controller'],[]).append(c)
    def paths(start,end):
        result=[]
        def walk(node,visited,path):
            if node==end:
                result.append(path);return
            for c in graph.get(node,[]):
                if c['controlled'] not in visited:walk(c['controlled'],visited|{c['controlled']},path+[c])
        walk(start,{start},[])
        return result
    evidence_paths=[]
    for controller in sorted({c['controller'] for c in controls}):
        lp=paths(controller,left);rp=paths(controller,right)
        for l in lp:
            for r in rp:
                if l or r:evidence_paths.append({'common_controller':controller,'left_path':[c['assessment_id'] for c in l],'right_path':[c['assessment_id'] for c in r],'evidence_ids':sorted({c['evidence_id'] for c in l+r})})
    return {'left':left,'right':right,'decision':'candidate' if evidence_paths else 'not_demonstrated','paths':evidence_paths,'legal_determination':'not-made','identity_merge':False}

def evaluate_b(data,known):
    rows,replays,unique=selected_versions(data['transactions'],known,['source_system','tx_id'],'tx_version')
    current=[];gross=Decimal('0');candidate_ids=[]
    for row in rows:
        rel=relation(data,row['from_party'],row['to_party'],known)
        executed=row['status']=='executed'
        eligible=rel['decision']=='candidate' and executed and instant(row['event_time'])<=instant(data['as_of_trade'])
        contribution=Decimal(row['amount']) if eligible else Decimal('0')
        gross+=contribution
        if eligible:candidate_ids.append(row['tx_id'])
        current.append({'transaction_version_key':[row['source_system'],row['tx_id'],row['tx_version']],'status':row['status'],'source_amount':money(Decimal(row['amount'])),'contribution':money(contribution),'currency':row['currency'],'unit':row['unit'],'relationship_decision':rel['decision'],'path_evidence':rel['paths'],'exclusion_reason':None if eligible else 'current-status-'+row['status'],'correction_predecessor_version':row['corrects_version']})
    disclosed=Decimal('0')
    for row in current:
        # Every task transaction is BANK→VENDOR, both explicitly in supplied scope.
        if not {'BANK','VENDOR'}.issubset(set(data['financial_disclosure_scope']['entities'])):disclosed+=Decimal(row['contribution'])
    return {'trade_as_of':data['as_of_trade'],'known_at':known,'regime':data['regime'],'selected_current_transactions':current,'current_executed_candidate_event_ids':sorted(candidate_ids),'candidate_relation_bank_vendor':relation(data,'BANK','VENDOR',known),'bank_other_shared_contact':relation(data,'BANK','OTHER',known),'gross_current_executed_candidate_amount':money(gross),'currency':'CNY','unit':'yuan','bank_regulatory_view':{'candidate_amount':money(gross),'consolidation_exclusion_applied':False,'legal_or_approval_result':'not-determined'},'explicit_consolidated_financial_disclosure_view':{'scope':['BANK','VENDOR'],'candidate_relationship_retained':True,'raw_current_executed_amount_retained':money(gross),'internal_scope_adjustment':money(gross-disclosed),'displayed_disclosure_amount':money(disclosed),'basis':'financial_statement','policy':'package-local-demonstration-rule; formal disclosure requirements unresolved'},'retained_version_keys':[[r['source_system'],r['tx_id'],r['tx_version']] for r in data['transactions'] if instant(r['observed_at'])<=instant(known)],'review_decision':'pending','ownership_claim':{'accepted':False,'confirmed_control_generated':False,'reason':'OwnershipPosition and ControlAssessment are separate; a percentage or product of percentages supplies no universal control rule.'},'input_snapshot_hash':digest(data['transactions']),'legal_determination':'not-made'}
rb={name:evaluate_b(b,known) for name,known in zip(['as_known_nov1','as_known_nov3','as_known_nov5'],b['knowledge_cutoffs'])}
dump(OUT/'task-b-results.json',rb)
mb=json.load(open(ROOT/'related-party-transaction-modeling/examples/graph-model.json'))
mb['model_id']='independent-confirmed-control-transactions';mb['description']='Synthetic R common-control evidence and BANK→VENDOR versioned transactions; regulatory/financial disclosure views are explicitly separate.'
mb['assumptions']=b['assumptions'];mb['unresolved']=b['unresolved']
# Explicit consumer adaptation, recorded as a finding; source package stays unchanged.
tx=next(n for n in mb['node_types'] if n['name']=='Transaction')
tx['properties'].append({'name':'unit','logical_type':'string','nullable':False,'multivalued':False,'business_meaning':'Explicit consumer-added amount unit, e.g. yuan. Package method requires it but packaged sample Transaction schema does not supply this property.','source_ids':['onto-related']})
mb['unresolved']+=['Package method requires reversal/correction back-reference but sample graph has no explicit edge/property. This task groups E1 versions by SYS/E1 and records corrects_version in evidence outputs; distinct reversal-event linkage needs a declared model extension.']
dump(OUT/'task-b-graph-model.json',mb)

# Evidence graphs retain identity, endpoints, controls and per-version assessments.
instance_a={
'identity_keys':{'ReportingEntity':['independent-synthetic','C1'],'ReportDefinition':['CN-regulator-unspecified','DEMO-R1','synthetic-1'],'MetricDefinition':['DEMO-R1:loanBalance','synthetic-1'],'ReportContext':['CTX-C1-DEMO-R1-20261031'],'SourceRecord':['source_system','record_id','source_version'],'ReportedFact':['submission_id','fact_id']},
'context':a['context'],
'run_fact_edges':[{'edge':'DERIVED_BY','from':[r['reported_fact']['submission_id'],'loanBalance'],'to':r['run_id']} for r in [ra1,ra3]],
'contribution_edges':[{'edge':'CONSUMES_RECORD','from':r['run_id'],'to':c['source_record_key'],'contribution':c['amount'],'conversion_reference':c['conversion_reference']} for r in [ra1,ra3] for c in r['source_contributions']],
'submission_edges':[{'edge':'SUPERSEDES','from':'S2','to':'S1'}],
'receipt_edges':[{'edge':'ACKNOWLEDGES','from':r['receipt_id'],'to':r['submission_id'],'kind':r['kind'],'status':r['status']} for r in a['receipts']],
'local_check_edges':[{'edge':'CHECKS_FACT','from':'LOCAL-S2','to':['S2','loanBalance'],'result':'passed'}],
'state_result':'S2 supersedes S1 as a proposed revision; S1 remains the current business-accepted submission until S2 obtains qualifying business acceptance.'}
dump(OUT/'task-a-evidence-graph.json',instance_a)
instance_b={'party_identity':'namespace + party_id; shared contact creates no sameAs',
'control_nodes':b['controls'],'evidence_nodes':b['evidence'],
'control_edges':[e for c in b['controls'] for e in [{'edge':'CONTROLLER','from':c['assessment_id'],'to':['independent-synthetic',c['controller']]},{'edge':'CONTROLLED','from':c['assessment_id'],'to':['independent-synthetic',c['controlled']]},{'edge':'SUPPORTED_BY','from':c['assessment_id'],'to':c['evidence_id']}]],
'transaction_edges':[e for t in b['transactions'] for e in [{'edge':'FROM_PARTY','from':[t['source_system'],t['tx_id'],t['tx_version']],'to':['independent-synthetic',t['from_party']]},{'edge':'TO_PARTY','from':[t['source_system'],t['tx_id'],t['tx_version']],'to':['independent-synthetic',t['to_party']]}]],
'assessment_snapshots':{k:{'known_at':v['known_at'],'case_ids':['case-'+k+'-SYS-'+t['transaction_version_key'][1] for t in v['selected_current_transactions']],'result':v['current_executed_candidate_event_ids']} for k,v in rb.items()},
'weak_contact':{'evidence':b['weak_links'][0],'control_edge_created':False,'identity_merge_created':False},
'adaptations':[{'field':'Transaction.unit','reason':'missing from packaged sample despite method requiring amount units','classification':'model-inference'},{'field':'corrects_version in task evidence','reason':'source package lacks explicit correction/reversal link in graph sample; this task version chain is preserved externally and not silently claimed to exist in that graph'}]}
dump(OUT/'task-b-evidence-graph.json',instance_b)

# Actual executable checks assert task-specific output and meaningful counterfactuals.
checks=[]
def check(name,condition):
    if not condition:raise AssertionError(name)
    checks.append({'id':name,'result':'passed'})
check('A-Nov1-selects-80-plus-20',ra1['reported_fact']['value']=='100.00' and ra1['selected_source_versions']==[['SYS','K1','v1'],['SYS','K2','v1']])
check('A-Nov3-selects-90-plus-20',ra3['reported_fact']['value']=='110.00' and ra3['selected_source_versions']==[['SYS','K1','v2'],['SYS','K2','v1']])
check('A-exact-replay-not-doubled',ra1['duplicate_replays_ignored']==1 and ra1['unique_source_version_count']==3)
check('A-transport-and-local-check-do-not-accept-S2',ra1['current_business_accepted_submission_id']=='S1' and ra1['submission_state']['S2']=='transport-received-business-pending')
check('A-missing-unit-blocks-no-partial-total',ram['reported_fact']['value'] is None and ram['blocked_publication'] and 'SYS/K1/v2' in ram['reported_fact']['nil_reason'])
check('A-accepted-S1-amount-is-unknown',ra1['current_accepted_amount'] is None)
check('B-Nov1-40-plus-30',rb['as_known_nov1']['gross_current_executed_candidate_amount']=='70.00')
check('B-Nov3-45-plus-30',rb['as_known_nov3']['gross_current_executed_candidate_amount']=='75.00')
check('B-Nov5-reversal-retains-E2-only',rb['as_known_nov5']['gross_current_executed_candidate_amount']=='30.00' and rb['as_known_nov5']['current_executed_candidate_event_ids']==['E2'])
check('B-reversed-E1-still-related-by-evidence',rb['as_known_nov5']['selected_current_transactions'][0]['relationship_decision']=='candidate' and rb['as_known_nov5']['selected_current_transactions'][0]['status']=='reversed')
check('B-shared-contact-not-related-or-identity-merged',all(v['bank_other_shared_contact']['decision']=='not_demonstrated' and not v['bank_other_shared_contact']['identity_merge'] for v in rb.values()))
check('B-financial-scope-does-not-exempt-regulatory-view',all(v['explicit_consolidated_financial_disclosure_view']['displayed_disclosure_amount']=='0.00' and v['bank_regulatory_view']['candidate_amount']==v['gross_current_executed_candidate_amount'] for v in rb.values()))
check('B-no-ownership-to-control-inference',all(not v['ownership_claim']['confirmed_control_generated'] for v in rb.values()))
# Counterfactual: late control evidence disappears from old knowledge snapshots.
late=deepcopy(b)
late['controls'][1]['observed_at']='2026-11-02T09:00:00+08:00'
check('B-late-control-not-backdated',relation(late,'BANK','VENDOR',b['knowledge_cutoffs'][0])['decision']=='not_demonstrated')
# Counterfactual: remove evidence, preserving the confirmed-looking edge itself.
missing_evidence=deepcopy(b);missing_evidence['evidence']=missing_evidence['evidence'][:1]
check('B-confirmed-label-without-evidence-insufficient',relation(missing_evidence,'BANK','VENDOR',b['knowledge_cutoffs'][1])['decision']=='not_demonstrated')
# Counterfactual: opaque version text changes do not change observed ordering.
opaque=deepcopy(a)
for row in opaque['source_records']:
    if row['record_id']=='K1':row['source_version']='zz' if row['source_version']=='v1' else 'aa'
check('A-version-labels-not-sorted',evaluate_a(opaque,a['known_at_runs'][1],'OPAQUE','DRAFT')['reported_fact']['value']=='110.00')
# Counterfactual: conflicting exact source version must stop selection.
conflict=deepcopy(a);conflict['source_records'].append(deepcopy(conflict['source_records'][0]));conflict['source_records'][-1]['amount']='999'
try:
    evaluate_a(conflict,a['known_at_runs'][0],'CONFLICT','DRAFT')
except ValueError as exc:check('A-conflicting-same-version-rejected','same-version-payload-conflict' in str(exc))
else:check('A-conflicting-same-version-rejected',False)
dump(OUT/'verification.json',{'scope':'Independent forward-test computations using copied package guidance and new synthetic task input; no packaged acceptance files or repository tests read.','checks':checks,'count':len(checks),'clinical_or_legal_or_native_validation':False})
print(json.dumps({'checks_passed':len(checks),'task_a':{'nov1':ra1['reported_fact']['value'],'nov3':ra3['reported_fact']['value'],'missing_unit':ram['reported_fact']['value'],'current_accepted':'S1'},'task_b':{k:v['gross_current_executed_candidate_amount'] for k,v in rb.items()}},indent=2))
