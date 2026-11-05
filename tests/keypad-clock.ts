import assert from 'node:assert/strict'
import {KeyDebouncer} from '../firmware/phone-core'
for(const bad of [NaN,Infinity,-Infinity,-1,5]) {
 const k=new KeyDebouncer()
 assert.equal(k.update(['CALL'],10),null)
 assert.equal(k.update(['CALL'],bad),null)
 assert.equal(k.update(['CALL'],100),null)
 assert.equal(k.update(['CALL'],200),null)
 assert.equal(k.update([],210),null)
 assert.equal(k.update([],239),null)
 assert.equal(k.update([],240),null)
 assert.equal(k.update(['CALL'],250),null)
 assert.equal(k.update(['CALL'],279),null)
 assert.equal(k.update(['CALL'],280),'CALL')
 assert.equal(k.update(['CALL'],300),null)
}
// An invalid idle sample also requires all-up recovery; equal timestamps
// cannot accumulate a debounce interval.
const k=new KeyDebouncer()
assert.equal(k.update([],NaN),null)
for(let i=0;i<100;i++) assert.equal(k.update([],0),null)
assert.equal(k.update(['1'],31),null)
assert.equal(k.update([],40),null)
assert.equal(k.update([],70),null)
assert.equal(k.update(['1'],80),null)
assert.equal(k.update(['1'],110),'1')
console.log('keypad clock fault/recovery tests passed')
