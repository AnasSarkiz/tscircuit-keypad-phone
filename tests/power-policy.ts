import assert from 'node:assert/strict'
import {powerPolicy,decodeTypeCCurrent,unreleasedEvidence,type PowerInputs,type Evidence} from '../firmware/power-policy'
const good:PowerInputs={source:'3A',usbRailGood:true,regnStable:true,temperatureColdOK:true,temperatureHotOK:true,sensorConnected:true,temperatureC:25,requestCharge:true,requestModem:true,requestBacklight:true,boostRailV:5}
const evidence:Evidence={lteOnlyVerifiedAcrossReset:true,carrierVoiceVerified:true,powerPathValidated:true,thermalAttachmentValidated:true,usbInputValidated:true}
assert.deepEqual(powerPolicy(unreleasedEvidence,good),{chargeRequest:false,modemEnable:false,boostEnable:false,backlightPWM:false})
for(const key of ['lteOnlyVerifiedAcrossReset','carrierVoiceVerified','powerPathValidated'] as const)assert.equal(powerPolicy({...evidence,[key]:false},good).modemEnable,false,key)
for(const source of ['none','default','1.5A'] as const)assert.equal(powerPolicy(evidence,{...good,source}).chargeRequest,false)
for(const key of ['usbRailGood','regnStable','temperatureColdOK','temperatureHotOK','sensorConnected','requestCharge'] as const)assert.equal(powerPolicy(evidence,{...good,[key]:false}).chargeRequest,false,key)
for(const temperatureC of [-40,10,20,34,45,80,NaN,Infinity])assert.equal(powerPolicy(evidence,{...good,temperatureC}).chargeRequest,false)
for(const boostRailV of [0,3.8,4.6,5.4,NaN,Infinity])assert.equal(powerPolicy(evidence,{...good,boostRailV}).backlightPWM,false)
for(const key of ['powerPathValidated','thermalAttachmentValidated','usbInputValidated'] as const)assert.equal(powerPolicy({...evidence,[key]:false},good).chargeRequest,false,key)
assert.equal(powerPolicy(evidence,good).chargeRequest,true)
assert.equal(powerPolicy(evidence,{...good,boostRailV:0}).boostEnable,true)
console.log('Power policy: default-off, LTE evidence, source downgrade, thermal fault and backlight startup checks passed. Host policy only; no hardware safety certification.')

assert.deepEqual([[true,true],[true,false],[false,true],[false,false]].map(([a,b])=>decodeTypeCCurrent(a,b)),['none','default','1.5A','3A'])
