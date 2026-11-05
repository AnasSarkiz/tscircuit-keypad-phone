import assert from 'node:assert/strict'
import {ChargeQualification} from '../firmware/charge-qualification'
import {unreleasedEvidence,type Evidence,type PowerInputs} from '../firmware/power-policy'
const e:Evidence={lteOnlyVerifiedAcrossReset:true,carrierVoiceVerified:true,powerPathValidated:true,thermalAttachmentValidated:true,usbInputValidated:true}
const i:PowerInputs={source:'3A',usbRailGood:true,regnStable:true,temperatureColdOK:true,temperatureHotOK:true,sensorConnected:true,temperatureC:25,requestCharge:true,requestModem:false,requestBacklight:false,boostRailV:0}
const q=new ChargeQualification()
assert.deepEqual([0,100,200,250].map(t=>q.update(t,e,i)),[false,false,false,true])
assert.equal(q.update(300,e,{...i,source:'1.5A'}),false)
assert.deepEqual([350,450,550,600].map(t=>q.update(t,e,i)),[false,false,false,true])
assert.equal(q.update(701,e,i),false,'stale sample must disable')
assert.equal(q.update(700,e,i),false,'backwards time must disable')
assert.equal(q.update(NaN,e,i),false)
q.reset();for(const t of [0,100,200,300,400])assert.equal(q.update(t,unreleasedEvidence,i),false)
q.reset();for(const t of [0,100,200,300])q.update(t,e,i)
assert.equal(q.update(350,e,{...i,temperatureHotOK:false}),false)
q.reset();assert.equal(q.update(10000,e,i),false,'reset never preserves qualification')
console.log('PASS: charge qualification dwell, stale samples, resets, source downgrade and thermal fault')
