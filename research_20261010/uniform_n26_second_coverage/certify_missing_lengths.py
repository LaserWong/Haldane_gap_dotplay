#!/usr/bin/env python3
import certify as c
c.resource.setrlimit(c.resource.RLIMIT_CPU,(30,30))
F=c.F;P=c.P;start=c.time.process_time();z=c.json.loads(c.read(P/'certificate.json'))['zero_gap_window'];s=F(z['S']);t=F(z['T']);K=c.down(s*s*t);assert K>F(1,2);w=(1+c.root(2*K-1,2)[0])/2;rho=(1-w)/w;d=c.down(t/(1+rho*rho));gap=F(23,10000);beta=F(49,4);rows=[]
for L in [26,27]:
 p=F(L,26);base=c.down(c.power(s,2-p)[0]*c.power(d,p/2)[0]);factor=1-c.power(rho,p)[1] if L%2 else F(1);C=c.down(base*factor);margin=C-c.expi(beta*gap)[1]*(1-C);assert C>F(1,2) and margin>0
 rows.append({'L':L,'p':str(p),'parity':'odd_signed_tail' if L%2 else 'even_nonnegative_tail','base_lower':str(base),'factor_lower':str(factor),'purity_lower':str(C),'gap':str(gap),'margin':str(margin)})
old=P.parent/'uniform_n28_second_initialization';assert c.hashlib.sha256(c.read(old/'MANIFEST_SHA256.json')).hexdigest()=='66c710bfc302c3f6a220a3162d933add710bfe51aef6fbcf1e256d6725430b55';r=c.json.loads(c.read(old/'certificate.json'))['combined_claim'];assert r['all_integer_L_at_least']==28 and F(r['gap'])>=gap and r['bootstrap_initialization']==30
c.read(P.parent/'root_review/FINITE_WINDOW_INTERPOLATION.md')
out={'status':'EXACT_PRODUCER_LENGTH_RESOLVED_PASS_REVIEW_REQUIRED','n':26,'beta':str(beta),'S':str(s),'T':str(t),'K':str(K),'w_lower':str(w),'rho_upper':str(rho),'D_lower':str(d),'rows':rows,'combined_claim':{'gap':str(gap),'all_integer_L_at_least':26,'unique_ground_state':True,'bootstrap_initialization':30,'coverage_onset':26,'union':['26 and27 length-resolved certificates','28..infinity inherited coverage']},'resource':{'cpu_seconds':c.time.process_time()-start,'peak_kib':c.resource.getrusage(c.resource.RUSAGE_SELF).ru_maxrss,'cpu_limit':30}}
(P/'length_resolved_certificate.json').write_text(c.json.dumps(out,indent=2)+'\n');(P/'LENGTH_INPUT_SHA256.json').write_text(c.json.dumps(c.inputs,indent=2)+'\n');print(out['combined_claim']);print([(x['L'],float(F(x['purity_lower'])),float(F(x['margin']))) for x in rows]);print(out['resource'])
