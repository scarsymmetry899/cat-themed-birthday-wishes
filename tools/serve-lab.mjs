import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
const root=path.resolve('.');
http.createServer((req,res)=>{try{let file=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://localhost').pathname));if(!file.startsWith(root+path.sep)&&file!==root){res.writeHead(403).end();return;}if(fs.statSync(file).isDirectory())file=path.join(file,'index.html');const types={'.html':'text/html','.css':'text/css','.js':'text/javascript','.wasm':'application/wasm','.svg':'image/svg+xml','.png':'image/png','.json':'application/json','.riv':'application/octet-stream'};res.setHeader('Content-Type',types[path.extname(file)]??'application/octet-stream');fs.createReadStream(file).pipe(res);}catch{res.writeHead(404).end('Not found');}}).listen(8137,'127.0.0.1',()=>console.log('Character review: http://127.0.0.1:8137/character-lab/'));
