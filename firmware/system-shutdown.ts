/** Host contract only: hardware GPIO driver and filesystem integration absent. uiShutdownRequest must be
 * a UI-approved shutdown event: a raw END-key press may instead end a call. */
export class SystemShutdown {
 private requested=false;private last:number|undefined;private fault=false
 step(x:{now:number;uiShutdownRequest:boolean;modemStage:string;modemSupplyEnabled:boolean;modemRailV:number;status:boolean;storageFlushed:boolean;hardwareValidated:boolean}){
  if(!Number.isFinite(x.now)||!Number.isFinite(x.modemRailV)||x.modemRailV<0||(this.last!==undefined&&(x.now<this.last||x.now-this.last>100)))this.fault=true
  this.last=x.now
  if(x.uiShutdownRequest)this.requested=true
  const safe=x.modemStage==='off'&&!x.modemSupplyEnabled&&x.modemRailV<.5&&!x.status&&x.storageFlushed
  return {shutdownRequested:this.requested,allowModemOn:!this.requested&&!this.fault,systemOffRequest:this.requested&&!this.fault&&x.hardwareValidated&&safe,fault:this.fault}
 }
}
