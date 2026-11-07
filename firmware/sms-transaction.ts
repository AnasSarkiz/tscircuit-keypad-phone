// Conservative one-part, basic ASCII SMS transaction for a future serialized AT
// transport. Firmware/profile must confirm command support. Never auto-retry
// after submitting Ctrl-Z: a timeout can mean sent with a lost acknowledgement.
export class SmsTransaction {
 state:'idle'|'mode'|'charset'|'prompt'|'result'|'sent'|'failed'|'unknown'='idle'
 private body='';private recipient='';private deadline=0;private refSeen=false
 private lastTime:number|undefined
 private active(){return ['mode','charset','prompt','result'].includes(this.state)}
 // Check time on every event, not just on periodic ticks: an event at the
 // deadline is late. Invalid or backwards time fails closed. After submission
 // the delivery outcome is unknown, not failed, and must never auto-retry.
 private expire(now:number):string[]|null {
  if(!this.active())return null
  const invalid=!Number.isFinite(now)||now<0||(this.lastTime!==undefined&&now<this.lastTime)
  if(!invalid)this.lastTime=now
  if(!invalid&&now<this.deadline)return null
  if(this.state==='result'){this.state='unknown';return []}
  const cancel=this.state==='prompt';this.state='failed';return cancel?['\x1b']:[]
 }
 start(number:string,body:string,now:number):string[]{
  if(this.active())throw new Error('transaction busy')
  if(!Number.isFinite(now)||now<0||(this.lastTime!==undefined&&now<this.lastTime))throw new Error('invalid transaction clock')
  // Deliberately excludes GSM extension alphabet, control codes and Unicode.
  if(!/^\+?[0-9]{1,20}$/.test(number)||!/^[A-Za-z0-9 .,!?():;=+\-]{1,160}$/.test(body))throw new Error('unsupported recipient or SMS alphabet')
  this.lastTime=now;this.recipient=number;this.body=body;this.refSeen=false;this.state='mode';this.deadline=now+5000
  return ['AT+CMGF=1\r']
 }
 line(line:string,now:number):string[]{
  const expired=this.expire(now);if(expired!==null)return expired
  const s=line.trim()
  if(this.active()&&(/^(ERROR|\+CMS ERROR:|\+CME ERROR:)/.test(s))){this.state='failed';return []}
  if(this.state==='mode'&&s==='OK'){this.state='charset';this.deadline=now+5000;return ['AT+CSCS="GSM"\r']}
  if(this.state==='charset'&&s==='OK'){this.state='prompt';this.deadline=now+5000;return [`AT+CMGS="${this.recipient}"\r`]}
  if(this.state==='result'&&/^\+CMGS:\s*\d+$/.test(s))this.refSeen=true
  if(this.state==='result'&&s==='OK'&&this.refSeen)this.state='sent'
  return []
 }
 // A UART parser must identify the un-terminated '>' prompt independently of lines.
 prompt(now:number):string[]{
  const expired=this.expire(now);if(expired!==null)return expired
  if(this.state!=='prompt')return []
  this.state='result';this.deadline=now+120000;return [this.body+'\x1a']
 }
 tick(now:number):string[]{return this.expire(now)??[]}
}
