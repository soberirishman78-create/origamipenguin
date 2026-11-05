import {targets} from '../../lib/metric-targets.js';

const response=status=>new Response(null,{status,headers:{'Cache-Control':'no-store','X-Content-Type-Options':'nosniff'}});

export async function onRequest(context){
  const {request,env}=context,url=new URL(request.url);
  if(request.method!=='POST')return new Response(null,{status:405,headers:{Allow:'POST','Cache-Control':'no-store'}});
  if(url.hostname!=='origamipenguin.com')return response(204);
  if(request.headers.get('Origin')!==url.origin)return response(403);
  if(request.headers.get('DNT')==='1'||request.headers.get('Sec-GPC')==='1')return response(204);
  if(!request.headers.get('Content-Type')?.toLowerCase().startsWith('application/json'))return response(415);
  if(Number(request.headers.get('Content-Length')||0)>512)return response(413);
  let body;
  try{
    const reader=request.body?.getReader();if(!reader)return response(400);
    let bytes=0,text='';const decoder=new TextDecoder();
    while(true){const {done,value}=await reader.read();if(done)break;bytes+=value.byteLength;if(bytes>512){await reader.cancel();return response(413);}text+=decoder.decode(value,{stream:true});}
    text+=decoder.decode();body=JSON.parse(text);
  }catch{return response(400);}
  if(!body||typeof body.event!=='string'||typeof body.target!=='string'||!Object.hasOwn(targets,body.event)||!targets[body.event].includes(body.target))return response(400);
  if(!env.USAGE_DB)return response(503);
  try{
    // Only daily aggregate counts are stored: no IP, email, cookie, referrer, or visitor ID.
    await env.USAGE_DB.prepare('INSERT INTO daily_counts(day,event,target,total) VALUES(?,?,?,1) ON CONFLICT(day,event,target) DO UPDATE SET total=MIN(total+1,1000000)').bind(new Date().toISOString().slice(0,10),body.event,body.target).run();
    return response(204);
  }catch{console.error(JSON.stringify({message:'usage_counter_write_failed'}));return response(503);}
}
