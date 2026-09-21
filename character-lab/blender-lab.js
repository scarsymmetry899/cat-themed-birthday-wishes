const $=s=>document.querySelector(s);
const viewer=$('#marmalade-3d');
const clips={idle:['Idle / breathing','Marmalade_IdleBreathing_Tripo'],peek:['Peeking','Marmalade_Peeking_Tripo'],look:['Looking around','Marmalade_LookingAround_Tripo'],walk:['Walking','Marmalade_Walking_Tripo']};
let current='idle',paused=false,rotating=false;
function readout(){const animations=viewer.availableAnimations||[];$('#readout').textContent=[`state: ${current}`,`clip: ${viewer.animationName||'—'}`,`speed: ${Number(viewer.timeScale||1).toFixed(2)}×`,`animations: ${animations.length}`,...animations.map(name=>`  • ${name}`)].join('\n');}
function setState(key,restart=true){current=key;const [label,clip]=clips[key];document.querySelectorAll('[data-state]').forEach(b=>b.classList.toggle('selected',b.dataset.state===key));$('#state-label').textContent=label;viewer.pause();viewer.animationName=clip;if(restart)viewer.currentTime=0;viewer.play({repetitions:Infinity});paused=false;$('#pause').textContent='Pause';readout();}
viewer.addEventListener('progress',event=>{$('#progress-bar').style.width=`${event.detail.totalProgress*100}%`;});
viewer.addEventListener('load',()=>{$('#load-status').textContent='3D asset ready';viewer.animationCrossfadeDuration=.45;setState('idle');readout();});
viewer.addEventListener('error',()=>{$('#load-status').textContent='3D asset failed to load';});
document.querySelectorAll('[data-state]').forEach(button=>button.addEventListener('click',()=>setState(button.dataset.state)));
$('#speed').addEventListener('input',event=>{viewer.timeScale=+event.target.value;$('#speed-value').textContent=`${(+event.target.value).toFixed(2)}×`;readout();});
$('#exposure').addEventListener('input',event=>{viewer.exposure=+event.target.value;$('#exposure-value').textContent=(+event.target.value).toFixed(2);});
$('#pause').addEventListener('click',()=>{paused=!paused;paused?viewer.pause():viewer.play({repetitions:Infinity});$('#pause').textContent=paused?'Play':'Pause';});
$('#restart').addEventListener('click',()=>{viewer.currentTime=0;viewer.play({repetitions:Infinity});paused=false;$('#pause').textContent='Pause';});
$('#reverse-peek').addEventListener('click',()=>{setState('peek');viewer.play({repetitions:1,pingpong:true});});
$('#phone').addEventListener('click',()=>document.body.classList.toggle('phone'));
$('#auto-rotate').addEventListener('click',event=>{rotating=!rotating;viewer.autoRotate=rotating;event.currentTarget.classList.toggle('selected',rotating);});
$('#front-view').addEventListener('click',()=>viewer.cameraOrbit='0deg 75deg auto');
$('#three-view').addEventListener('click',()=>viewer.cameraOrbit='35deg 75deg auto');
$('#side-view').addEventListener('click',()=>viewer.cameraOrbit='90deg 75deg auto');
