/** Host-side safety policy. No hardware drivers or LTE disable command inferred. */
export type Evidence={lteOnlyVerifiedAcrossReset:boolean;carrierVoiceVerified:boolean;powerPathValidated:boolean;thermalAttachmentValidated:boolean;usbInputValidated:boolean}
export type PowerInputs={source:'none'|'default'|'1.5A'|'3A';usbRailGood:boolean;regnStable:boolean;temperatureColdOK:boolean;temperatureHotOK:boolean;sensorConnected:boolean;temperatureC:number;requestCharge:boolean;requestModem:boolean;requestBacklight:boolean;boostRailV:number}
export function powerPolicy(e:Evidence,i:PowerInputs){
 const usb=i.source==='3A'&&i.usbRailGood&&e.usbInputValidated
 const temp=i.sensorConnected&&i.temperatureColdOK&&i.temperatureHotOK&&Number.isFinite(i.temperatureC)&&i.temperatureC>=21&&i.temperatureC<=33
 return {
  chargeRequest:e.powerPathValidated&&usb&&i.regnStable&&temp&&e.thermalAttachmentValidated&&i.requestCharge,
  modemEnable:e.lteOnlyVerifiedAcrossReset&&e.carrierVoiceVerified&&e.powerPathValidated&&i.requestModem,
  boostEnable:e.powerPathValidated&&i.requestBacklight,
  backlightPWM:e.powerPathValidated&&i.requestBacklight&&Number.isFinite(i.boostRailV)&&i.boostRailV>=4.7&&i.boostRailV<=5.3,
 }
}
export const unreleasedEvidence:Evidence={lteOnlyVerifiedAcrossReset:false,carrierVoiceVerified:false,powerPathValidated:false,thermalAttachmentValidated:false,usbInputValidated:false}

export type CCDetector='HUSB320-BA000'|'FUSB303B'
export function decodeTypeCCurrent(out1:boolean,out2:boolean,detector:CCDetector='HUSB320-BA000'):PowerInputs['source'] {
 return out1?(out2?(detector==='FUSB303B'?'default':'none'):(detector==='FUSB303B'?'none':'default')):(out2?'1.5A':'3A')
}
/** GPIO decoding cannot establish valid power or completed initialization. */
export function qualifiedTypeCCurrent(out1:boolean,out2:boolean,detector:CCDetector,powerGood:boolean,initializationVerified:boolean):PowerInputs['source'] {
 return powerGood&&initializationVerified?decodeTypeCCurrent(out1,out2,detector):'none'
}
