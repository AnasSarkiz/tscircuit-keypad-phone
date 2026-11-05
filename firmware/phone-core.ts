// Host-tested logic prototype, not flashed ESP32 firmware. No transport or
// GPIO drivers. Deliberate single-key policy prevents matrix ghosting actions.
export class KeyDebouncer {
  private candidate: string|null=null
  private since=0
  private latched: string|null=null
  private chordBlocked=false
  private releaseSince:number|null=null
  private lastTime:number|null=null
  update(keys: string[], nowMs: number): string|null {
    // A broken/restarted scan clock must not satisfy debounce by accident.
    // Require a fresh stable all-up interval after any invalid time sample.
    const invalidTime=!Number.isFinite(nowMs)||nowMs<0||
      (this.lastTime!==null&&nowMs<this.lastTime)
    this.lastTime=Number.isFinite(nowMs)&&nowMs>=0?nowMs:null
    if(invalidTime){
      this.chordBlocked=true;this.releaseSince=null
      this.candidate=null;this.latched=null;return null
    }
    if(keys.length>1){
      this.chordBlocked=true;this.releaseSince=null
      this.candidate=null;this.latched=null;return null
    }
    if(this.chordBlocked){
      if(keys.length!==0){this.releaseSince=null;return null}
      if(this.releaseSince===null){this.releaseSince=nowMs;return null}
      if(nowMs-this.releaseSince<30)return null
      this.chordBlocked=false;this.releaseSince=null
      this.candidate=null;this.since=nowMs;return null
    }
    const next=keys.length===1?keys[0]:null
    if(next!==this.candidate){this.candidate=next;this.since=nowMs;return null}
    if(nowMs-this.since<30) return null
    if(next===null){this.latched=null;return null}
    if(this.latched===next) return null
    this.latched=next;return next
  }
}
export class PhoneCore {
  digits=''
  state:'idle'|'dialing'|'ringing'|'active'='idle'
  private received=''
  private deadline=0
  // Returned commands must pass through a serialized AT transport; never
  // directly expose arbitrary UI text to AT commands.
  key(k:string,nowMs:number):string[] {
    if(k==='END'){
      if(this.state==='idle'){this.digits=this.digits.slice(0,-1);return []}
      this.state='idle';return ['ATH\r']
    }
    if(k==='CALL'){
      if(this.state==='ringing'){this.state='dialing';this.deadline=nowMs+30000;return ['ATA\r']}
      if(this.state!=='idle'||!/^\+?[0-9]{1,20}$/.test(this.digits))return []
      this.state='dialing';this.deadline=nowMs+60000;return [`ATD${this.digits};\r`]
    }
    if(this.state==='idle'&&/^[0-9]$/.test(k)&&this.digits.length<20)this.digits+=k
    return []
  }
  feed(chunk:string):void {
    this.received+=chunk
    if(this.received.length>4096){this.received='';return}
    let eol:number
    while((eol=this.received.indexOf('\n'))>=0){
      const line=this.received.slice(0,eol).trim();this.received=this.received.slice(eol+1)
      if(line==='RING'&&this.state==='idle')this.state='ringing'
      if(['NO CARRIER','BUSY','NO ANSWER','ERROR'].includes(line))this.state='idle'
      // CLCC state 0 means active; plain OK is only command acknowledgement.
      if(/^\+CLCC:\s*\d+,\d+,0,/.test(line))this.state='active'
    }
  }
  tick(nowMs:number):string[] {
    if(this.state==='dialing'&&nowMs>=this.deadline){this.state='idle';return ['ATH\r']}
    return []
  }
}
