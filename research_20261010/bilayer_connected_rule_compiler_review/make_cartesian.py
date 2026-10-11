from pathlib import Path
p=Path(__file__).parent;s=p.parent/'bilayer_connected_rule_compiler'
x=(s/'fixture_snapshot.cpp').read_text()
a=x.index('V C(const V&v)');b=x.index('V K(const V&v)')
x=x[:a]+'''// Independent Cartesian local actions: delta creation/annihilation; swap minus delta contraction.
V cart(const V&v,int op){V out;for(auto [s,x]:v)for(auto e:edges){int a=s>>(2*e.a)&3,b=s>>(2*e.b)&3;uint32_t base=s&~((3u<<(2*e.a))|(3u<<(2*e.b)));auto put=[&](int c,int d,int f){add(out,base|(uint32_t(c)<<(2*e.a))|(uint32_t(d)<<(2*e.b)),I(x)*e.w*f);};if(op==0){if(a&&a==b)put(0,0,1);}else if(op==1){if(!a&&!b)for(int c=1;c<4;c++)put(c,c,1);}else if(bool(a)!=bool(b))put(b,a,1);else if(a&&b){put(b,a,1);if(a==b)for(int c=1;c<4;c++)put(c,c,-1);}}maxstates=max(maxstates,out.size());return out;}
V C(const V&v){return cart(v,0);}V Cd(const V&v){return cart(v,1);}V D(const V&v){return cart(v,2);}
''' +x[b:]
a=x.index('V pairadd(');b=x.index('void graph(',a)
x=x[:a]+'''V pairadd(V v,int a,int b){V z;for(auto[s,x]:v){assert(!((s>>(2*a))&3)&&!((s>>(2*b))&3));for(int c=1;c<4;c++)add(z,s|(uint32_t(c)<<(2*a))|(uint32_t(c)<<(2*b)),x);}return z;}
'''+x[b:]
(p/'cartesian_fixture.cpp').write_text(x)
old=(s/'PROOF.md').read_text().replace('15·7·13·19','10·7·13·19')
import hashlib,json
h=hashlib.sha256(old.encode()).hexdigest();assert h=='3e5e589be090f6fab992b2e35423c61da7e8e834cdb4901d2fa5f9e2936c82d5'
m=(s/'MANIFEST_SHA256.json').read_text().replace('7c7c83fff5f6bd9b6f2ac642ec6fcc68d98d7c8881dc1c0fed78af393131af6a',h)
assert hashlib.sha256(m.encode()).hexdigest()=='ca4e1e0ae113d6e2fea60e694fa5e6735443f4e688a6168b39c8f758977c6d19'
print('Original announced seal independently reconstructed; only documented proof bound and its manifest entry changed.')
