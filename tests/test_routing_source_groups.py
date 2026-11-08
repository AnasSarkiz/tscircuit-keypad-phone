"""Fast fail-closed regressions for recovered routing's physical-port net resolver."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
class RoutingSourceGroups(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original=json.loads((ROOT/'output/usb-placement-v66.circuit.json').read_text())
    def rejected(self, mutate, diagnostic):
        records=copy.deepcopy(self.original);mutate(records)
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for folder in ('engineering','routing','output'):(root/folder).mkdir()
            (root/'engineering/usb_layered_v66.py').write_bytes((ROOT/'engineering/usb_layered_v66.py').read_bytes())
            (root/'routing/usb-layered-v66.json').write_bytes((ROOT/'routing/usb-layered-v66.json').read_bytes())
            (root/'output/usb-placement-v66.circuit.json').write_text(json.dumps(records))
            result=subprocess.run([sys.executable,str(root/'engineering/usb_layered_v66.py')],capture_output=True,text=True,timeout=60)
        self.assertNotEqual(result.returncode,0)
        self.assertIn(diagnostic,result.stderr)
    def test_cross_component_internal_group_is_rejected(self):
        def mutate(j):
            mcu=next(x for x in j if x['type']=='source_component' and x['name']=='U_MCU')
            other=next(x for x in j if x['type']=='source_port' and x['source_component_id']!=mcu['source_component_id'])
            mcu['internally_connected_source_port_ids'][0].append(other['source_port_id'])
        self.rejected(mutate,'invalid internal terminal group')
    def test_conflicting_nets_on_repeated_pad_are_rejected(self):
        def mutate(j):
            mcu=next(x for x in j if x['type']=='source_component' and x['name']=='U_MCU')
            signal=next(x for x in j if x['type']=='source_net' and x['name']=='VLOGIC_3V15')
            j.append({'type':'source_trace','source_trace_id':'MUTATED_CONFLICT','connected_source_port_ids':[mcu['internally_connected_source_port_ids'][0][-1]],'connected_source_net_ids':[signal['source_net_id']]})
        self.rejected(mutate,'conflicting source net assignments')
    def test_unmapped_copper_is_rejected(self):
        def mutate(j):next(x for x in j if x['type']=='pcb_smtpad')['pcb_port_id']=None
        self.rejected(mutate,'unmapped physical port')
if __name__=='__main__':unittest.main()
