// Hand-authored refinement against the unchanged 300 × 370 front-view crop.
// Decorative contours stay outside the clean, overlapping joint zones.
export function refine({root,find,p,g,e,C}) {
 const edit=(name,d)=>find(root,name).d=d;
 const head=find(root,'head_group'),body=find(root,'body_group');
 edit('head_base','M -63 -47 C -48 -65 -21 -75 7 -74 C 35 -75 62 -59 71 -34 C 76 -18 78 -8 83 1 L 78 3 L 85 8 L 80 11 L 85 16 L 79 17 C 81 27 75 36 67 41 C 51 52 30 58 8 58 C -19 59 -45 53 -64 42 C -76 35 -83 28 -82 20 L -88 17 L -82 13 L -90 10 L -84 6 L -90 3 L -83 -2 C -78 -15 -73 -36 -63 -47 Z');
 edit('forehead_M','M -20 -72 L -12 -70 C -11 -62 -8 -57 -6 -51 L -1 -66 L 5 -65 L 10 -52 C 13 -60 14 -65 16 -71 L 22 -72 C 20 -58 17 -46 15 -34 L 11 -31 C 8 -39 3 -47 1 -53 C -2 -46 -6 -40 -8 -33 L -12 -35 C -15 -45 -18 -60 -20 -72 Z M -24 -65 C -24 -51 -21 -42 -20 -34 L -17 -30 C -16 -43 -17 -57 -19 -66 Z');
 edit('cream_muzzle','M 0 -17 C -8 -18 -14 -12 -22 -9 C -34 -6 -49 -6 -63 -1 L -59 2 L -64 4 C -59 7 -54 9 -48 13 L -50 14 C -38 21 -27 24 -15 25 L -16 27 C 2 29 16 27 28 24 C 42 20 55 13 63 3 L 59 2 L 63 -1 C 46 -7 34 -6 24 -10 C 15 -12 7 -18 0 -17 Z');
 // The painted eyes are wider apart, with small inward-biased pupils.
 const eyeD=['M -20 0 C -22 -11 -12 -20 0 -19 C 13 -18 22 -7 21 2 C 19 12 9 18 -2 17 C -14 16 -19 8 -20 0 Z','M -21 1 C -21 -10 -11 -20 1 -19 C 14 -19 22 -10 21 1 C 21 12 10 18 -1 18 C -12 18 -20 12 -21 1 Z'];
 for(const [i,s] of ['left','right'].entries()){
  const eye=find(root,`${s}_eye`);eye.x=i?35:-37;eye.y=-1;eye.clip=eyeD[i];edit(`${s}_eye_white`,eyeD[i]);
  Object.assign(find(root,`${s}_iris`),{x:i?-2:3,y:0,rx:14.5,ry:16.2});
  Object.assign(find(root,`${s}_pupil_dark`),{x:i?-2:4,y:-.3,rx:9.3,ry:13.5});
  Object.assign(find(root,`${s}_catchlight`),{x:i?-5:1,y:-8.5,rx:3,ry:3.8});
  find(root,`${s}_catchlight_small`).opacity=.4;
  find(root,`${s}_catchlight_small`).x=i?2:8;
  find(root,`${s}_catchlight_small`).y=6;
  edit(`${s}_lid_top`,'M -25 -80 L 25 -80 L 25 0 C 8 -5 -8 -5 -25 0 Z');
  find(root,`${s}_upper_eyelid`).children.push(p(`${s}_lid_edge`,'M -25 0 C -8 -5 8 -5 25 0',null,C.stripe,.65));
  find(root,`${s}_lid_top`).fill='#EFA54F';find(root,`${s}_lid_bottom`).fill='#EFA54F';
  find(root,`${s}_lower_eyelid`).children.push(p(`${s}_closed_eye_line`,'M -23 0 C -7 6 7 6 23 0',null,C.ink,.85));
 }
 edit('left_brow','M -51 -33 C -41 -42 -30 -43 -23 -30 C -33 -35 -41 -36 -51 -31 Z');
 edit('right_brow','M 22 -30 C 31 -44 42 -42 51 -34 L 53 -29 C 42 -35 34 -36 22 -30 Z');
 find(root,'nose').y=18.5;
 edit('nose_shape','M -8 -1 C -6 -4 5 -4 8 -1 C 7 2 3 5 0 5.5 C -3 5 -7 2 -8 -1 Z');
 find(root,'mouth').y=26;
 edit('mouth_line','M 0 -3 L -.3 3 C -4 10 -10 11 -15 7 M -.3 3 C 4 10 10 11 15 6');
 edit('cheek_left_upper','M -82 -2 C -73 -3 -61 1 -49 9 L -45 13 C -59 11 -72 8 -81 7 L -87 5 L -82 3 Z');
 edit('cheek_left_lower','M -81 17 C -71 17 -61 19 -47 23 L -42 26 C -52 30 -62 31 -71 28 L -78 23 L -74 22 Z');
 edit('cheek_right_upper','M 81 -3 C 73 -3 61 1 49 9 L 44 13 C 59 10 72 7 81 7 L 85 4 L 81 2 Z');
 edit('cheek_right_lower','M 79 16 C 69 17 57 20 45 24 L 40 27 C 53 31 64 29 73 25 L 78 21 L 75 20 Z');
 // Rounded ear tips and warmer shadowed wells, not large triangular pink stickers.
 edit('left_ear_outer','M -18 25 C -28 7 -32 -33 -28 -60 C -27 -65 -23 -66 -19 -63 C -1 -51 17 -37 32 -20 Z');
 edit('right_ear_outer','M 18 25 C 28 4 31 -33 25 -59 C 24 -64 20 -64 16 -61 C -1 -50 -20 -33 -32 -19 Z');
 edit('left_inner','M -20 12 C -27 -6 -28 -39 -23 -54 C -12 -49 8 -33 22 -16 C 3 -22 -10 -6 -20 12 Z');
 edit('right_inner','M 20 12 C 27 -8 27 -40 20 -54 C 7 -46 -10 -29 -22 -14 C -2 -22 11 -6 20 12 Z');
 const soft=(name,d,color,alpha)=>({...p(name,d,color),opacity:alpha});
 head.children.splice(3,0,g('facial_volume',0,0,[
  soft('left_temple_shadow','M -63 -45 C -74 -20 -73 3 -66 20 C -62 34 -47 42 -33 48 C -61 44 -80 28 -82 13 C -79 -5 -74 -27 -63 -45 Z','#8C4529',.17),
  soft('right_temple_shadow','M 63 -47 C 78 -24 76 1 70 18 C 65 32 51 42 37 47 C 65 41 79 25 80 13 C 76 -10 74 -30 63 -47 Z','#8C4529',.14),
  soft('forehead_warmth','M -49 -47 C -24 -69 21 -70 46 -46 C 31 -56 16 -53 5 -41 C -2 -34 -1 -17 -1 -8 C -8 -18 -8 -37 -15 -45 C -22 -53 -37 -52 -49 -47 Z','#FFE0A0',.18),
  soft('nose_bridge','M -12 -31 C -8 -20 -10 -5 -7 11 C -4 18 5 18 8 11 C 11 -5 8 -22 12 -31 C 4 -21 -4 -21 -12 -31 Z','#F8CB85',.27)
 ]));
 edit('chest','M -28 -22 C -17 -17 15 -17 27 -23 C 31 -12 27 0 24 7 L 27 6 L 20 20 L 22 20 L 13 34 L 14 27 L 6 42 L 5 36 L -2 49 L -3 42 L -9 47 L -11 36 L -15 38 L -18 25 L -23 23 L -23 16 L -28 12 L -27 6 L -31 3 C -32 -5 -31 -15 -28 -22 Z');
 body.children.splice(1,0,g('body_volume',0,0,[soft('body_left_shadow','M -36 -42 C -51 -12 -51 29 -43 58 C -34 69 -26 72 -16 75 C -41 73 -51 62 -52 43 C -50 6 -48 -23 -36 -42 Z','#8C4529',.16),soft('body_right_light','M 24 -39 C 43 -12 46 29 40 51 C 39 65 25 72 18 73 C 30 51 30 24 24 -39 Z','#F8C273',.18)]));
 // Small separable fur accents, deliberately not crossing animated joints.
 for(const [s,sign] of [['left',-1],['right',1]]){
  const cheek=g(`${s}_cheek_fur`,sign*73,16,[soft(`${s}_cheek_tuft`,`M 0 -13 L ${sign*12} -8 L ${sign*5} -6 L ${sign*13} -1 L ${sign*5} 0 L ${sign*10} 6 L 0 9 Z`,C.fur,.8)]);
  head.children.splice(head.children.indexOf(find(root,`${s}_eye`)),0,cheek);
  find(root,`${s}_ear_light`).opacity=.68;
  // Both foreleg bands belong to the shin, avoiding a stripe crossing a hinge.
  find(root,`${s}_upper_band`).opacity=0;
  find(root,`${s}_lower_front`).children.splice(1,0,p(`${s}_foreleg_top_band`,'M -15 1 C -7 6 5 7 15 0 L 15 6 C 6 12 -6 12 -15 7 Z',C.stripe));
  edit(`${s}_lower_band`,'M -13 24 C -5 27 4 28 13 23 L 12 29 C 4 33 -5 32 -12 30 Z');
  find(root,`${s}_upper_front`).children.splice(1,0,soft(`${s}_leg_volume`,'M -15 -21 C -19 -9 -17 13 -12 27 L -7 33 C -12 7 -9 -10 -6 -24 Z','#BA632F',.2));
 }
 // The tip and rings stay on their tail segments rather than floating overlays.
 find(root,'tail_base').x=96;
 for(let i=0;i<5;i++){const segment=find(root,`tail_segment_${i}`);for(const shape of segment.children.filter(n=>n.kind==='path'))shape.width+=2.5;}
 find(root,'tail_joint_2').y=-21;find(root,'tail_joint_4').y=-11;
 // Update connected endpoints, so length corrections never open a joint.
 edit('tail_fur_2','M 0 0 C -.9 -4.2 -1.7 -14.7 -2 -21');
 edit('tail_fur_4','M 0 0 C .45 -2.2 .85 -7.7 1 -11');
 find(root,'birthday_hat').y=-72;find(root,'hat_anchor').y=-72;
 for(const s of ['left','right']){const ear=find(root,`${s}_ear`),index=head.children.indexOf(ear);let child=ear;if(s==='left'){child=g('left_peek_ear',ear.x,ear.y,[ear]);ear.x=0;ear.y=0;}head.children[index]=g(`${s}_ear_follow`,0,0,[child]);}
 const response=g('head_response',0,0,head.children);head.children=[response];
}
