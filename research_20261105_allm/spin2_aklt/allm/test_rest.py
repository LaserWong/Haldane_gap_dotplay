import os; os.environ["CASES"]="rest"
import json, test_opineq as T
res=[]
for (S,Js,n,m,c,neg) in [(1,[2],5,6,[1,.2,.2,1],1),(1,[2],5,5,[1,.2,.2,1],1),(2,[3,4],5,6,[1,.2,.2,1],1),(2,[3,4],4,7,[3,4,3],0),(2,[3,4],5,7,[4,6,6,4],0)]:
    r=T.test(S,Js,n,m,c); r['negctl']=bool(neg); print(json.dumps(r),flush=True); res.append(r)
json.dump(res,open('test_opineq_rest.json','w'),indent=1)
