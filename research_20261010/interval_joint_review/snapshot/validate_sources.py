"""Reconstruct the parameter matrix polynomials from original saved moments."""
from certify_joint_extension import *
from filter_rayleigh import input_path

def main():
 rows=[];sources={}
 for model in MODELS:
  nx,ny=model['geometry'];G=model['G'];A=model['first_moment_coefficients'];B=model['full_second_moment_coefficients'];selected=None;raw=[]
  for g in map(F,('3/100','1/25','1/20','3/50','7/100','2/25','1/10')):
   path=input_path(nx,ny,g);r=json.loads(path.read_text());den=r['integer_matrix_denominator']
   gg=np.array(r['gram'],dtype=object);aa=np.array(r['shifted_hamiltonian_numerator'],dtype=object)*F(1,den);bb=np.array(r['shifted_H2_numerator'],dtype=object)*F(1,den*den)
   assert r['s']=='1/2' and r['block_krylov_depth']==1 and F(r['E00'])==-F(3*nx*ny,4)
   if selected is None:selected=r['selected_basis_indices']
   assert r['selected_basis_indices']==selected
   assert np.array_equal(gg,G) and np.array_equal(aa,A[0]+g*A[1]) and np.array_equal(bb,B[0]+g*B[1]+g*g*B[2])
   raw.append((g,aa,bb));sources[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
  g0=F(3,100);h=F(1,100);a1=(raw[1][1]-raw[0][1])/h;a0=raw[0][1]-g0*a1
  b2=(raw[2][2]-2*raw[1][2]+raw[0][2])/(2*h*h);b1=(raw[1][2]-raw[0][2])/h-(2*g0+h)*b2;b0=raw[0][2]-g0*b1-g0*g0*b2
  assert all(np.array_equal(x,y) for x,y in zip(A,[a0,a1])) and all(np.array_equal(x,y) for x,y in zip(B,[b0,b1,b2]))
  # In the fixed basis, Q has the exact indicated q values.
  raw_model=json.loads((AUX/f'matrix_polynomial_{nx}x{ny}.json').read_text());assert selected==raw_model['selected_basis_indices']
  dim=len(G);pair_count=(max(selected)+1)//2;qs=[0 if i==0 else 2 if i<=pair_count else 4 for i in selected]
  assert np.array_equal(A[0],np.diag(qs)@G) and np.array_equal(B[0],np.diag([q*q for q in qs])@G)
  rows.append(dict(geometry=[nx,ny],dimension=dim,source_couplings=[str(g) for g,_,_ in raw],exact_matrix_matches=21,zero_coupling_number_action_verified=True))
 out=dict(status='PASS exact source reconstruction',models=rows,source_sha256=sources,higher_moment_fields_consumed=False,physical_vectors_constructed=False)
 (HERE/'source_validation.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS source matrices',len(sources))
if __name__=='__main__':main()
