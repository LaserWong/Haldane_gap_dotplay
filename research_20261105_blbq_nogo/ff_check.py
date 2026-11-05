"""Discriminator: is KHH(alpha) frustration-free (GM/Knabe hypothesis)? NUMERICAL ED + PROVED structural argument in LOCAL_GAP_PLAN.md"""
import sys,json,numpy as np; sys.path.insert(0,'../spin2_aklt'); from ed import bond
for a in [1,0.95,0.9]:
    w,v=np.linalg.eigh(bond('KHH',a)); e8=json.load(open(f'../spin2_aklt/ed_KHH_{a if a!=1 else 1}_3-8.json'))['8']['E0_per_site']
    print(a,'bond spectrum',np.round(np.unique(np.round(w,6)),4),'bond min',round(w.min(),4),'E0/site L=8 periodic',round(e8,5),'frustration per bond',round(e8-w.min(),4))
