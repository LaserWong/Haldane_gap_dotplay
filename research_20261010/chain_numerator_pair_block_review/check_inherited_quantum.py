"""Clarify that new exact symmetry claims do not extend to inherited rounded vectors."""
import audit as A
report=[]
def difference(v,w):
 k=next(k for k in sorted(set(v)|set(w)) if v.get(k,0)!=w.get(k,0))
 return dict(packed_state=k,labels=[(k>>(4*i))&15 for i in range(8)],original_coefficient=str(v.get(k,0)),transformed_coefficient=str(w.get(k,0)))
def witness(v):
 k=min(v);return dict(packed_state=k,labels=[(k>>(4*i))&15 for i in range(8)],nonzero_coefficient=str(v[k]))
for name in ['packed_input.txt','packed_old_direction.txt']:
 v=A.A.read_packed(A.OLD/name);v={k:x for k,x in v.items() if x};tr={((k<<4)&0xffffffff)|(k>>28):x for k,x in v.items()};rf={};mz=True
 for k,x in v.items():
  labs=[(k>>(4*i))&15 for i in range(8)];mz=mz and sum(A.A.P.MAG[z] for z in labs)==0;kk=sum(z<<(4*(7-i)) for i,z in enumerate(labs));rf[kk]=x*(-1)**sum(z in [1,2,3] for z in labs)
 up=A.spin(v,'+');dn=A.spin(v,'-');report.append(dict(file=name,magnetization_zero=mz,translation_even=tr==v,reflection_even=rf==v,raising_zero=not up,lowering_zero=not dn,raising_support=len(up),lowering_support=len(dn),translation_counterexample=difference(v,tr),reflection_counterexample=difference(v,rf),raising_counterexample=witness(up),lowering_counterexample=witness(dn)))
assert all(r['magnetization_zero'] and not r['translation_even'] and not r['reflection_even'] and not r['raising_zero'] and not r['lowering_zero'] for r in report)
A.save('inherited_quantum_diagnostic.json',report);print('INHERITED QUANTUM SCOPE CLARIFIED',flush=True)
