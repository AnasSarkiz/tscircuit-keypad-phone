import assert from 'node:assert/strict'
import {ModemSequencer,Sample} from '../firmware/modem-sequencer'
// Reach states through the public contract, never by modifying private timers.
function reach(target:'key-off'|'shutdown'){
 const q=new ModemSequencer();let t=0
 const x:Sample={now:0,requestOn:true,releaseApproved:true,vbatt:0,status:false,atReady:false,shutdownConfirmed:false,railsValid:false}
 const tick=(patch:Partial<Sample>={})=>q.step(Object.assign(x,patch,{now:t+=50}))
 tick();let out=tick({vbatt:3.8,railsValid:true})
 for(let i=0;i<200&&out.stage!=='boot';i++)out=tick()
 assert.equal(out.stage,'boot');assert.equal(tick({status:true,atReady:true}).stage,'on')
 out=tick({requestOn:false});assert.equal(out.stage,'key-off')
 if(target==='shutdown')for(let i=0;i<100&&out.stage!=='shutdown';i++)out=tick()
 assert.equal(out.stage,target);return tick
}
for(const phase of ['key-off','shutdown'] as const){
 for(const fault of [{railsValid:false},{vbatt:3.29},{vbatt:NaN},{releaseApproved:false}]){
  const tick=reach(phase);const out=tick(fault)
  assert.equal(out.stage,'fault');assert.equal(out.pwrkeyLow,false);assert.equal(out.resetLow,false);assert.equal(out.supplyEnable,true)
  assert.equal(tick({railsValid:true,vbatt:3.8,releaseApproved:true,status:false,shutdownConfirmed:true}).stage,'fault')
 }
}
console.log('PASS eight shutdown fault cases: release key, preserve prior supply, latch fault; no claim of hardware brownout control')
