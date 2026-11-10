import contextlib
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'bin'))
import research
from science_config import resolve_grid,resolved_science

class Science(unittest.TestCase):
 def grid(self,science=None):
  grid=json.loads((ROOT/'conf/recipe.json').read_text())
  if science is not None: grid['science']=science
  return grid
 def test_default_parity(self):
  s=resolved_science(self.grid())
  self.assertEqual(len(s['configs']),9)
  self.assertTrue(all(v==list(range(1,1001)) for v in s['seeds'].values()))
  self.assertEqual(s['hdbscan'],{'min_samples':list(range(2,20)),'min_cluster_size':list(range(5,50)),'cluster_selection_epsilon':[0.,1.,2.]})
 def test_actual_default_constructor_parity(self):
  import umap
  import hdbscan
  from dimple_representations.hdbscan_runner import estimator_kwargs
  x=np.random.default_rng(31).normal(size=(60,3))
  old=umap.UMAP(n_neighbors=30,min_dist=0,n_components=3,densmap=True,metric='euclidean',random_state=1,n_jobs=1).fit_transform(x).astype(np.float32)
  science=resolved_science(self.grid()); c=next(c for c in science['configs'] if c['config_id']=='n30_d0')
  params={k:v for k,v in c.items() if k!='config_id'};params['random_state']=1
  new=umap.UMAP(**params,n_jobs=1).fit_transform(x).astype(np.float32)
  self.assertEqual(old.tobytes(),new.tobytes())
  old_labels=hdbscan.HDBSCAN(min_samples=2,min_cluster_size=5,cluster_selection_epsilon=0.,cluster_selection_method='eom',core_dist_n_jobs=1).fit_predict(old.astype(np.float64))
  from science_config import hdb_candidates
  candidate=next(hdb_candidates(science))[1]
  new_labels=hdbscan.HDBSCAN(**estimator_kwargs(candidate)).fit_predict(new.astype(np.float64))
  self.assertEqual(old_labels.tobytes(),new_labels.tobytes())
  rows=pd.DataFrame([{'config_id':'n30_d0','candidate_ordinal':1,'number_of_clusters':2,'number_of_noise_points':0,'silhouette':.5},{'config_id':'n30_d0','candidate_ordinal':2,'number_of_clusters':3,'number_of_noise_points':2,'silhouette':.6}])
  rows['status']='success'
  from freeze5_scoring import legacy_dimple_score
  expected,_=legacy_dimple_score(rows,fit_include_noise=True);observed,_=research.score_table(rows)
  np.testing.assert_array_equal(expected.raw_score,observed.sort_values('candidate_ordinal').score)
 def test_baseline_scope(self):
  self.assertEqual(resolved_science(self.grid({'execution':{'n_random_states':2}}))['baseline_config_id'],'n30_d0')
  self.assertIsNone(resolved_science(self.grid({'umap':{'n_components':2}}))['baseline_config_id'])
  self.assertIsNone(resolved_science(self.grid({'backend':'pca'}))['baseline_config_id'])
 def test_reject_unknown_inactive_conflicting(self):
  for science in [{'umap':{'typo':3}},{'execution':{'n_random_states':True}},{'backend':'pca','umap':{}},{'pca':{}},{'backend':'ica','ica':{'retained_components':2,'variance_threshold':.9}},{'hdbscan':{'typo':2}}]:
   with self.subTest(science=science), self.assertRaises(ValueError): resolved_science(self.grid(science))
 def test_frozen_scientific_hashes(self):
  hashes={'conf/recipe.json': 'c7444343111f0bc08de03768f4d0b6d21f33348c712c25260d281af361041f89', 'bin/freeze5_scoring.py': '50aecc32d8483f28d10e27401a3b347b3bf5f5d9d8f4fd5ec60cce2ebd452981'}
  for name,digest in hashes.items(): self.assertEqual(hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),digest)
 def test_exact_vendored_sources(self):
  hashes={'pca_runner.py': '6c8ec4cc080bf5df416e8a3641a952c0cffe38827d9b8355b80803a18da25444', 'ica_runner.py': 'f432a6e0b72f235eacbb931d75e196a65c2cb7d5452b5d04b4c77dafeff6dfa0', 'config.py': 'aa7ba83ea4c38a2d57a2d3c038e24e4ce40b52bd5cd08225bad5b6ca4e81e3ac'}
  hashes['hdbscan_runner.py']='9681958851be153bd5022a4b7bd88bfeaec62a5ee7950b7e58fab8ce6601c80c'
  for name,digest in hashes.items():
   self.assertEqual(hashlib.sha256((ROOT/'bin/dimple_representations'/name).read_bytes()).hexdigest(),digest)
 def test_actual_custom_backends_and_pool(self):
  rng=np.random.default_rng(23)
  latent=rng.laplace(size=(60,2)); x=latent@np.array([[1,.3,2,0],[.2,1,0,2]])
  for backend in ['pca','ica','umap']:
   with self.subTest(backend=backend), tempfile.TemporaryDirectory() as directory:
    previous=Path.cwd(); os.chdir(directory)
    try:
     custom={'backend':backend,'grid_eps':[0,.25],'grid_min_samples':[2,3],'grid_min_cluster_size':[3,5],'hdbscan':{'cluster_selection_method':['eom','leaf'],'metric':['manhattan','cosine'],'alpha':1.2,'max_cluster_size':0,'allow_single_cluster':False,'cluster_selection_persistence':0.0}}
     if backend=='umap':
      custom.update(umap={'n_neighbors':5,'n_components':2,'densmap':False,'metric':'manhattan','spread':1.3,'learning_rate':.8,'repulsion_strength':1.2,'negative_sample_rate':4,'local_connectivity':.5,'set_op_mix_ratio':.8,'random_state':7},execution={'n_random_states':2,'legacy_ensemble_seeds':False})
     else: custom[backend]={'retained_components':2}
     grid=self.grid(custom);grid.update(confirmed=True,input_contract={})
     research.write_json('grid.json',grid); np.save('pixels.npy',x)
     science=resolved_science(grid); cid=science['configs'][0]['config_id']
     manifest={'matrix_shape':list(x.shape),'run_grid_sha256':research.sha('grid.json'),'pixels_sha256':research.sha('pixels.npy'),'grid':grid,'resolved_science':science}
     research.write_json('manifest.json',manifest)
     args=SimpleNamespace(grid='grid.json',recipe=str(ROOT/'conf/recipe.json'),pixels='pixels.npy',config=cid,manifest='manifest.json',start=1,end=len(science['seeds'][cid]))
     research.seeds(args); research.concat(args)
     embedding=np.load(cid+'.embedding.npy')
     self.assertEqual(embedding.shape,(60,4 if backend=='umap' else 2))
     if backend!='umap':
      from dimple_representations.pca_runner import fit_pca
      from dimple_representations.ica_runner import fit_ica
      expected=(fit_pca if backend=='pca' else fit_ica)(x,{'retained_components':2,'variance_threshold':None})['embedding']
      np.testing.assert_allclose(embedding,expected,rtol=1e-12,atol=1e-12)
     else: self.assertEqual(science['seeds'][cid],[7,8])
     args.embedding=cid+'.embedding.npy';args.distances=cid+'.distances.npy';args.ensemble=cid+'.ensemble.json'
     for ms in [2,3]: args.min_samples=ms; research.fit_grid(args)
     pool=research.read_pool([cid],60,research.sha('manifest.json'),science)
     self.assertEqual(len(pool),32); self.assertEqual(set(pool.candidate_ordinal),set(range(1,33)))
     self.assertEqual(set(pool.cluster_selection_method),{'eom','leaf'}); self.assertEqual(set(pool.metric),{'manhattan','cosine'})
     research.score_table(pool)
     # Real damaged output is rejected; restoring it permits repeat validation.
     label=Path(cid+'.ms02.labels.npz'); valid=label.read_bytes();label.write_bytes(b'bad')
     with self.assertRaises(Exception): research.read_pool([cid],60,research.sha('manifest.json'),science)
     label.write_bytes(valid);self.assertEqual(len(research.read_pool([cid],60,research.sha('manifest.json'),science)),32)
    finally: os.chdir(previous)

if __name__=='__main__': unittest.main()
