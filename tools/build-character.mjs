import fs from 'node:fs';
import path from 'node:path';
// Source geometry is authored in master-sheet front-view coordinates.
// All production exports are vectors. No bitmap is embedded in the character.
const out = 'assets/character/production';
fs.mkdirSync(out,{recursive:true});
const C={fur:'#E8893A',stripe:'#A94E2B',cream:'#F7E3BE',eye:'#D99A24',ink:'#4A2C25',nose:'#D97C78',ear:'#E7A0A0',teal:'#2E8C87',coral:'#F06F61',gold:'#F5C65B'};
let seq=100; const ids={}; const id=n=>ids[n]??= `0:${seq++}`;
const group=(name,x,y,children,extra={})=>({kind:'group',name,x,y,children,...extra});
const p=(name,d,fill,stroke=null,width=1)=>({kind:'path',name,d,fill,stroke,width});
const e=(name,x,y,rx,ry,fill,stroke=null,width=1)=>({kind:'ellipse',name,x,y,rx,ry,fill,stroke,width});
const fur=(name,d)=>p(name,d,C.fur,C.stripe,.65);
const stripe=(name,d)=>p(name,d,C.stripe);
const parts=[];
const g=(...args)=>{const a=group(...args);parts.push(a);return a;};
const tail=g('tail_base',100,278,[
  fur('tail_contour','M 0 0 C -32 8 -48 -10 -47 -40 C -46 -58 -50 -66 -50 -78 C -51 -91 -38 -96 -30 -88 C -20 -78 -24 -62 -22 -48 C -22 -28 -11 -25 9 -26 Z'),
  stripe('tail_band_1','M -43 -8 C -34 -14 -28 -17 -22 -18 L -12 -25 L -2 -26 L 4 -8 C -10 -2 -22 1 -33 -2 Z'),
  stripe('tail_band_2','M -47 -31 C -40 -36 -31 -39 -23 -39 L -22 -50 C -32 -50 -39 -47 -47 -44 Z'),
  stripe('tail_band_3','M -47 -58 C -40 -63 -31 -65 -24 -64 L -24 -75 C -34 -77 -42 -73 -49 -69 Z'),
  p('tail_cream_tip','M -50 -79 C -54 -91 -40 -100 -31 -90 C -27 -86 -25 -82 -25 -78 C -32 -84 -41 -83 -50 -79 Z',C.cream)
]);
const rear=[];
for(const [side,x] of [['left',118],['right',207]]){
 rear.push(g(`${side}_thigh`,x,272,[fur(`${side}_haunch`,'M 0 -28 C -19 -23 -24 0 -23 20 C -23 40 -13 51 5 49 C 22 47 26 29 20 11 C 16 -6 13 -21 0 -28 Z'),stripe(`${side}_thigh_stripe`,'M -21 3 C -7 -3 4 2 19 10 L 22 19 C 8 12 -9 10 -23 15 Z'),g(`${side}_rear_lower`,0,33,[fur(`${side}_rear_shin`,'M -14 -12 C -17 0 -13 13 -7 17 L 12 15 C 14 1 11 -10 5 -16 Z'),g(`${side}_rear_paw`,0,17,[p(`${side}_rear_toes`,'M -9 -8 C -23 -6 -22 8 -10 10 L 9 10 C 20 7 17 -8 9 -10 Z',C.cream,C.stripe,.6)])]) ]));
}
const torso=g('body_group',162,245,[fur('torso','M -37 -51 C -49 -34 -51 2 -54 37 C -56 66 -36 79 -3 78 C 26 81 48 69 50 47 C 54 19 39 -32 30 -47 Z'),stripe('body_left_band','M -44 -14 C -37 -10 -33 0 -31 15 C -42 9 -46 6 -48 0 Z'),stripe('body_right_band','M 37 -17 C 31 -9 29 -1 27 8 C 36 5 43 1 44 -5 Z'),g('cream_belly',0,32,[p('belly','M -20 -35 C -36 -17 -36 14 -24 33 C -12 50 16 45 25 29 C 34 9 31 -24 15 -37 Z',C.cream)]),g('cream_chest',0,-23,[p('chest','M -30 -24 C -18 -18 16 -18 27 -27 C 24 -8 15 10 8 28 L 2 22 L -4 36 L -11 27 L -17 30 C -21 13 -33 -6 -30 -24 Z',C.cream)])]);
const legs=[];
for(const [side,x] of [['left',140],['right',186]]){
 legs.push(g(`${side}_upper_front`,x,243,[fur(`${side}_upper_shape`,'M -17 -24 C -24 -4 -20 22 -15 33 L 14 33 C 19 6 17 -18 9 -24 Z'),stripe(`${side}_upper_band`,'M -20 7 C -7 14 1 11 16 5 L 16 13 C 1 21 -9 20 -19 15 Z'),g(`${side}_lower_front`,0,32,[fur(`${side}_lower_shape`,'M -16 -10 C -17 5 -14 30 -12 43 L 10 45 C 16 19 16 3 14 -10 Z'),stripe(`${side}_lower_band`,'M -15 9 C -5 13 5 13 15 8 L 14 16 C 3 21 -4 19 -14 16 Z'),g(`${side}_paw`,0,48,[p(`${side}_paw_tip`,'M -12 -8 C -25 -9 -24 9 -13 12 C -5 14 7 14 14 11 C 24 7 21 -7 10 -10 Z',C.cream,C.stripe,.7),p(`${side}_toe_a`,'M -9 1 L -9 11',null,C.stripe,.7),p(`${side}_toe_b`,'M 2 1 L 2 12',null,C.stripe,.7)])]) ]));
}
const ears=[];
for(const [side,sign] of [['left',-1],['right',1]]){
 const ear=g(`${side}_ear`,sign*59,-44,[fur(`${side}_ear_outer`,sign<0?'M -18 26 C -31 5 -32 -34 -29 -60 C -24 -66 9 -46 33 -21 Z':'M 18 26 C 31 5 32 -34 29 -60 C 24 -66 -9 -46 -33 -21 Z'),g(`${side}_inner_ear`,0,0,[p(`${side}_inner`,sign<0?'M -19 13 C -26 -9 -24 -36 -23 -48 C -9 -42 8 -28 21 -13 Z':'M 19 13 C 26 -9 24 -36 23 -48 C 9 -42 -8 -28 -21 -13 Z',C.ear),p(`${side}_ear_light`,sign<0?'M -17 3 L -13 -32 L -4 -7 L 14 -14 L 3 2 Z':'M 17 3 L 13 -32 L 4 -7 L -14 -14 L -3 2 Z',C.cream)])]); ears.push(ear);
}
const eyes=[];
for(const [side,x] of [['left',-34],['right',34]]){
 const shape='M -20 0 C -22 -16 -11 -25 0 -25 C 14 -25 23 -14 21 0 C 20 14 9 22 -2 21 C -13 20 -20 11 -20 0 Z';
 eyes.push(g(`${side}_eye`,x,-2,[p(`${side}_eye_white`,shape,C.cream,C.ink,1.3),g(`${side}_pupil`,0,0,[e(`${side}_iris`,0,-1,15,20,C.eye),e(`${side}_pupil_dark`,1,-2,10,17,'#251C13'),e(`${side}_catchlight`,5,-12,4.2,5.5,'#FFF9E9'),e(`${side}_catchlight_small`,-4,6,1.4,1.5,'#FFF9E9')]),g(`${side}_upper_eyelid`,0,-26,[p(`${side}_lid_top`,'M -24 -27 L 24 -27 L 24 0 C 5 -5 -7 -5 -24 0 Z',C.fur)]),g(`${side}_lower_eyelid`,0,24,[p(`${side}_lid_bottom`,'M -23 0 C -7 6 7 6 23 0 L 23 18 L -23 18 Z',C.fur)])],{clip:shape}));
}
const head=g('head_group',163,147,[...ears,fur('head_base','M -61 -51 C -43 -70 -12 -77 15 -73 C 45 -72 65 -55 71 -28 C 76 -14 78 -6 85 2 L 78 3 L 87 11 L 78 12 L 83 20 C 76 21 74 34 65 42 C 48 60 24 65 0 66 C -28 64 -49 58 -67 43 C -76 35 -78 25 -86 23 L -81 17 L -90 15 L -82 9 L -90 5 L -82 0 C -77 -15 -74 -38 -61 -51 Z'),
 stripe('forehead_M','M -25 -67 L -17 -71 L -9 -46 L -2 -62 L 6 -63 L 13 -43 L 20 -68 L 27 -64 L 19 -29 L 12 -26 L 2 -47 L -6 -27 L -13 -28 Z'),
 stripe('left_brow','M -53 -34 C -40 -44 -29 -42 -21 -30 C -35 -36 -43 -34 -53 -30 Z'),stripe('right_brow','M 21 -30 C 29 -42 42 -42 53 -33 L 53 -29 C 41 -35 32 -35 21 -30 Z'),
 stripe('cheek_left_upper','M -82 5 C -67 3 -57 8 -46 17 C -61 16 -71 14 -80 13 Z'),stripe('cheek_left_lower','M -76 24 C -61 20 -53 23 -41 28 C -50 35 -63 36 -69 33 Z'),
 stripe('cheek_right_upper','M 82 5 C 67 3 57 8 46 17 C 61 16 71 14 80 13 Z'),stripe('cheek_right_lower','M 76 24 C 61 20 53 23 41 28 C 50 35 63 36 69 33 Z'),
 ...eyes,
 g('muzzle',0,32,[p('cream_muzzle','M 0 -14 C -10 -16 -17 -9 -24 -6 C -33 -5 -43 0 -41 10 C -40 25 -22 31 0 31 C 22 31 40 25 41 10 C 43 0 33 -5 24 -6 C 17 -9 10 -16 0 -14 Z',C.cream),p('muzzle_chin','M -21 23 C -9 37 14 38 26 21 C 11 28 -8 28 -21 23 Z','#F1D7AE')]),
 g('mouth',0,25,[p('mouth_line','M 0 -3 L 0 4 C -5 13 -13 12 -17 8 M 0 4 C 5 13 13 12 17 8',null,C.ink,.9)]),
 g('nose',0,17,[p('nose_shape','M -9 -1 C -7 -5 6 -5 9 -1 C 8 3 3 7 0 7 C -3 7 -8 3 -9 -1 Z',C.nose,C.stripe,.55),p('nose_highlight','M -5 -1 C -2 -3 2 -3 5 -1',null,'#F4B0A0',1)]),
 g('left_whiskers',-28,34,[p('whisker_l1','M 0 0 C -13 -6 -34 -8 -52 -7',null,C.cream,.9),p('whisker_l2','M -2 5 C -18 2 -35 5 -49 9',null,C.cream,.8),p('whisker_l3','M -2 10 C -16 13 -28 18 -36 23',null,C.cream,.65)]),
 g('right_whiskers',28,34,[p('whisker_r1','M 0 0 C 13 -6 34 -8 52 -7',null,C.cream,.9),p('whisker_r2','M 2 5 C 18 2 35 5 49 9',null,C.cream,.8),p('whisker_r3','M 2 10 C 16 13 28 18 36 23',null,C.cream,.65)])
]);
const hat=g('birthday_hat',0,-77,[p('hat_cone','M -28 0 L 7 -66 L 30 0 Z',C.teal),p('hat_ribbon','M -19 -20 L 14 -47 L 18 -35 L -25 -6 Z',C.coral),e('hat_pompom',7,-66,7,7,C.gold)],{opacity:0}); head.children.push(hat);
const root=group('cat_root',0,0,[tail,...rear,torso,...legs,head]);
// Fine vector strokes preserve the master's brushed surface without raster fragments.
let seed=1709;const rand=()=>{seed=(seed*1664525+1013904223)>>>0;return seed/4294967296;};
function texture(name,base,cx,cy,rx,ry,count){const paths=['',''];for(let i=0;i<count;i++){const a=rand()*Math.PI*2,r=Math.sqrt(rand()),x=cx+Math.cos(a)*rx*r,y=cy+Math.sin(a)*ry*r,len=2+rand()*5;const flow=(x-cx)/rx*1.5;paths[i%3?0:1]+=`M ${x} ${y} C ${x+flow} ${y+len*.3} ${x+flow*.7} ${y+len*.6} ${x+flow} ${y+len} `;}const lines=paths.map((d,i)=>({...p(`${name}_${i}`,d,null,i?'#A94E2B':'#F7C17D',.4),opacity:.25}));return {...group(name,0,0,lines),clipRef:base};}
head.children.splice(3,0,texture('head_fur','head_base',0,-8,90,74,450));
torso.children.splice(1,0,texture('body_fur','torso',0,16,52,76,220));
for(const leg of legs)leg.children.splice(1,0,texture(`${leg.name}_fur`,`${leg.name.replace('_upper_front','')}_upper_shape`,0,6,20,30,65));
function attrs(o){return Object.entries(o).map(([k,v])=>`${k}="${v}"`).join(' ')}
function find(n,name){if(n.name===name)return n;for(const c of n.children??[]){const match=find(c,name);if(match)return match;}}
function svg(n){if(n.kind==='group'){const clip=n.clip??(n.clipRef?find(root,n.clipRef)?.d:null);return `<g id="${n.name}" transform="translate(${n.x} ${n.y})" opacity="${n.opacity??1}">${clip?`<defs><clipPath id="${n.name}_clip"><path d="${clip}"/></clipPath></defs><g clip-path="url(#${n.name}_clip)">`:''}${n.children.map(svg).join('')}${clip?'</g>':''}</g>`;}const fill=n.fill===C.fur?'url(#fur)':n.fill===C.cream?'url(#cream)':n.fill??'none';return n.kind==='path'?`<path id="${n.name}" d="${n.d}" fill="${fill}" opacity="${n.opacity??1}" stroke="${n.stroke??'none'}" stroke-width="${n.width}" stroke-linecap="round"/>`:`<ellipse ${attrs({id:n.name,cx:n.x,cy:n.y,rx:n.rx,ry:n.ry,fill,stroke:n.stroke??'none','stroke-width':n.width})}/>`;}
const svgdoc=content=>`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 370"><defs><linearGradient id="fur" gradientUnits="userSpaceOnUse" x1="-40" y1="-60" x2="40" y2="75"><stop stop-color="#F1AC58"/><stop offset=".48" stop-color="#E8893A"/><stop offset="1" stop-color="#CC6B2C"/></linearGradient><linearGradient id="cream" gradientUnits="userSpaceOnUse" x1="0" y1="-15" x2="0" y2="40"><stop stop-color="#FFEDD1"/><stop offset="1" stop-color="#F0D4A6"/></linearGradient></defs>${content}</svg>`;
fs.writeFileSync(`${out}/marmalade-assembled.svg`,svgdoc(svg(root)));
fs.writeFileSync(`${out}/parts.json`,JSON.stringify(root,null,2));
for(const part of parts)fs.writeFileSync(`${out}/${part.name}.svg`,svgdoc(svg(part)));
// Expand SVG cubic/quadratic geometry into native Rive cubic vertices.
function paths(d){const t=d.match(/[A-Za-z]|[-+]?(?:\d*\.)?\d+(?:e[-+]?\d+)?/g);let i=0,cmd,cur=[0,0],contours=[],v=[],closed=false;const num=()=>+t[i++];const finish=()=>{if(v.length){contours.push({v,closed});v=[];closed=false;}};
 while(i<t.length){if(/[A-Za-z]/.test(t[i]))cmd=t[i++];if(cmd==='M'){finish();cur=[num(),num()];v.push({p:cur});cmd='L';}else if(cmd==='L'){cur=[num(),num()];v.push({p:cur});}else if(cmd==='C'){const a=[num(),num()],b=[num(),num()],end=[num(),num()];v.at(-1).out=a;v.push({p:end,in:b});cur=end;}else if(cmd==='Z'){closed=true;finish();cmd=null;}else throw Error('Unsupported path '+cmd);}finish();return contours;}
const color=h=>'FF'+h.slice(1).toUpperCase();
function geom(d){return paths(d).map(({v,closed})=>`<PointsPath isClosed="${closed}">${v.map(a=>{if(!a.in&&!a.out)return `<StraightVertex x="${a.p[0]}" y="${a.p[1]}"/>`;const handle=b=>b?[Math.atan2(b[1]-a.p[1],b[0]-a.p[0]),Math.hypot(b[0]-a.p[0],b[1]-a.p[1])]:[0,0];const [ir,il]=handle(a.in),[or,ol]=handle(a.out);return `<CubicDetachedVertex x="${a.p[0]}" y="${a.p[1]}" inRotation="${ir}" inDistance="${il}" outRotation="${or}" outDistance="${ol}"/>`;}).join('')}</PointsPath>`).join('');}
function paint(fill){if(fill===C.fur)return `<LinearGradient startX="-40" startY="-60" endX="40" endY="75"><GradientStop position="0" colorValue="FFF1AC58"/><GradientStop position="0.48" colorValue="FFE8893A"/><GradientStop position="1" colorValue="FFCC6B2C"/></LinearGradient>`;if(fill===C.cream)return `<LinearGradient startX="0" startY="-15" endX="0" endY="40"><GradientStop position="0" colorValue="FFFFEDD1"/><GradientStop position="1" colorValue="FFF0D4A6"/></LinearGradient>`;return `<SolidColor colorValue="${color(fill)}"/>`;}
function rml(n,clips=[]){const uid=id(n.name);if(n.kind==='group'){let mask='';if(n.clip){const mid=id(n.name+'_mask');mask=`<Shape id="${mid}" name="${n.name}_mask">${geom(n.clip)}</Shape>`;clips=[...clips,mid];}if(n.clipRef)clips=[...clips,id(n.clipRef)];return `<Node id="${uid}" name="${n.name}" x="${n.x}" y="${n.y}" opacity="${n.opacity??1}">${[...n.children].reverse().map(c=>rml(c,clips)).join('')}${mask}</Node>`;}return `<Shape id="${uid}" name="${n.name}" opacity="${n.opacity??1}" ${n.kind==='ellipse'?`x="${n.x}" y="${n.y}"`:''}>${n.kind==='ellipse'?`<Ellipse width="${n.rx*2}" height="${n.ry*2}" originX="0.5" originY="0.5"/>`:geom(n.d)}${n.fill?`<Fill>${paint(n.fill)}</Fill>`:''}${n.stroke?`<Stroke thickness="${n.width}" cap="round"><SolidColor colorValue="${color(n.stroke)}"/></Stroke>`:''}${clips.map(c=>`<ClippingShape sourceId="${c}"/>`).join('')}</Shape>`;}
const artwork=rml(root);
const key=(name,prop,frames)=>`<KeyedObject objectId="${id(name)}"><KeyedProperty propertyKey="${({x:13,y:14,rotation:15,scaleX:16,scaleY:17,opacity:18})[prop]}">${frames.map(([f,val])=>`<KeyFrameDouble frame="${f}" value="${val}" interpolationType="linear"/>`).join('')}</KeyedProperty></KeyedObject>`;
const animations=[];function anim(name,duration,keys,loop='oneShot'){const aid=id('anim_'+name);animations.push(`<LinearAnimation id="${aid}" name="${name}" fps="60" duration="${duration}" loopValue="${loop}">${keys.join('')}</LinearAnimation>`);return aid;}
anim('Neutral',60,[key('cat_root','y',[[0,0]])]);
const doc=`<Rive version="1" kind="fragment"><Artboard width="300" height="370" name="Marmalade_Main" id="0:1" defaultStateMachineId="0:2" styleId="0:4"><LayoutComponentStyle id="0:4"/>${artwork}${animations.join('')}<StateMachine name="Marmalade_Main" id="0:2"><StateMachineLayer name="Body_Action"><AnyState x="0" y="-100"/><ExitState x="500" y="-100"/><EntryState x="0" y="0"><StateTransition stateToId="0:3"/></EntryState><AnimationState x="200" y="0" id="0:3" animationId="${id('anim_Neutral')}"/></StateMachineLayer></StateMachine></Artboard></Rive>`;
fs.writeFileSync('rive-foundation/scene.rml',doc);
fs.writeFileSync(`${out}/id-map.json`,JSON.stringify(ids,null,2));
console.log(`Generated ${parts.length} vector groups; native RML neutral assembly.`);
