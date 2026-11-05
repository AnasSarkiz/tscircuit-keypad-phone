import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from engineering.modem_clearance import enforce
rows=json.loads(Path('output/placement-constraints-v10.json').read_text());others=[]
for row in rows:
 if row['side']!='rear' or 'modem' in row['name']:continue
 a,b=row['bounds_mm'];others.append(dict(ref=row['name'],x=(a[0]+b[0])/2,y=(a[1]+b[1])/2,width=b[0]-a[0],height=b[1]-a[1],rotation=0,layer='bottom',verified_body=False))
m=dict(ref='MODEM',x=11.6,y=6,width=25,height=29,rotation=0,layer='bottom')
try:enforce(m,others,[p['ref'] for p in others])
except ValueError as e:reason=str(e)
else:raise AssertionError('Unverified assembly envelopes must not pass')
assert 'unverified body' in reason
Path('output/placement-envelope-v21.json').write_text(json.dumps({'modem':m,'others':others,'status':'BLOCKED','reasons':reason.splitlines(),'scope':'Only existing reserved envelopes; expanded 211-component netlist not placed. Opposite face/3D/antenna constraints excluded.'},indent=2))
print('EXPECTED BLOCK:',reason)
