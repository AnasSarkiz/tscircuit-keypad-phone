import {powerPolicy,type Evidence,type PowerInputs} from './power-policy'
/** Host sequencing only; not a replacement for independent thermal hardware.
 * Caller must poll at <=100 ms and reset this object after host reset.
 * Untrusted timestamps never enable charging; release remains false by default.
 */
export class ChargeQualification {
 private last:number|null=null
 private since:number|null=null
 private samples=0
 private enabled=false
 reset(){this.last=null;this.since=null;this.samples=0;this.enabled=false}
 update(nowMs:number,e:Evidence,i:PowerInputs){
  const timingOK=Number.isFinite(nowMs)&&nowMs>=0&&(this.last===null||(nowMs>this.last&&nowMs-this.last<=100))
  const eligible=timingOK&&powerPolicy(e,i).chargeRequest
  if(!eligible){this.since=null;this.samples=0;this.enabled=false}
  else {this.since??=nowMs;this.samples++;this.enabled=this.samples>=3&&nowMs-this.since>=250}
  this.last=Number.isFinite(nowMs)&&nowMs>=0?nowMs:null
  return this.enabled
 }
}
