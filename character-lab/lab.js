// Official low-level Rive runtime: one native machine, explicit review clock.
const $=s=>document.querySelector(s),canvas=$('#character'),stage=$('#stage');
const names=['Idle / breathing','Peeking','Looking around','Walking / trotting'];
let rc,file,board,machine,renderer,inputs={},nodes={},state=0,paused=false,token=0,time=0,walkTime=0,last=0,request=0,fps=0,frameCount=0,measureStart=0,loaded=false;
const target={lookX:50,lookY:50,moveSpeed:0},trails={},previous={},contactReadout={};
const pawNames=['left_paw','right_paw','left_rear_paw','right_rear_paw'];
$('#walk-test').insertAdjacentHTML('afterend','<button id="gait-test">Walk ↔ trot</button>');
stage.insertAdjacentHTML('beforeend',`<svg class="reference-layer" viewBox="0 0 300 370" aria-hidden="true"><image href="../assets/character/marmalade-master-sheet-v1.png" width="1536" height="1024"/></svg><svg class="landmark-layer" viewBox="0 0 300 370" aria-hidden="true"><path d="M100 146H223 M130 167H198 M116 204H210 M106 218H220 M96 278H111 M100 337H223 M106 209V233 M220 209V233"/><text x="224" y="146">eyes</text><text x="201" y="166">nose</text><text x="214" y="204">chin</text><text x="223" y="219">shoulders</text><text x="49" y="278">tail root</text><text x="224" y="337">paws</text></svg><svg class="contact-layer" viewBox="0 0 300 370" aria-hidden="true"></svg>`);
if(location.hostname==='127.0.0.1')$('.fidelity').insertAdjacentHTML('beforeend','<button id="record-motion">Record 8 s motion evidence at 1×</button><p id="record-status" class="note"></p><video id="motion-replay" controls loop playsinline style="max-width:320px;display:none"></video>');
function set(n,v){if(inputs[n])inputs[n].value=v;}
function action(n){if(n!==state){walkTime=0;for(const p of pawNames){trails[p]=[];delete previous[p];}}state=n;set('state',n);$('#state-label').textContent=names[n];stage.classList.toggle('peeking',n===1);document.querySelectorAll('[data-state]').forEach(b=>b.classList.toggle('selected',+b.dataset.state===n));}
function sync(){
 target.moveSpeed=+$('#speed').value;set('scrollProgress',+$('#peek').value);set('hasHat',$('#hat').checked);set('blinkEnabled',$('#blink').checked);set('expression',+$('#expression').value);set('showMarkings',$('#markings').checked);
 target.lookX=(+$('#look-x').value+1)*50;target.lookY=(+$('#look-y').value+1)*50;
 for(const [id,v] of [['speed',$('#speed').value+'%'],['peek',$('#peek').value+'%'],['x',(+$('#look-x').value).toFixed(2)],['y',(+$('#look-y').value).toFixed(2)],['rate',$('#rate').value+'×'],['reference',$('#reference-opacity').value+'%']])$('#'+id+'-value').value=v;
 stage.classList.toggle('guides',$('#debug').checked);stage.classList.toggle('reference-on',$('#reference').checked);stage.classList.toggle('landmarks-on',$('#landmarks').checked);stage.classList.toggle('silhouette',$('#silhouette').checked);$('.reference-layer').style.opacity=+$('#reference-opacity').value/100;
 if(paused&&loaded){machine.advanceAndApply(0);board.advance(0);draw();}
}
function resize(){const rect=canvas.getBoundingClientRect(),dpr=devicePixelRatio*+$('#render-scale').value;canvas.width=Math.round(rect.width*dpr);canvas.height=Math.round(rect.height*dpr);if(loaded)draw();}
function draw(){renderer.beginFrame();renderer.save();renderer.align(rc.Fit.contain,rc.Alignment.center,{minX:0,minY:0,maxX:canvas.width,maxY:canvas.height},board.bounds);board.draw(renderer);renderer.restore();}
function setPause(value){paused=value;$('#pause').textContent=paused?'Play':'Pause';last=0;}
function advance(dt){
 time+=dt;if(state===3)walkTime+=dt;
 set('moveSpeed',inputs.moveSpeed.value+(target.moveSpeed-inputs.moveSpeed.value)*(1-Math.exp(-dt/.28)));
 const alpha=1-Math.exp(-dt/0.13);for(const n of ['lookX','lookY'])set(n,inputs[n].value+(target[n]-inputs[n].value)*alpha);
 set('headLook',inputs.headLook.value+(inputs.lookX.value-inputs.headLook.value)*(1-Math.exp(-dt/.3)));
 set('earLook',inputs.earLook.value+(inputs.headLook.value-inputs.earLook.value)*(1-Math.exp(-dt/.2)));
 machine.advanceAndApply(dt);board.advance(dt);
}
function nodePoint(name,tip=0){const m=nodes[name].worldTransform();const point={x:m.tx+m.yx*tip,y:m.ty+m.yy*tip};m.delete();return point;}
function diagnostics(dt){
 const show=$('#contacts').checked,showTrails=$('#trails').checked,joints=$('#debug').checked;let svg=show?'<path d="M75 337H241" stroke="#927455" stroke-width=".6"/>':'';
 for(const [index,name] of pawNames.entries()){
  const point=nodePoint(name,name.includes('rear')?10:13),old=previous[name];
  const velocity=old&&dt>0?Math.hypot(point.x-old.x,point.y-old.y)/dt:0;previous[name]=point;
  const floor=state===1?260:(name.includes('rear')?332:336),contact=Math.abs(point.y-floor)<1.3&&velocity<7&&!(state===1&&name.includes('rear'));
  contactReadout[name]=`${contact?'contact':'swing'} (${point.x.toFixed(1)}, ${point.y.toFixed(1)}) ${velocity.toFixed(1)} u/s`;
  trails[name]??=[];if(dt>0){trails[name].push(point);if(trails[name].length>100)trails[name].shift();}
  const color=['#247e78','#c36b42','#657eaa','#93679b'][index];
  if(showTrails)svg+=`<polyline points="${trails[name].map(p=>`${p.x},${p.y}`).join(' ')}" fill="none" stroke="${color}" stroke-width=".65"/>`;
  if(show)svg+=`<circle cx="${point.x}" cy="${point.y}" r="3" fill="${contact?'#269884':'#d87c50'}"/><text x="${point.x+4}" y="${point.y-4}">${name.replace('left','L').replace('right','R').replace('_paw','')}</text>`;
 }
 if(joints)for(const name of ['head_group','body_group','left_upper_front','right_upper_front','left_lower_front','right_lower_front','tail_base']){const p=nodePoint(name);svg+=`<circle cx="${p.x}" cy="${p.y}" r="2.2" fill="none" stroke="#287a81" stroke-width=".6"/>`;}
 $('.contact-layer').innerHTML=svg;
 // Replace the old static pivot artwork; native transforms above are authoritative.
 $('#debug-overlay').style.display='none';
}
function frame(now){
 const elapsed=last?Math.min(.05,(now-last)/1000):0;last=now;const dt=paused||document.hidden?0:elapsed*+$('#rate').value;
 if(dt)advance(dt);draw();diagnostics(dt);frameCount++;
 if(now-measureStart>1000){fps=Math.round(frameCount*1000/(now-measureStart));frameCount=0;measureStart=now;}
 const cycle=.95+(.6-.95)*+$('#speed').value/100;
 $('#readout').textContent=`Marmalade_Main / ${names[state]}\n${Object.entries(inputs).map(([n,i])=>`${n}: ${typeof i.value==='number'?i.value.toFixed(2):i.value}`).join(' · ')}\nClock ${time.toFixed(2)} s · ${paused?'Paused':fps+' draw callbacks/s'} · rate ${$('#rate').value}× · locomotion loops ≈${Math.floor(walkTime/cycle)}\nCanvas ${canvas.width} × ${canvas.height} · actual DPR ${devicePixelRatio.toFixed(2)} · raster multiplier ${$('#render-scale').value}\n${Object.entries(contactReadout).map(([n,v])=>`${n}: ${v}`).join('\n')}`;
 request=rc.requestAnimationFrame(frame);
}
async function start(){
 rive.RuntimeLoader.setWasmUrl(new URL('vendor/rive.wasm',location.href).href);rive.RuntimeLoader.setWasmFallbackUrl(null);rc=await rive.RuntimeLoader.awaitInstance();
 const response=await fetch('../assets/character/production/marmalade-foundation.riv',{cache:'no-store'});if(!response.ok)throw Error('Rive asset HTTP '+response.status);
 file=await rc.load(new Uint8Array(await response.arrayBuffer()));board=file.defaultArtboard();renderer=rc.makeRenderer(canvas);resetMachine();
 for(const name of [...pawNames,'head_group','body_group','left_upper_front','right_upper_front','left_lower_front','right_lower_front','tail_base'])nodes[name]=board.node(name);
 loaded=true;resize();sync();$('#status').textContent='Native Rive ready';setPause(matchMedia('(prefers-reduced-motion: reduce)').matches);request=rc.requestAnimationFrame(frame);
}
function resetMachine(){machine?.delete();machine=new rc.StateMachineInstance(board.stateMachineByName('Marmalade_Main'),board);inputs={};for(let i=0;i<machine.inputCount();i++){const item=machine.input(i);inputs[item.name]=['blinkEnabled','hasHat','showMarkings'].includes(item.name)?item.asBool():item.asNumber();}time=0;walkTime=0;sync();set('state',state);machine.advanceAndApply(0);board.advance(0);for(const p of pawNames){trails[p]=[];delete previous[p];}}
new ResizeObserver(resize).observe(canvas);addEventListener('resize',resize);$('#render-scale').addEventListener('change',resize);
document.querySelectorAll('[data-state]').forEach(b=>b.onclick=()=>{token++;action(+b.dataset.state);});document.querySelectorAll('input,select').forEach(el=>el.addEventListener('input',sync));$('#peek').addEventListener('input',()=>{token++;action(1);});
$('#pause').onclick=()=>setPause(!paused);$('#step').onclick=()=>{if(!loaded)return;setPause(true);advance(1/60);draw();diagnostics(1/60);};$('#restart').onclick=()=>{token++;resetMachine();};
$('#blink-pose').onclick=()=>{token++;state=0;action(0);$('#blink').checked=true;setPause(true);resetMachine();for(let i=0;i<143;i++)advance(1/60);draw();};
$('#mobile').onclick=()=>{$('.viewer').classList.toggle('phone');$('#mobile').textContent=$('.viewer').classList.contains('phone')?'Full frame':'Phone frame';};
const wait=ms=>new Promise(resolve=>{const start=time,t=token;function poll(){if(token!==t||(time-start)*1000>=ms)resolve();else requestAnimationFrame(poll);}poll();});
async function ramp(from,to,ms,t){const start=time;while(token===t){const p=Math.min(1,(time-start)*1000/ms),ease=p*p*(3-2*p);$('#peek').value=from+(to-from)*ease;sync();if(p===1)return;await new Promise(requestAnimationFrame);}}
async function test(which){const t=++token;setPause(false);$('#test-status').textContent='Running '+which+'…';if(which==='walk'){action(0);await wait(900);if(t!==token)return;action(3);await wait(3500);if(t!==token)return;action(0);}else{action(1);$('#peek').value=0;sync();await wait(700);if(t!==token)return;await ramp(0,100,3400,t);await wait(900);if(t!==token)return;if(which==='reverse'){await ramp(100,0,3400,t);await ramp(0,100,3400,t);}else action(2);}if(t===token)$('#test-status').textContent='Sequence complete.';}
$('#peek-test').onclick=()=>test('peek');$('#walk-test').onclick=()=>test('walk');$('#reverse-test').onclick=()=>test('reverse');
$('#gait-test').onclick=async()=>{const t=++token;setPause(false);action(3);$('#test-status').textContent='Running gait blend…';for(const [speed,hold] of [[0,1200],[100,2200],[0,2200]]){if(t!==token)return;$('#speed').value=speed;sync();await wait(hold);}if(t===token)$('#test-status').textContent='Gait blend complete.';};
function gaze(v){action(2);$('#look-x').value=v;sync();}$('#gaze-left').onclick=()=>gaze(-1);$('#gaze-right').onclick=()=>gaze(1);
$('#reset').onclick=()=>{token++;action(0);for(const [id,v] of [['look-x',0],['look-y',0],['peek',100],['speed',0],['expression',0],['rate',1]])$('#'+id).value=v;$('#hat').checked=false;$('#track').checked=false;$('#blink').checked=true;$('#markings').checked=true;sync();setPause(false);};
const deadzone=v=>Math.abs(v)<.12?0:Math.sign(v)*(Math.abs(v)-.12)/.88;
canvas.addEventListener('pointermove',e=>{if(!$('#track').checked)return;const r=canvas.getBoundingClientRect();$('#look-x').value=deadzone(Math.max(-1,Math.min(1,(e.clientX-r.left)/r.width*2-1)));$('#look-y').value=deadzone(Math.max(-1,Math.min(1,(e.clientY-r.top)/r.height*2-1)));sync();});
document.addEventListener('visibilitychange',()=>{last=0;});addEventListener('pagehide',()=>{if(rc)rc.cancelAnimationFrame(request);machine?.delete();board?.delete();file?.delete();renderer?.delete();});
start().catch(error=>{$('#status').textContent='Rive failed to load';console.error(error);});
if($('#record-motion'))$('#record-motion').onclick=async()=>{
 const button=$('#record-motion');if(!loaded||!canvas.captureStream||!window.MediaRecorder)return;
 button.disabled=true;$('#rate').value=1;sync();setPause(false);
 const stream=canvas.captureStream(60),chunks=[],metrics=[],recordState=state,recordTest=$('#test-status').textContent;
 const media=new MediaRecorder(stream,{mimeType:'video/webm'});
 const sample=setInterval(()=>metrics.push({time,state,moveSpeed:inputs.moveSpeed.value,paws:{...contactReadout}}),100);
 media.ondataavailable=e=>{if(e.data.size)chunks.push(e.data);};
 media.onstop=async()=>{clearInterval(sample);stream.getTracks().forEach(t=>t.stop());const blob=new Blob(chunks,{type:'video/webm'}),video=$('#motion-replay');if(video.dataset.blob)URL.revokeObjectURL(video.dataset.blob);video.src=URL.createObjectURL(blob);video.dataset.blob=video.src;video.style.display='block';try{const name=recordTest.includes('gait')?'gait-blend':recordTest.includes('reverse')?'peek-reverse':recordState===3?(+$('#speed').value>50?'trot':'walk'):'state-'+recordState;const response=await fetch('/__qa__/'+name,{method:'POST',headers:{'Content-Type':'video/webm'},body:blob});if(!response.ok)throw Error('Save failed');await fetch('/__qa__/'+name+'-metrics',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(metrics,null,2)});$('#record-status').textContent='Saved real-time '+name+' capture and live paw metrics under docs/qa/phase-2-refinement/.';}catch(e){$('#record-status').textContent=e.message;}button.disabled=false;};
 media.start();$('#record-status').textContent='Recording live native Rive at 1× for eight seconds…';setTimeout(()=>media.stop(),8000);
};
