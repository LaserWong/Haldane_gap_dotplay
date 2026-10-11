from pathlib import Path
H=Path(__file__).resolve().parent
s=(H/'snapshot/PREVIOUS_independent_matrix.cpp').read_text()
for a,b in [
 ('Matrix pp{},tt{},cmcm{},comm{},ttzero{};','Matrix pp{},tt{},cmcm{},comm{},ttzero{},r44{},r4cm{},r66{},r6m6{},m66{};'),
 ('for(int k=0;k<3;k++)add(p[k],cm[k],1);gram_contract(pp','gram_contract(r44,p,p,a4);gram_contract(r4cm,p,cm,a4);for(int k=0;k<3;k++)add(p[k],cm[k],1);gram_contract(pp'),
 ('cr=image_CR(st);bool active=false;','cr=image_CR(st);gram_contract(r66,cr,cr,a6);gram_contract(r6m6,cr,t,a6);gram_contract(m66,t,t,a6);bool active=false;'),
 ('emit(out,"TT_on_M_zero",ttzero,6,!limit);','emit(out,"TT_on_M_zero",ttzero,6,!limit);emit(out,"R4R4",r44,4,!limit);emit(out,"R4CM",r4cm,4,!limit);emit(out,"R6R6",r66,6,!limit);emit(out,"R6M6",r6m6,6,!limit);emit(out,"M6M6",m66,6,!limit);')]:
 assert s.count(a)==1;s=s.replace(a,b)
(H/'independent_split.cpp').write_text(s)
