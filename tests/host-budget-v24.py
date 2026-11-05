import itertools,json,math
from pathlib import Path
rows=[]
for logic,eta,bl,voc,r in itertools.product([.6,.1],[.8,.85,.9],[False,True],[3.6,3.8,4.1],[.05,.1,.2]):
 p=7.6/eta+3.3*logic/.8+(5.3*.131/.75 if bl else 0)
 disc=voc*voc-4*r*p;v=(voc+math.sqrt(disc))/2 if disc>=0 else None;i=p/v if v else None
 rows.append(dict(logic_allocation_A=logic,assumed_efficiency=eta,backlight=bl,OCV_V=voc,assumed_shared_R_ohm=r,power_W=p,SYS_V=v,pack_A=i,conditional_pass=bool(v and v>=3.2 and i<=3.6)))
counts={str(a):sum(x['conditional_pass'] for x in rows if x['logic_allocation_A']==a) for a in [.6,.1]}
assert counts['0.1']>counts['0.6'];assert any(not x['conditional_pass'] for x in rows if x['logic_allocation_A']==.1)
# An entire RGB565 framebuffer exactly consumes SRAM, making it unusable as an architecture.
sram=40*1024;frame=128*160*2;assert frame==sram
alloc={'two_scanline_buffers':2*128*2,'UART_RX_TX':2*2048,'SMS_and_UI_state':8192,'stacks_interrupts':8192,'drivers_and_globals':4096}
headroom=sram-sum(alloc.values());assert headroom>=8192
result={'scope':'Comparison only. 100mA logic is an engineering allocation, NOT a measured or guaranteed STM32 system maximum. Modem 2A at3.8V LTE-only; no transient simulation. Efficiencies, pack resistance and protection remain unqualified.','conditional_pass_counts_of_54':counts,'scenarios':rows,'STM32U083_memory':{'SRAM_bytes':sram,'full_framebuffer_bytes':frame,'candidate_allocations_bytes':alloc,'unallocated_bytes':headroom,'linked_firmware_available':False},'battery_approved':False,'GSM_approved':False,'fabrication_ready':False}
Path('output/host-budget-v24.json').write_text(json.dumps(result,indent=2));print(counts,'SRAM headroom',headroom)
