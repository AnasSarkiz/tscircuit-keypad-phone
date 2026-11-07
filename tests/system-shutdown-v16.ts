import assert from 'node:assert/strict'
import {SystemShutdown} from '../firmware/system-shutdown'
const base={now:0,uiShutdownRequest:false,modemStage:'on',modemSupplyEnabled:true,modemRailV:3.8,status:true,storageFlushed:false,hardwareValidated:false}
const s=new SystemShutdown();assert(!s.step(base).systemOffRequest)
let r=s.step({...base,now:50,uiShutdownRequest:true});assert(r.shutdownRequested);assert(!r.allowModemOn);assert(!r.systemOffRequest)
for(const [i,stage] of ['key-off','shutdown','fault','discharge'].entries())assert(!s.step({...base,now:100+i*50,modemStage:stage,hardwareValidated:true}).systemOffRequest)
const off={...base,now:300,modemStage:'off',modemSupplyEnabled:false,modemRailV:0,status:false,storageFlushed:true,hardwareValidated:true}
assert(!s.step({...off,modemRailV:.5}).systemOffRequest)
assert(!s.step({...off,now:350,storageFlushed:false}).systemOffRequest)
assert(!s.step({...off,now:400,hardwareValidated:false}).systemOffRequest)
assert(s.step({...off,now:450}).systemOffRequest)
assert(!s.step({...off,now:700}).systemOffRequest)
assert(!s.step({...off,now:750}).systemOffRequest)
for(const bad of [NaN,Infinity,-1]){const t=new SystemShutdown();assert(!t.step({...off,uiShutdownRequest:true,modemRailV:bad}).systemOffRequest)}
for(const now of [-1,-1000]){
 const t=new SystemShutdown()
 const invalid=t.step({...off,now,uiShutdownRequest:true})
 assert.equal(invalid.fault,true,'negative initial time must fault')
 assert.equal(invalid.systemOffRequest,false,'negative time cannot authorize shutdown')
 assert.equal(invalid.allowModemOn,false)
 const later=t.step({...off,now:0})
 assert.equal(later.fault,true,'clock fault must remain latched')
 assert.equal(later.systemOffRequest,false)
}
console.log('PASS shutdown sequencing gate, latched request, residual rail, storage, unvalidated hardware and stale-input fault; host policy only')
