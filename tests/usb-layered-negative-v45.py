from pathlib import Path
import json,tempfile,subprocess
from concurrent.futures import ThreadPoolExecutor
root=Path.cwd();original=json.loads((root/'routing/usb-layered-v45.json').read_text());out={}
cases=[('debug_boot_open','placed UART endpoint disconnected'),('debug_rx_open','placed UART endpoint disconnected'),('column_bias_open','placed UART endpoint disconnected'),('mcu_bus_via_open','placed translator supply disconnected'),('mcu_host_open','placed UART endpoint disconnected'),('mcu_ep_open','placed ground disconnected'),('antenna_intrusion','antenna_keepout'),('bad_annulus','AssertionError'),('via_pad_short','G_NOR_top'),('split_plane','ground'),('missing_ground_via','placed ground disconnected'),('supply_open','placed supply disconnected'),('translator_bus_open','placed translator supply disconnected'),('modem_gate_open','placed modem control disconnected'),('sim_bypass_open','placed SIM circuit disconnected'),('socket_ground_open','placed ground disconnected'),('fet_gate_open','placed modem control disconnected'),('modem_key_open','placed modem endpoint disconnected'),('modem_sim_open','placed modem endpoint disconnected'),('uart_open','placed UART endpoint disconnected'),('flow_open','placed UART endpoint disconnected'),('status_open','placed UART endpoint disconnected')]
def run_case(case):
 name,expected=case
 c=json.loads(json.dumps(original))
 if name=='debug_boot_open':c['routes']=[r for r in c['routes'] if r['name']!='MCU_DBG_BOOT_PAD']
 if name=='debug_rx_open':c['routes']=[r for r in c['routes'] if r['name']!='MCU_DBG_RX_AUTO']
 if name=='column_bias_open':c['routes']=[r for r in c['routes'] if r['name']!='MCU_DBG_COL0_BIAS_AUTO']
 if name=='mcu_bus_via_open':c['vias']=[v for v in c['vias'] if v['name']!='MCU_VDD_BUS']
 if name=='mcu_host_open':c['routes']=[r for r in c['routes'] if r['name']!='MCU_TX_LONG_AUTO']
 if name=='mcu_ep_open':c['routes']=[r for r in c['routes'] if r['name']!='MCU_EP_ROW1']
 if name=='antenna_intrusion':c['routes'].append(dict(name='BAD_ANTENNA',net='GND',layer='top',width=.15,points=[[-20,42],[-10,42]],pads=[]))
 if name=='status_open':c['routes']=[r for r in c['routes'] if r['name']!='MOD_STATUS_LONG']
 if name=='flow_open':c['routes']=[r for r in c['routes'] if r['name']!='MOD_FLOW_RTS_LONG']
 if name=='uart_open':c['routes']=[r for r in c['routes'] if r['name']!='MOD_UART_RXD_TOP']
 if name=='modem_key_open':c['routes']=[r for r in c['routes'] if r['name']!='MOD_KEY_TOP']
 if name=='modem_sim_open':c['routes']=[r for r in c['routes'] if r['name']!='MOD_SIM_RST_LONG']
 if name=='socket_ground_open':c['routes']=[r for r in c['routes'] if r['name']!='SOCKET_GND']
 if name=='fet_gate_open':c['routes']=[r for r in c['routes'] if r['name']!='KEY_FET_GATE']
 if name=='bad_annulus':c['vias'][0]['drill']=.3
 if name=='via_pad_short':next(v for v in c['vias'] if v['name']=='G_NOR')['xy']=[-8.3,-62.05]
 if name=='split_plane':c['ground_boundary']=[-24,-80.5,0,-60.5]
 if name=='missing_ground_via':c['vias']=[v for v in c['vias'] if v['name']!='G_CC_CAP']
 if name=='sim_bypass_open':c['routes']=[r for r in c['routes'] if r['name']!='SIM_VDD_BYPASS']
 if name=='modem_gate_open':c['routes']=[r for r in c['routes'] if r['name']!='RESET_GATE_DEFAULT']
 if name=='translator_bus_open':c['routes']=[r for r in c['routes'] if r['name']!='MODEM_EXT_TRANSLATOR_BUS']
 if name=='supply_open':c['routes']=[r for r in c['routes'] if r['name']!='AUX_SUPPLY_BRIDGE']
 with tempfile.TemporaryDirectory() as td:
  d=Path(td)
  for sub in ['engineering','routing','output']:(d/sub).mkdir()
  (d/'engineering/usb_layered_v45.py').write_bytes((root/'engineering/usb_layered_v45.py').read_bytes());(d/'routing/usb-layered-v45.json').write_text(json.dumps(c));(d/'output/usb-placement-v45.circuit.json').write_bytes((root/'output/usb-placement-v45.circuit.json').read_bytes())
  p=subprocess.run([str(root/'.venv/bin/python'),str(d/'engineering/usb_layered_v45.py')],capture_output=True,text=True)
  assert p.returncode!=0,name
  assert expected in p.stderr,(name,p.stderr)
  return name,p.stderr.strip().splitlines()[-1]
with ThreadPoolExecutor(max_workers=4) as pool:out=dict(pool.map(run_case,cases))
(root/'output/usb-layered-negative-v45.json').write_text(json.dumps(out,indent=2));print('PASS twenty-two layered-copper mutations rejected',out)
