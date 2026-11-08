/** Executable timing contract, not flashed firmware. Inputs must be measured by
 * qualified hardware; no current prototype provides all of them. Standard
 * Hardware Design V1.1 corroborates the key dwell values, but exact SKU/revision
 * applicability remains a release gate. Modem USB is disconnected in the current
 * board: its late-USB startup timing is not modeled here. See
 * qualification-modem-supply/ before integrating USB. */
export type Stage='off'|'settle'|'key-on'|'boot'|'on'|'key-off'|'shutdown'|'discharge'|'fault'
export interface Sample {now:number;requestOn:boolean;releaseApproved:boolean;vbatt:number;status:boolean;atReady:boolean;shutdownConfirmed:boolean;railsValid:boolean}
export class ModemSequencer {
 stage:Stage='off'; private since=0; private last:number|undefined; private stableSince:number|undefined; private supply=false
 private enter(s:Stage,t:number){this.stage=s;this.since=t;this.stableSince=undefined}
 step(x:Sample){
  const invalid=!Number.isFinite(x.now)||x.now<0||!Number.isFinite(x.vbatt)||x.vbatt<0||x.vbatt>4.3|| (this.last!==undefined&&(x.now<this.last||x.now-this.last>100))
  this.last=x.now
  // Fault releases PWRKEY but preserves the previous supply state. Never
  // silently interrupt an operating modem merely because software timed out.
  if(invalid||(!x.releaseApproved&&this.stage!=='off'&&this.stage!=='discharge'))this.enter('fault',x.now)
  switch(this.stage){
   case 'off':
    this.supply=false
    if(x.requestOn&&x.releaseApproved&&x.vbatt<0.5&&!x.status&&!x.atReady){this.supply=true;this.enter('settle',x.now)}break
   case 'settle':
    // A modem already showing activity must not have its supply cut or receive
    // another startup key pulse. Preserve supply and require diagnosis.
    // Check the original settle deadline before enter() can reset its timer.
    if(x.status||x.atReady||x.now-this.since>10000){this.enter('fault',x.now);break}
    if(!x.requestOn){this.supply=false;this.enter('discharge',x.now);break}
    if(x.railsValid&&x.vbatt>=3.3&&x.vbatt<=4.3){
     this.stableSince??=x.now
     if(x.now-this.stableSince>=2100)this.enter('key-on',x.now)
    }else this.stableSince=undefined
    break
   case 'key-on':
    if(!x.railsValid||x.vbatt<3.3)this.enter('fault',x.now)
    else if(x.now-this.since>=2100)this.enter('boot',x.now)
    break
   case 'boot':
    if(!x.railsValid||x.vbatt<3.3)this.enter('fault',x.now)
    else if(x.now-this.since>60000)this.enter('fault',x.now)
    else if(x.status&&x.atReady)this.enter('on',x.now)
    break
   case 'on':
    if(!x.status||!x.railsValid||x.vbatt<3.3)this.enter('fault',x.now)
    else if(!x.requestOn)this.enter('key-off',x.now)
    break
   case 'key-off':
    if(!x.railsValid||x.vbatt<3.3)this.enter('fault',x.now)
    else if(x.now-this.since>=3100)this.enter('shutdown',x.now);break
   case 'shutdown':
    if(!x.railsValid||x.vbatt<3.3)this.enter('fault',x.now)
    else if(x.now-this.since>60000)this.enter('fault',x.now)
    else if(!x.status&&x.shutdownConfirmed){this.supply=false;this.enter('discharge',x.now)}
    break
   case 'discharge': if(x.vbatt<0.5&&!x.status)this.enter('off',x.now);break
   case 'fault': break // requires external diagnosis; no blind auto-restart
  }
  return {stage:this.stage,supplyEnable:this.supply,pwrkeyLow:this.stage==='key-on'||this.stage==='key-off',resetLow:false}
 }
}
// RESET_N >=100ms exists in hardware document, but automated reset intentionally
// unavailable until board rails, module firmware and recovery have been tested.
