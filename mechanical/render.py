"""Orthographic illustration from the actual exported GLB meshes, not a concept image."""
from pathlib import Path
import sys
import numpy as np
import trimesh as tm
p=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]/'output'
scene=tm.load(p/'exploded.glb',force='scene')
assembled=tm.load(p/'assembly.glb',force='scene')
case_bounds=np.array([assembled.geometry[n].bounds for n in ['front_shell','rear_shell']])
case_size=(case_bounds[:,1,:].max(axis=0)-case_bounds[:,0,:].min(axis=0))*1000
case_label=' × '.join(f'{v:g}' for v in case_size)
rot=tm.transformations.rotation_matrix(np.radians(32),[0,0,1])[:3,:3]
rot=tm.transformations.rotation_matrix(np.radians(57),[1,0,0])[:3,:3]@rot
faces=[]
for name in scene.geometry:
 m=scene.geometry[name]
 v=(m.vertices*1000)@rot.T
 col=m.visual.face_colors
 for i,f in enumerate(m.faces):
  pts=v[f]; normal=np.cross(pts[1]-pts[0],pts[2]-pts[0]);norm=np.linalg.norm(normal)
  if norm==0 or normal[2]<=0:continue
  shade=.55+.45*normal[2]/norm
  rgb=(col[i,:3]*shade).astype(int)
  faces.append((pts[:,2].mean(),pts[:,:2],rgb))
allpts=np.concatenate([f[1] for f in faces]);lo=allpts.min(0);hi=allpts.max(0)
scale=min(750/(hi[0]-lo[0]),730/(hi[1]-lo[1]));center=(hi+lo)/2
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="1000"><rect width="1100" height="1000" fill="#f3f5f7"/><text x="40" y="50" font-family="Arial" font-size="28" fill="#243344">ANAS PHONE / Exploded fit model</text><text x="40" y="80" font-family="Arial" font-size="17" fill="#536472">Actual exported geometry • simplified component envelopes • not verified mating</text>']
for depth,pts,rgb in sorted(faces,key=lambda f:f[0]):
 coords=(pts-center)*scale;coords[:,0]+=550;coords[:,1]=500-coords[:,1]
 points=' '.join(f'{x:.2f},{y:.2f}' for x,y in coords)
 s.append(f'<polygon points="{points}" fill="rgb({rgb[0]},{rgb[1]},{rgb[2]})" stroke="rgb({rgb[0]},{rgb[1]},{rgb[2]})" stroke-width="0.5"/>')
s.append(f'<text x="40" y="935" font-family="Arial" font-size="17" fill="#243344">{case_label} mm housing • one rigid main board • separate flexible antenna</text><text x="40" y="965" font-family="Arial" font-size="16" fill="#536472">Amber: battery / antenna. Keycaps, FPC, battery power and RF fit remain provisional.</text></svg>')
(p/'exploded.svg').write_text(''.join(s))
