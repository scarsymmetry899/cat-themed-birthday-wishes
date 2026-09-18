import assert from 'node:assert/strict';
import fs from 'node:fs';
const data=JSON.parse(fs.readFileSync('assets/character/production/gait-samples.json','utf8'));
const result={};
for(const [name,cycle] of Object.entries(data)){
 let contacts=0,maxStanceDrift=0;
 for(const sample of cycle.samples)for(const [paw,point] of Object.entries(sample.feet)){
  assert(Number.isFinite(point.x)&&Number.isFinite(point.y));
  if(point.contact){contacts++;const expectedX=paw.startsWith('left')?(paw.includes('rear')?133:140):(paw.includes('rear')?193:186),expectedY=paw.includes('rear')?322:323;maxStanceDrift=Math.max(maxStanceDrift,Math.hypot(point.x-expectedX,point.y-expectedY));}
 }
 assert(maxStanceDrift<1e-9,`${name}: planted paw target drift`);
 for(const paw of Object.keys(cycle.samples[0].feet))assert(Math.hypot(cycle.samples[0].feet[paw].x-cycle.samples.at(-1).feet[paw].x,cycle.samples[0].feet[paw].y-cycle.samples.at(-1).feet[paw].y)<1e-8,'cycle seam');
 if(name==='Trot')for(const sample of cycle.samples){assert.equal(sample.feet.left_paw.contact,sample.feet.right_rear_paw.contact);assert.equal(sample.feet.right_paw.contact,sample.feet.left_rear_paw.contact);}
 result[name]={seconds:cycle.duration/cycle.fps,contacts,maxStanceDrift};
}
const source=fs.readFileSync('rive-foundation/scene.rml','utf8');
for(const name of ['Marmalade_Main','showMarkings','headLook','earLook','PeekEars','PeekEyes','PeekReach','PeekOvershoot','Walk','Trot'])assert(source.includes(`name="${name}"`),name);
console.log(JSON.stringify({passed:true,scope:'Authored target geometry, cycle closure and diagonal timing; not an aesthetic or runtime-blend acceptance test.',gaits:result},null,2));
