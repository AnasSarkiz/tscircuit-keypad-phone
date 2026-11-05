"""Nodal corner analysis of the additional temperature window; beta-model only."""
import math,itertools,json
from pathlib import Path
ranges={'cold':[],'hot':[]};faults=[]
# Independent component corners: sense top/bottom, NTC R/B, threshold top/bottom,
# feedback resistance, input series resistance, comparator offset, rail.
for signs in itertools.product([-1,1],repeat=11):
 a,b,c,d,e,f,g,h,j,k,l=signs
 rt=5300*(1+a*.001);rp=31140*(1+b*.001)
 r25=10000*(1+c*.01);beta=3435*(1+d*.01)
 rf=10e6*(1+g*.01);rfc=10e6*(1+l*.01);ri=10000*(1+h*.001)
 rail=4.58 if k<0 else 4.8;offset=j*.002/rail
 for coldout,hotout in itertools.product([0,1],repeat=2):
  cref=(1/(60400*(1+e*.001))+coldout/rfc)/(1/(60400*(1+e*.001))+1/(100000*(1+f*.001))+1/rfc)
  href=100000*(1+f*.001)/(93100*(1+e*.001)+100000*(1+f*.001))
  def nodes(r):
   vs=(1/rt+hotout/(ri+rf))/(1/rt+1/rp+(0 if math.isinf(r) else 1/r)+1/(ri+rf)) if r else 0
   hs=(vs/ri+hotout/rf)/(1/ri+1/rf)
   return vs,hs
  def diff(t,which):
   r=r25*math.exp(beta*(1/(t+273.15)-1/298.15));vs,hs=nodes(r)
   return (vs-cref if which=='cold' else hs-href)+offset
  for which in ranges:
   lo,hi=-10,70
   for _ in range(30):
    mid=(lo+hi)/2
    if diff(mid,which)>0:lo=mid
    else:hi=mid
   ranges[which].append((lo+hi)/2)
  # Even for worst previous comparator output states, open must fail cold;
  # short must fail hot. Does not cover a detached but intact sensor.
  vs,hs=nodes(math.inf);assert vs>cref+abs(offset)
  vs,hs=nodes(0);assert hs<href-abs(offset)
report={'corner_sets':2048,'output_states_per_corner':4,'trip_ranges_C':{k:[min(v),max(v)] for k,v in ranges.items()},'open_short_fault_checks':'passed every corner/output state','scope':'Beta approximation and selected electrical tolerances only; not supplier full R-T bound or thermal-attachment proof. No power-on-reset claim.','release':'CHARGE_REQUEST remains unqualified and off. Need source qualification, rail-good startup gate, precise R-T curve and physical thermal lag/gradient.'}
assert min(ranges['cold'])>15 and max(ranges['hot'])<40
Path('output/thermal-v5-checks.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
