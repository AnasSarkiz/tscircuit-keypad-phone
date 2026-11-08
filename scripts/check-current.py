"""Reproducible recovered electrical/placement/routing checks, not a factory release.

Run with .venv/bin/python after installing requirements-routing.txt.
Historical mechanical/process stages are documented separately, not silently passed.
"""
import subprocess
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
py=sys.executable
commands=[
 ['npm','run','typecheck'],['npm','run','check:pcb-inputs'],
 ['npm','run','test:jlc-imports'],['npm','run','test:keypad-import'],['npm','run','test:board-imports'],
 ['npm','run','test:logical-phone'],['npm','run','check:public'],['npm','test'],['npm','run','test:power'],
 ['npm','run','test:modem-safety'],
 [py,'-m','unittest','discover','-s','tests','-p','test_modem_clearance_recovery.py','-v'],
 [py,'engineering/usb_layered_v66.py'],
 [py,'-m','unittest','discover','-s','tests','-p','test_routing_source_groups.py','-v'],
 [py,'tests/whole-board-coverage-v66.py'],
 [py,'tests/routing-recovery-regression.py'],
 ['node','--import','tsx','tests/usb-layered-export-v66.ts'],
]
if '--negative' in sys.argv[1:]:commands.append([py,'tests/usb-layered-negative-v66.py'])
if any(arg!='--negative' for arg in sys.argv[1:]):raise SystemExit('Usage: .venv/bin/python scripts/check-current.py [--negative]')
for command in commands:
 print('RUN', ' '.join(command),flush=True)
 subprocess.run(command,cwd=ROOT,check=True)
print('PASS recovered logical, placement and routed-copper checks only. Not full mechanical, process, electrical-safety, RF/carrier or fabrication approval.')
