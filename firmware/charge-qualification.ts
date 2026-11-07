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
 private clockFault=false
 private observed:number|null=null
 reset(){this.last=null;this.since=null;this.samples=0;this.enabled=false;this.clockFault=false;this.observed=null}
 private disable(){this.since=null;this.samples=0;this.enabled=false}
 /** Must be called by a running scheduler between samples. This cannot turn off
  * hardware when the processor or scheduler itself is stopped. */
 checkFresh(nowMs:number){
  if(!Number.isFinite(nowMs)||nowMs<0||(this.observed!==null&&nowMs<this.observed))this.clockFault=true
  if(!this.clockFault)this.observed=nowMs
  if(this.clockFault||this.last===null||nowMs-this.last>100)this.disable()
  return this.enabled
 }
 /** sampledAtMs is the acquisition time of a NEW sensor/USB sample, in the
  * same monotonic clock domain as nowMs. A caller must not relabel cached data. */
 update(nowMs:number,e:Evidence,i:PowerInputs,sampledAtMs:number){
  if(!Number.isFinite(nowMs)||nowMs<0||!Number.isFinite(sampledAtMs)||sampledAtMs<0||sampledAtMs>nowMs||(this.observed!==null&&nowMs<this.observed)||(this.last!==null&&sampledAtMs<=this.last))this.clockFault=true
  const timingOK=!this.clockFault&&nowMs-sampledAtMs<=100&&(this.last===null||sampledAtMs-this.last<=100)
  const eligible=timingOK&&powerPolicy(e,i).chargeRequest
  if(!eligible)this.disable()
  else {this.since??=sampledAtMs;this.samples++;this.enabled=this.samples>=3&&sampledAtMs-this.since>=250}
  if(!this.clockFault){this.last=sampledAtMs;this.observed=nowMs}
  return this.enabled
 }
}
