"""Nodal corner analysis of the additional temperature window; manufacturer nominal R-T interpolation; tolerance envelope remains unqualified."""
import math,itertools,json,bisect
from pathlib import Path
rt_table=[(-10,42470),(0,27280),(10,17960),(20,12090),(25,10000),(30,8313),(40,5827),(50,4160),(60,3020),(70,2228)]
def nominal_r(t):
 i=max(0,min(len(rt_table)-2,bisect.bisect_right([p[0] for p in rt_table],t)-1));a,b=rt_table[i],rt_table[i+1]
 xa,xb,x=1/(a[0]+273.15),1/(b[0]+273.15),1/(t+273.15)
 return math.exp(math.log(a[1])+(x-xa)/(xb-xa)*math.log(b[1]/a[1]))
for t,r in rt_table:assert abs(nominal_r(t)-r)<1e-8
ranges={'cold':[],'hot':[]};faults=[]
# Independent component corners: sense top/bottom, NTC R/B, threshold top/bottom,
# feedback resistance, input series resistance, comparator offset, rail.
for signs in itertools.product([-1,1],repeat=11):
 a,b,c,d,e,f,g,h,j,k,l=signs
 rt=5300*(1+a*.0035);rp=31140*(1+b*.0035)
 r25=10000*(1+c*.01);beta=3435*(1+d*.01)
 rf=10e6*(1+g*.02);rfc=10e6*(1+l*.02);ri=10000*(1+h*.0035)
 rail=4.58 if k<0 else 4.8;offset=j*.002/rail
 for coldout,hotout in itertools.product([0,1],repeat=2):
  cref=(1/(60400*(1+e*.0035))+coldout/rfc)/(1/(60400*(1+e*.0035))+1/(100000*(1+f*.0035))+1/rfc)
  href=100000*(1+f*.0035)/(93100*(1+e*.0035)+100000*(1+f*.0035))
  def nodes(r):
   vs=(1/rt+hotout/(ri+rf))/(1/rt+1/rp+(0 if math.isinf(r) else 1/r)+1/(ri+rf)) if r else 0
   hs=(vs/ri+hotout/rf)/(1/ri+1/rf)
   return vs,hs
  def diff(t,which):
   r=nominal_r(t)*(r25/10000)*math.exp((beta-3435)*(1/(t+273.15)-1/298.15));vs,hs=nodes(r)
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
report={'corner_sets':2048,'output_states_per_corner':4,'trip_ranges_C':{k:[min(v),max(v)] for k,v in ranges.items()},'open_short_fault_checks':'passed every corner/output state','source':'https://www.semitec-global.com/uploads/2022/01/P12-13-AT-Thermistor.pdf','nominal_RT_table_ohms':rt_table,'scope':'Nominal table with log-R/inverse-temperature interpolation; not a manufacturer-guaranteed full R-T tolerance envelope. R25/B perturbation approximation and 0.35% precision and2% hysteresis-resistor allowances including100C drift; precision candidates assigned V12; aging remains unbounded; not supplier full R-T bound or thermal-attachment proof. No power-on-reset claim.','release':False,'blocker':'CHARGE_REQUEST remains unqualified and off. Need source qualification, rail-good startup gate, precise R-T curve and physical thermal lag/gradient.'}
assert min(ranges['cold'])>15 and max(ranges['hot'])<40
Path('output/thermal-v56-checks.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
