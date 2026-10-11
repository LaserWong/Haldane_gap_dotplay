from pathlib import Path
p=Path(__file__).resolve().parent;s=(p/'controller.py').read_text()
s=s.replace('P=Path(__file__).resolve().parent','SOURCE=Path(__file__).resolve().parent\nP=Path(os.environ.get("BILAYER_PRODUCTION_JOB",str(SOURCE/"UNAUTHORIZED_JOB"))).resolve()\nimport production_admission as production')
s=s.replace("files=[P/'whole',P/'whole.cpp',P/'controller.py']+[P.parent/","files=[SOURCE/'whole',SOURCE/'whole.cpp',SOURCE/'production_controller.py',SOURCE/'production_admission.py',SOURCE/'pencil24.py',SOURCE/'production_finalize.py',P/'EXPECTED_M012.json']+[SOURCE.parent/")
s=s.replace("+[P.parent/'bilayer_brauer_rule_compiler/run'","+[SOURCE.parent/'bilayer_brauer_rule_compiler/run'")
a=s.index('def validate_budget(');b=s.index('def admit(',a)
s=s[:a]+"def validate_budget(ledger):\n production.validate_ledger(ledger)\n\n"+s[b:]
s=s.replace("ct=time.process_time();verify_inputs()","ct=time.process_time();authority=read(P/'PRODUCTION_AUTHORITY.json');assert authority['explicit_authorization'] is True and authority['hard_cap']==21600 and authority['soft_stop']==20000 and authority['deadline_utc']=='2026-10-14T00:00:00Z';verify_inputs()")
s=s.replace("{'hard_cap':90,'soft_stop':75,'charged':10,'controller_reserved':10,'attempts':[]}","{'hard_cap':21600,'soft_stop':20000,'charged':1200,'controller_reserved':1200,'attempts':[]}")
s=s.replace("validate_budget(ledger);reconcile_stale(ledger);admit(ledger,cap,0,0,time.time())","validate_budget(ledger);reconcile_stale(ledger);forecast=production.forecast(ledger,args,cap,time.time(),name in authority.get('authorized_retry_attempts',[]))")
s=s.replace("'test':test}","'test':test,'admission_forecast':forecast,'authority_sha256':digest((P/'PRODUCTION_AUTHORITY.json').read_bytes())}")
s=s.replace("str(P/'whole')","str(SOURCE/'whole')").replace("str(P.parent/'bilayer_whole_m4_pipeline')","str(SOURCE.parent/'bilayer_whole_m4_pipeline')").replace("str(P.parent/'bilayer_brauer_rule_compiler/run')","str(SOURCE.parent/'bilayer_brauer_rule_compiler/run')")
# No self-test modes or implicit production job initialization from CLI.
s=s[:s.index("if __name__=='__main__':")]+'''if __name__=='__main__':
 assert sys.argv[1]!='test','production test mode disabled'
 # Reconcile/adopt every successful but possibly not yet committed output first.
 if (P/'BUDGET_LEDGER.json').exists():
  for old in read(P/'BUDGET_LEDGER.json')['attempts']:
   if old['state']=='complete':adopt_completed(P/'runs'/old['name'])
 out=run(sys.argv[1],int(sys.argv[2]),sys.argv[3:]);adopt_completed(out)
'''
(p/'production_controller.py').write_text(s)
