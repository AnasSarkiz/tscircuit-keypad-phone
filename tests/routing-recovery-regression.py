"""Keep every historically verified V66 copper connection after footprint migration."""
import json
from pathlib import Path
old=json.loads(Path('qualification-routing-recovery/baseline-result.json').read_text())['placed_net_islands']
new=json.loads(Path('output/usb-layered-v66-checks.json').read_text())['placed_net_islands']
def verify(candidate):
    count=0
    for net,groups in old.items():
        for group in groups:
            assert any(set(group)<=set(g) for g in candidate.get(net,[])),(net,group)
            count+=1
    return count
count=verify(new)
bad={net:[list(group) for group in groups]for net,groups in new.items()}
# A deliberately removed copper island must be rejected, not silently ignored.
removed=next(net for net,groups in bad.items()if any(len(set(g))>1 for g in groups));bad[removed]=[]
try:verify(bad)
except AssertionError:pass
else:raise AssertionError('deleted historical copper island accepted')
Path('output/routing-recovery-regression.json').write_text(json.dumps({'historical_v66_islands_preserved':count,'deleted_island_mutation_rejected':True,'release':False},indent=2)+'\n')
print('PASS',count,'historical V66 copper islands retained; deleted-island mutation rejected')
