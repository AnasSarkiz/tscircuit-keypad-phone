"""Run current checks; archive preservation test needs the delivered V65 ZIP."""
import subprocess,sys
from pathlib import Path
py=sys.executable
commands=[[py,'scripts/restore-fixtures.py'],['npx','tsx','tests/usb-placement-v66.tsx'],[py,'mechanical/usb_placement_v66.py'],[py,'engineering/usb_layered_v66.py'],[py,'mechanical/usb_layered_fit_v66.py'],[py,'tests/manufacturing-v66.py'],[py,'tests/factory-screen-v66.py'],[py,'tests/factory-candidate-v66.py'],[py,'tests/mask-track-screen-v66.py'],[py,'tests/mcu-courtyard-v66.py'],[py,'tests/whole-board-coverage-v66.py'],[py,'tests/coverage-regression-v66.py'],[py,'tests/usb-layered-negative-v66.py'],['npx','tsx','tests/usb-layered-export-v66.ts']]
for cmd in commands:subprocess.run(cmd,check=True)
print('PASS current nominal checks; physical/electrical/RF/carrier/factory qualification remains open')
