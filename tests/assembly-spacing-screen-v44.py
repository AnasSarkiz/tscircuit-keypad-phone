"""Advisory supplier spacing screen of provisional body envelopes, not exact pad/courtyard DFM."""
import json,itertools
from pathlib import Path
from shapely.geometry import box
rows=json.load(open('output/usb-placement-v44/fit-check.json'))['entries']
def category(m):
 if m.startswith(('RC0603','RT0603','C0603')):return '0603'
 if m in ['TPS3808G01DBVR','TPS70933DBVR','SN74LVC1G02DBVR','SN74AXC1T45DBVR','SN74LVC1G17DBVR','AO3400A','TPD3E001DRLR']:return 'SOT'
 if m in ['TPD6S300ARUKR','TPS259470LRPWR']:return 'QFN'
 return None
limits={('0603','0603'):.18,('0603','SOT'):.2,('SOT','SOT'):.4,('0603','QFN'):1,('QFN','SOT'):1,('QFN','QFN'):1}
viol=[];count=0
for a,b in itertools.combinations(rows,2):
 ca,cb=category(a['MPN']),category(b['MPN'])
 if a['side']!=b['side'] or ca is None or cb is None:continue
 limit=limits.get((ca,cb),limits.get((cb,ca)));count+=1
 def geom(r):
  x,y,_=r['center_mm'];w,h,_=r['body_mm'];return box(x-w/2,y-h/2,x+w/2,y+h/2)
 gap=geom(a).distance(geom(b))
 if gap<limit-1e-8:viol.append({'a':a['reference'],'b':b['reference'],'gap_mm':gap,'screen_min_mm':limit})
out={'source':'https://jlcpcb.com/help/article/minimum-spacing-for-smd-components','source_updated':'2026-09-09','covered_pairs':count,'advisory_spacing_deficits':viol,'unclassified_components':[r['reference'] for r in rows if category(r['MPN']) is None],'limitations':['Provisional conservative body envelopes only; exact manufacturer component/courtyard/pad geometry not qualified.','Supplier measurement-method image returned HTTP 403 to local fetch; no claim of reproducing its measurement convention.','These are screening deficits requiring exact-layout review, not proof a factory will reject the board.'],'factory_approval':False,'release':False}
Path('output/assembly-spacing-screen-v44.json').write_text(json.dumps(out,indent=2));print('Advisory spacing screen:',count,'pairs;',len(viol),'deficits',viol)
