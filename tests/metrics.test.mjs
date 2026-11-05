import test from 'node:test';
import assert from 'node:assert/strict';
import {onRequest} from '../functions/api/events.js';

function fixture(body={event:'page_view',target:'/'},headers={},method='POST'){
  const calls=[];
  const env={USAGE_DB:{prepare(sql){return {bind(...params){calls.push({sql,params});return {async run(){return {success:true};}};}};}}};
  const request=new Request('https://origamipenguin.com/api/events',{method,headers:{Origin:'https://origamipenguin.com','Content-Type':'application/json',...headers},...(method==='POST'?{body:JSON.stringify(body)}:{})});
  return {request,env,calls};
}
test('valid actions save only the date, action, and bounded public target',async()=>{
  const f=fixture();assert.equal((await onRequest(f)).status,204);assert.equal(f.calls.length,1);assert.equal(f.calls[0].params.length,3);assert.match(f.calls[0].params[0],/^\d{4}-\d{2}-\d{2}$/);assert.deepEqual(f.calls[0].params.slice(1),['page_view','/']);
});
test('unknown targets and event kinds cannot write data',async()=>{for(const body of [{event:'page_view',target:'/not-a-real-page?email=private'},{event:'email',target:'/'},{event:'constructor',target:'/'},null]){const f=fixture(body);assert.equal((await onRequest(f)).status,400);assert.equal(f.calls.length,0);}});
test('cross-origin submissions are rejected',async()=>{const f=fixture(undefined,{Origin:'https://example.com'});assert.equal((await onRequest(f)).status,403);assert.equal(f.calls.length,0);});
test('privacy signals skip counters',async()=>{for(const header of [{'DNT':'1'},{'Sec-GPC':'1'}]){const f=fixture(undefined,header);assert.equal((await onRequest(f)).status,204);assert.equal(f.calls.length,0);}});
test('large payloads and unsupported content are rejected',async()=>{assert.equal((await onRequest(fixture({event:'x'.repeat(800),target:'/'}))).status,413);assert.equal((await onRequest(fixture(undefined,{'Content-Type':'text/plain'}))).status,415);});
test('read requests cannot expose counters',async()=>{assert.equal((await onRequest(fixture(undefined,{},'GET'))).status,405);});
test('missing binding is explicit and does not break page responses',async()=>{const f=fixture();f.env={};assert.equal((await onRequest(f)).status,503);});
