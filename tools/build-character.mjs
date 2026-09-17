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
// Production redraw v2: round facial volumes, soft cream cheek boundary,
// compact haunches and overlapping limb contours replace the rejected draft.
const edit=(name,d)=>{const item=find(root,name);item.d=d;return item;};
edit('head_base','M -62 -49 C -43 -68 -12 -76 15 -73 C 45 -71 65 -53 71 -28 C 76 -13 79 -5 83 3 L 79 6 L 84 12 L 78 15 C 81 31 68 44 53 51 C 31 63 5 65 -18 61 C -44 58 -65 49 -76 34 C -82 26 -83 20 -82 14 L -87 11 L -82 6 L -87 2 L -82 -2 C -77 -16 -74 -37 -62 -49 Z');
edit('forehead_M','M -24 -65 C -21 -67 -18 -67 -16 -66 L -9 -45 L -2 -62 L 4 -61 L 12 -44 L 20 -67 L 25 -64 L 17 -30 C 15 -27 12 -28 10 -32 L 1 -48 L -7 -30 C -9 -27 -12 -30 -13 -33 Z');
edit('cream_muzzle','M 0 -16 C -12 -17 -20 -8 -28 -7 C -44 -6 -52 -1 -65 -5 C -62 8 -49 19 -32 24 C -12 31 10 32 29 26 C 46 21 60 9 64 -4 C 51 0 39 -7 27 -7 C 17 -8 9 -17 0 -16 Z');
find(root,'muzzle_chin').opacity=0;
for(const [side,sign] of [['left',-1],['right',1]]){
 const eye=find(root,`${side}_eye`); const shape='M -20 0 C -21 -12 -12 -19 -1 -19 C 11 -20 20 -12 20 0 C 20 11 11 18 0 18 C -12 18 -20 12 -20 0 Z';eye.clip=shape;find(root,`${side}_eye_white`).d=shape;
 for(const [suffix,rx,ry] of [['iris',15.5,17.5],['pupil_dark',11.5,15.5]]){Object.assign(find(root,`${side}_${suffix}`),{rx,ry});}
 find(root,`${side}_eye`).y=-1;
 find(root,`${side}_catchlight`).rx=3.1;find(root,`${side}_catchlight`).ry=3.7;
 find(root,`${side}_catchlight_small`).opacity=0;
 const lid=find(root,`${side}_upper_eyelid`); const at=eye.children.indexOf(lid);eye.children[at]=g(`${side}_expression_lid`,0,0,[lid]);
 const pupil=find(root,`${side}_pupil`);eye.children[eye.children.indexOf(pupil)]=g(`${side}_gaze_drift`,0,0,[pupil]);
 edit(`${side}_upper_shape`,'M -15 -25 C -24 -17 -20 4 -16 20 C -15 29 -10 38 -2 39 C 11 39 17 26 16 13 C 17 -3 20 -19 9 -24 C 0 -28 -7 -28 -15 -25 Z');
 edit(`${side}_lower_shape`,'M -14 -12 C -17 -8 -16 4 -13 21 C -12 30 -13 39 -10 44 C -5 50 6 49 11 44 C 14 32 14 14 15 1 C 16 -8 9 -15 0 -14 Z');
 find(root,`${side}_upper_shape`).stroke=null;find(root,`${side}_lower_shape`).stroke=null;
 const thigh=find(root,`${side}_thigh`);thigh.x=163+sign*30;
 edit(`${side}_upper_band`,'M -18 16 C -11 20 -6 18 -2 19 C 5 20 10 18 15 15 L 14 21 C 7 23 1 24 -3 23 C -10 24 -14 22 -17 22 Z');
 edit(`${side}_lower_band`,'M -14 17 C -5 20 5 21 14 16 L 13 22 C 3 26 -5 25 -13 23 Z');
 edit(`${side}_ear_light`,sign<0?'M -15 5 C -10 -1 -7 -2 -1 -1 L -12 -14 L 3 -5 L -5 -20 L 10 -6 L 19 -9 L 7 4 Z':'M 15 5 C 10 -1 7 -2 1 -1 L 12 -14 L -3 -5 L 5 -20 L -10 -6 L -19 -9 L -7 4 Z');
}
edit('chest','M -28 -23 C -17 -19 16 -19 27 -24 C 33 -10 28 7 22 20 C 15 32 9 48 3 57 L -2 47 L -7 51 C -10 34 -24 28 -28 12 C -33 0 -34 -12 -28 -23 Z');
// Chest sits over shoulder overlaps, as in the canonical front view.
const chest=find(root,'cream_chest');torso.children.splice(torso.children.indexOf(chest),1);chest.x+=torso.x;chest.y+=torso.y;root.children.splice(root.children.indexOf(head),0,chest);
for(const side of ['left','right'])for(const name of ['upper_shape','lower_shape','haunch','rear_shin']){const piece=find(root,`${side}_${name}`);piece.fill='#E8893B';piece.stroke=null;}
// Five articulated round-ended segments share endpoints and overlap by their radius.
tail.children=[];let tailParent=tail;
for(const [i,dx,dy,w] of [[0,-28,-5,24],[1,-17,-23,25],[2,-2,-28,25],[3,-2,-25,24],[4,1,-17,22]]){
 const segment=g(`tail_segment_${i}`,0,0,[p(`tail_fur_${i}`,`M 0 0 C ${dx*.45} ${dy*.2} ${dx*.85} ${dy*.7} ${dx} ${dy}`,null,C.fur,w),p(`tail_ring_${i}`,`M ${dx*.24} ${dy*.24} C ${dx*.4} ${dy*.32} ${dx*.5} ${dy*.5} ${dx*.62} ${dy*.62}`,null,i===4?C.cream:C.stripe,w+.2)]);tailParent.children.push(segment);const joint=g(`tail_joint_${i}`,dx,dy,[]);segment.children.push(joint);tailParent=joint;
}
tailParent.children.push(e('tail_soft_tip',0,0,10.8,9,C.cream));
head.children.push(g('hat_anchor',0,-77,[]));
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
// Standalone exports retain local coordinates, with a generous inspection canvas.
// parts.json and the assembled SVG preserve the actual parent/pivot registration.
const partDoc=n=>svgdoc(svg(n)).replace('viewBox="0 0 300 370"','viewBox="-180 -180 600 650"');
for(const part of parts)fs.writeFileSync(`${out}/${part.name}.svg`,partDoc(part));
for(const name of ['head_base','torso',...['left','right'].flatMap(s=>[`${s}_eye_white`,`${s}_iris`,`${s}_pupil_dark`,`${s}_catchlight`])])fs.writeFileSync(`${out}/${name}.svg`,partDoc(find(root,name)));
for(const [name,left,right] of [['focused',20,20],['mischievous',28,14]]){
 find(root,'left_expression_lid').y=left;find(root,'right_expression_lid').y=right;
 fs.writeFileSync(`${out}/marmalade-${name}.svg`,svgdoc(svg(root)));
}
find(root,'left_expression_lid').y=0;find(root,'right_expression_lid').y=0;
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
const rest={cat_root:{y:0},head_group:{y:147,rotation:0},left_upper_front:{y:243,rotation:0},right_upper_front:{y:243,rotation:0},left_lower_front:{y:32,rotation:0},right_lower_front:{y:32,rotation:0},left_paw:{y:48,rotation:0},right_paw:{y:48,rotation:0},left_thigh:{y:272,rotation:0},right_thigh:{y:272,rotation:0}};
function pose(name,overrides={},duration=60,loop='oneShot'){const keys=[];for(const [part,props] of Object.entries(rest))for(const [prop,value] of Object.entries(props)){const frames=overrides[part]?.[prop];keys.push(key(part,prop,Array.isArray(frames)?frames:[[0,frames??value]]));}return anim(name,duration,keys,loop);}
rest.left_gaze_drift={x:0,y:0};rest.right_gaze_drift={x:0,y:0};
pose('Idle');
const glance=[[0,0],[35,0],[65,-2],[110,-2],[145,2],[190,2],[220,0],[240,0]];
pose('Looking',{head_group:{rotation:glance.map(([f,v])=>[f,v*.015])},left_gaze_drift:{x:glance},right_gaze_drift:{x:glance}},240,'loop');
const peek={head_group:{y:166,rotation:.035},left_upper_front:{y:215,rotation:-.12},right_upper_front:{y:215,rotation:.12},left_lower_front:{y:10},right_lower_front:{y:10},left_paw:{y:22,rotation:.12},right_paw:{y:22,rotation:-.12}};
pose('PeekHidden',{...peek,cat_root:{y:260}});pose('PeekHold',peek);
for(const [name,duration,amplitude] of [['Walk',64,7],['Trot',40,11]]){
 const wave=(base,a,phase=0)=>Array.from({length:17},(_,i)=>[i*duration/16,base+Math.sin(i/16*Math.PI*2+phase)*a]);const motions={cat_root:{y:Array.from({length:17},(_,i)=>[i*duration/16,-(Math.sin(i/16*Math.PI*4)**2)*2])},head_group:{rotation:wave(0,.016)}};
 for(const [side,phase] of [['left',0],['right',Math.PI]]){motions[`${side}_upper_front`]={y:wave(243,amplitude,phase),rotation:wave(0,.04,phase)};motions[`${side}_lower_front`]={y:wave(32,amplitude*.3,phase),rotation:wave(0,.035,phase)};motions[`${side}_paw`]={y:wave(48,amplitude*.2,phase),rotation:wave(0,.035,phase+1)};motions[`${side}_thigh`]={y:wave(272,amplitude*.55,phase+Math.PI),rotation:wave(0,.03,phase+Math.PI)};}
 pose(name,motions,duration,'loop');
}
anim('Breathing',288,[key('body_group','scaleY',[[0,1],[72,1.014],[144,1],[216,.995],[288,1]])],'loop');
anim('Ears',360,[key('left_ear','rotation',[[0,0],[112,0],[118,-.065],[125,.02],[135,0],[360,0]]),key('right_ear','rotation',[[0,0],[230,0],[238,.05],[249,0],[360,0]])],'loop');
anim('Tail',240,Array.from({length:5},(_,i)=>key(`tail_segment_${i}`,'rotation',Array.from({length:17},(_,f)=>[f*15,Math.sin(f/16*Math.PI*2-i*.4)*(.018+i*.007)]))),'loop');
const lidKeys=(closed=false)=>['left','right'].flatMap(s=>[key(`${s}_upper_eyelid`,'y',closed?[[0,-26],[158,-26],[164,24],[170,-26],[240,-26]]:[[0,-26]]),key(`${s}_lower_eyelid`,'y',closed?[[0,24],[158,24],[164,16],[170,24],[240,24]]:[[0,24]])]);
anim('Blink',240,lidKeys(true),'loop');anim('EyesOpen',60,lidKeys());
for(const [label,axis,offset] of [['GazeLeft','x',-5],['GazeCenterX','x',0],['GazeRight','x',5],['GazeUp','y',-3],['GazeCenterY','y',0],['GazeDown','y',3]])anim(label,60,['left','right'].map(s=>key(`${s}_pupil`,axis,[[0,offset]])));
for(const [name,amount] of [['NoHat',0],['Hat',1]])anim(name,60,[key('birthday_hat','opacity',[[0,amount]])]);
for(const [name,yl,yr,rl,rr] of [['Gentle',0,0,0,0],['Focused',20,20,.12,-.12],['Mischievous',28,14,-.1,-.05]])anim(name,60,[key('left_expression_lid','y',[[0,yl]]),key('right_expression_lid','y',[[0,yr]]),key('left_expression_lid','rotation',[[0,rl]]),key('right_expression_lid','rotation',[[0,rr]])]);
const input=(name,type,value)=>`<StateMachine${type} id="${id('input_'+name)}" name="${name}" value="${value}"/>`;
const inputs=[input('state','Number',0),input('scrollProgress','Number',100),input('lookX','Number',50),input('lookY','Number',50),input('moveSpeed','Number',0),input('expression','Number',0),input('blinkEnabled','Bool',true),input('hasHat','Bool',false)];
const condition=(name,value)=>typeof value==='boolean'?`<TransitionBoolCondition inputId="${id('input_'+name)}" opValue="${value?'equal':'notEqual'}"/>`:`<TransitionNumberCondition inputId="${id('input_'+name)}" opValue="equal" value="${value}"/>`;
const transition=(to,cond='',blend=false,duration=450)=>`<${blend?'BlendStateTransition':'StateTransition'} stateToId="${id('state_'+to)}" duration="${duration}" interpolationType="cubic"><CubicEaseInterpolator x1=".42" y1="0" x2=".58" y2="1"/>${cond}</${blend?'BlendStateTransition':'StateTransition'}>`;
const state=(name,animation,x,children='')=>`<AnimationState id="${id('state_'+name)}" x="${x}" y="0" animationId="${id('anim_'+animation)}">${children}</AnimationState>`;
const layer=(name,first,states)=>`<StateMachineLayer name="${name}"><AnyState x="0" y="-140"/><ExitState x="600" y="-140"/><EntryState x="0" y="0">${transition(first,'',false,0)}</EntryState>${states}</StateMachineLayer>`;
function blend(name,inputName,items,x,children=''){return `<BlendState1DInput id="${id('state_'+name)}" inputId="${id('input_'+inputName)}" x="${x}" y="0">${items.map(([a,v])=>`<BlendAnimation1D animationId="${id('anim_'+a)}" value="${v}"/>`).join('')}${children}</BlendState1DInput>`;}
const bodyNames=['Idle','Peeking','Looking','Walking'];const body=bodyNames.map((n,i)=>{const transitions=bodyNames.filter(t=>t!==n).map(t=>transition(t,condition('state',bodyNames.indexOf(t)),i===1||i===3,550)).join('');return i===1?blend(n,'scrollProgress',[['PeekHidden',0],['PeekHold',100]],i*220+180,transitions):i===3?blend(n,'moveSpeed',[['Walk',0],['Trot',100]],i*220+180,transitions):state(n,n,i*220+180,transitions);}).join('');
const layers=[layer('Body_Action','Idle',body),layer('Breathing','Breathing',state('Breathing','Breathing',180)),layer('Ear_Reaction','Ears',state('Ears','Ears',180)),layer('Tail_Behavior','Tail',state('Tail','Tail',180)),layer('Face_Reaction','Blink',state('Blink','Blink',180,transition('EyesOpen',condition('blinkEnabled',false)))+state('EyesOpen','EyesOpen',400,transition('Blink',condition('blinkEnabled',true)))),layer('Gaze_X','GazeX',blend('GazeX','lookX',[['GazeLeft',0],['GazeCenterX',50],['GazeRight',100]],180)),layer('Gaze_Y','GazeY',blend('GazeY','lookY',[['GazeUp',0],['GazeCenterY',50],['GazeDown',100]],180)),layer('Accessories','NoHat',state('NoHat','NoHat',180,transition('Hat',condition('hasHat',true),false,250))+state('Hat','Hat',400,transition('NoHat',condition('hasHat',false),false,250))),layer('Expression','Gentle',['Gentle','Focused','Mischievous'].map((n,i)=>state(n,n,180+i*220,['Gentle','Focused','Mischievous'].filter(t=>t!==n).map(t=>transition(t,condition('expression',['Gentle','Focused','Mischievous'].indexOf(t)),false,280)).join(''))).join(''))];
const doc=`<Rive version="1" kind="fragment"><Artboard width="300" height="370" name="Marmalade_Main" id="0:1" defaultStateMachineId="0:2" styleId="0:4"><LayoutComponentStyle id="0:4"/>${artwork}${animations.join('')}<StateMachine name="Marmalade_Main" id="0:2">${inputs.join('')}${layers.join('')}</StateMachine></Artboard></Rive>`;
fs.writeFileSync('rive-foundation/scene.rml',doc);
fs.writeFileSync(`${out}/id-map.json`,JSON.stringify(ids,null,2));
console.log(`Generated ${parts.length} vector groups; native RML neutral assembly.`);
