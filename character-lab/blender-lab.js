const $=s=>document.querySelector(s);
const viewer=$('#marmalade-3d');
const clips={idle:['Idle / breathing','Marmalade_IdleBreathing_Tripo'],peek:['Peeking','Marmalade_Peeking_Tripo'],look:['Looking around','Marmalade_LookingAround_Tripo'],walk:['Walking','Marmalade_Walking_Tripo']};
let current='idle',paused=false,rotating=false,reverseFrame=0;
function readout(){const animations=viewer.availableAnimations||[];$('#readout').textContent=[`state: ${current}`,`clip: ${viewer.animationName||'—'}`,`speed: ${Number(viewer.timeScale||1).toFixed(2)}×`,`animations: ${animations.length}`,...animations.map(name=>`  • ${name}`)].join('\n');}
function repetitionsFor(key){return key==='peek'?1:Infinity;}
function playCurrent(){viewer.play({repetitions:repetitionsFor(current)});}
function stopManualReverse(){if(reverseFrame){cancelAnimationFrame(reverseFrame);reverseFrame=0;}}
function setState(key,restart=true){stopManualReverse();current=key;const [label,clip]=clips[key];document.querySelectorAll('[data-state]').forEach(b=>b.classList.toggle('selected',b.dataset.state===key));$('#state-label').textContent=label;viewer.pause();viewer.timeScale=Math.abs(+$('#speed').value||1);viewer.animationName=clip;if(restart)viewer.currentTime=0;playCurrent();paused=false;$('#pause').textContent='Pause';readout();}
viewer.addEventListener('progress',event=>{$('#progress-bar').style.width=`${event.detail.totalProgress*100}%`;});
viewer.addEventListener('load',()=>{$('#load-status').textContent='3D asset ready';viewer.animationCrossfadeDuration=.45;setState('idle');readout();});
viewer.addEventListener('error',()=>{$('#load-status').textContent='3D asset failed to load';});
document.querySelectorAll('[data-state]').forEach(button=>button.addEventListener('click',()=>setState(button.dataset.state)));
$('#speed').addEventListener('input',event=>{viewer.timeScale=Math.sign(viewer.timeScale||1)*(+event.target.value);$('#speed-value').textContent=`${(+event.target.value).toFixed(2)}×`;readout();});
$('#exposure').addEventListener('input',event=>{viewer.exposure=+event.target.value;$('#exposure-value').textContent=(+event.target.value).toFixed(2);});
$('#pause').addEventListener('click',()=>{paused=!paused;paused?viewer.pause():playCurrent();$('#pause').textContent=paused?'Play':'Pause';});
$('#restart').addEventListener('click',()=>{stopManualReverse();viewer.timeScale=Math.abs(+$('#speed').value||1);viewer.currentTime=0;playCurrent();paused=false;$('#pause').textContent='Pause';readout();});
$('#reverse-peek').addEventListener('click',()=>{stopManualReverse();current='peek';const [label,clip]=clips.peek;document.querySelectorAll('[data-state]').forEach(b=>b.classList.toggle('selected',b.dataset.state==='peek'));$('#state-label').textContent=label;viewer.pause();viewer.animationName=clip;viewer.timeScale=Math.abs(+$('#speed').value||1);viewer.currentTime=viewer.duration||0;const duration=viewer.duration||0;const started=performance.now();const tick=now=>{const elapsed=(now-started)/1000*(+$('#speed').value||1);viewer.currentTime=Math.max(0,duration-elapsed);if(viewer.currentTime>0){reverseFrame=requestAnimationFrame(tick);}else{reverseFrame=0;}};reverseFrame=requestAnimationFrame(tick);paused=false;$('#pause').textContent='Pause';readout();});
$('#phone').addEventListener('click',()=>document.body.classList.toggle('phone'));
$('#auto-rotate').addEventListener('click',event=>{rotating=!rotating;viewer.autoRotate=rotating;event.currentTarget.classList.toggle('selected',rotating);});
// The preserved Tripo mesh carries a baked orientation correction. Map the
// human-readable buttons to the actual rendered views rather than raw angles.
$('#front-view').addEventListener('click',()=>viewer.cameraOrbit='35deg 75deg auto');
$('#three-view').addEventListener('click',()=>viewer.cameraOrbit='90deg 75deg auto');
$('#side-view').addEventListener('click',()=>viewer.cameraOrbit='0deg 75deg auto');
