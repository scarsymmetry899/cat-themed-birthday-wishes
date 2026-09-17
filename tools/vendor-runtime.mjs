import fs from 'node:fs';
fs.mkdirSync('character-lab/vendor',{recursive:true});
for(const f of ['rive.js','rive.wasm'])fs.copyFileSync(`node_modules/@rive-app/canvas/${f}`,`character-lab/vendor/${f}`);
// License is linked by the package README; upstream package ships no LICENSE file.
