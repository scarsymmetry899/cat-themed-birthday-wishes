import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
const root=path.resolve('.'),qa=path.join(root,'docs/qa/phase-2-refinement');
const types={'.html':'text/html','.css':'text/css','.js':'text/javascript','.wasm':'application/wasm','.svg':'image/svg+xml','.png':'image/png','.json':'application/json','.riv':'application/octet-stream','.webm':'video/webm'};
http.createServer((req,res)=>{
 try{
  const pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname);
  if(req.method==='POST'&&/^\/__qa__\/(walk|trot|gait-blend|peek-reverse|state-[0-3])(-metrics)?$/.test(pathname)){
   // Loopback-only review capture; reject cross-origin requests and limit size.
   if(req.headers.origin!=='http://127.0.0.1:8137'){res.writeHead(403).end();return;}
   const chunks=[];let size=0;req.on('data',data=>{size+=data.length;if(size>20*1024*1024)req.destroy();else chunks.push(data);});
   req.on('end',()=>{fs.mkdirSync(qa,{recursive:true});const suffix=pathname.endsWith('-metrics')?'.json':'.webm';fs.writeFileSync(path.join(qa,pathname.split('/').pop()+suffix),Buffer.concat(chunks));res.writeHead(201).end('Saved');});return;
  }
  if(req.method!=='GET'&&req.method!=='HEAD'){res.writeHead(405).end();return;}
  let file=path.resolve(root,'.'+pathname);
  if(!file.startsWith(root+path.sep)&&file!==root){res.writeHead(403).end();return;}
  if(fs.statSync(file).isDirectory())file=path.join(file,'index.html');
  res.setHeader('Content-Type',types[path.extname(file)]??'application/octet-stream');res.setHeader('Cache-Control','no-store');
  if(req.method==='HEAD')res.end();else fs.createReadStream(file).on('error',()=>res.destroy()).pipe(res);
 }catch{res.writeHead(404).end('Not found');}
}).listen(8137,'127.0.0.1',()=>console.log('Character review: http://127.0.0.1:8137/character-lab/'));
