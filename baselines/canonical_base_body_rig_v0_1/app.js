(async function(){
  const manifest=window.RIG_MANIFEST || await fetch('manifest.json').then(r=>r.json());
  const canvas=document.getElementById('rigCanvas');
  const ctx=canvas.getContext('2d');
  const viewSelect=document.getElementById('viewSelect');
  const jointControls=document.getElementById('jointControls');
  const images={};
  const outlineImages={};

  const partLabels={
    pelvis:'Pelvis',mid_torso:'Waist / Mid Torso',chest:'Chest / Ribcage',
    upper_arm_L:'Upper Arm L',forearm_L:'Forearm L',hand_L:'Hand L',
    upper_arm_R:'Upper Arm R',forearm_R:'Forearm R',hand_R:'Hand R',
    thigh_L:'Thigh L',calf_L:'Calf L',foot_L:'Foot L',
    thigh_R:'Thigh R',calf_R:'Calf R',foot_R:'Foot R'
  };
  const groups={Torso:['pelvis','mid_torso','chest'],Arms:['upper_arm_L','forearm_L','hand_L','upper_arm_R','forearm_R','hand_R'],Legs:['thigh_L','calf_L','foot_L','thigh_R','calf_R','foot_R']};

  const state={viewId:'front',angles:{},scale:.44,rootRotation:0,flip:false,showPivots:true,showOutlines:false,transparent:false};
  for(const p of Object.keys(manifest.views.front.parts)) state.angles[p]=0;

  for(const [id,v] of Object.entries(manifest.views)){
    const o=document.createElement('option');o.value=id;o.textContent=v.label;viewSelect.appendChild(o);
    images[id]={};outlineImages[id]={};
    for(const [pid,p] of Object.entries(v.parts)){
      images[id][pid]=await loadImage(p.assetAligned);
      outlineImages[id][pid]=await loadImage(p.outline);
    }
  }

  buildControls(); bind(); render();

  function buildControls(){
    jointControls.innerHTML='';
    for(const [group,parts] of Object.entries(groups)){
      const wrap=document.createElement('div');wrap.className='joint-group';
      const h=document.createElement('h3');h.textContent=group;wrap.appendChild(h);
      for(const pid of parts){
        const lim=manifest.views[state.viewId].parts[pid].rotationLimitsDeg;
        const row=document.createElement('div');row.className='joint-row';
        const lab=document.createElement('label');lab.textContent=partLabels[pid];
        const input=document.createElement('input');input.type='range';input.min=lim[0];input.max=lim[1];input.step=1;input.value=state.angles[pid];input.dataset.part=pid;
        const out=document.createElement('output');out.textContent=`${state.angles[pid]}°`;
        input.addEventListener('input',()=>{state.angles[pid]=+input.value;out.textContent=`${input.value}°`;render();});
        row.append(lab,input,out);wrap.appendChild(row);
      }
      jointControls.appendChild(wrap);
    }
  }

  function bind(){
    viewSelect.addEventListener('change',()=>{state.viewId=viewSelect.value;buildControls();render();});
    document.getElementById('pivotsToggle').addEventListener('change',e=>{state.showPivots=e.target.checked;render();});
    document.getElementById('outlinesToggle').addEventListener('change',e=>{state.showOutlines=e.target.checked;render();});
    document.getElementById('transparentToggle').addEventListener('change',e=>{state.transparent=e.target.checked;render();});
    document.getElementById('scaleSlider').addEventListener('input',e=>{state.scale=+e.target.value;render();});
    document.getElementById('rootRotSlider').addEventListener('input',e=>{state.rootRotation=+e.target.value;render();});
    document.getElementById('flipToggle').addEventListener('change',e=>{state.flip=e.target.checked;render();});
    document.getElementById('resetBtn').addEventListener('click',()=>applyPreset('neutral'));
    document.getElementById('exportBtn').addEventListener('click',exportPng);
    document.getElementById('savePoseBtn').addEventListener('click',savePose);
    document.getElementById('loadPoseInput').addEventListener('change',loadPose);
    document.querySelectorAll('[data-preset]').forEach(b=>b.addEventListener('click',()=>applyPreset(b.dataset.preset)));
    canvas.addEventListener('pointerdown',pointerDown);canvas.addEventListener('pointermove',pointerMove);canvas.addEventListener('pointerup',pointerUp);canvas.addEventListener('pointercancel',pointerUp);
  }

  const presets={
    neutral:{},
    walk:{mid_torso:-5,chest:5,upper_arm_L:-22,forearm_L:24,upper_arm_R:24,forearm_R:-28,thigh_L:-18,calf_L:34,foot_L:-8,thigh_R:18,calf_R:-18,foot_R:8},
    reach:{mid_torso:5,chest:-5,upper_arm_L:-54,forearm_L:28,hand_L:-8,upper_arm_R:-28,forearm_R:-38,hand_R:12,thigh_L:8,thigh_R:-8},
    crouch:{mid_torso:10,chest:-7,upper_arm_L:-20,forearm_L:42,upper_arm_R:18,forearm_R:-40,thigh_L:30,calf_L:76,foot_L:-18,thigh_R:-28,calf_R:-72,foot_R:18},
    twist:{pelvis:-8,mid_torso:12,chest:-10,upper_arm_L:-34,forearm_L:46,upper_arm_R:30,forearm_R:-42,thigh_L:-10,thigh_R:10}
  };
  function applyPreset(name){for(const p of Object.keys(state.angles))state.angles[p]=0;Object.assign(state.angles,presets[name]||{});buildControls();render();}

  function M(a=1,b=0,c=0,d=1,e=0,f=0){return[a,b,c,d,e,f]}
  function mul(A,B){return[A[0]*B[0]+A[2]*B[1],A[1]*B[0]+A[3]*B[1],A[0]*B[2]+A[2]*B[3],A[1]*B[2]+A[3]*B[3],A[0]*B[4]+A[2]*B[5]+A[4],A[1]*B[4]+A[3]*B[5]+A[5]]}
  function tr(x,y){return M(1,0,0,1,x,y)}
  function rot(deg){const a=deg*Math.PI/180,c=Math.cos(a),s=Math.sin(a);return M(c,s,-s,c,0,0)}
  function sc(x,y){return M(x,0,0,y,0,0)}
  function around(p,deg){return mul(mul(tr(p[0],p[1]),rot(deg)),tr(-p[0],-p[1]))}
  function point(A,p){return{x:A[0]*p[0]+A[2]*p[1]+A[4],y:A[1]*p[0]+A[3]*p[1]+A[5]}}
  function setCtx(A){ctx.setTransform(A[0],A[1],A[2],A[3],A[4],A[5])}

  let handleCache=[];
  function matrices(){
    const v=manifest.views[state.viewId];const root=v.pivots.root;
    const stage=mul(mul(mul(tr(canvas.width*.5,canvas.height*.94),rot(state.rootRotation)),sc((state.flip?-1:1)*state.scale,state.scale)),tr(-root[0],-root[1]));
    const body={root:M()};
    function calc(pid){if(body[pid])return body[pid];const p=v.parts[pid];const parent=calc(p.parent);body[pid]=mul(parent,around(p.pivot,state.angles[pid]||0));return body[pid];}
    for(const pid of Object.keys(v.parts))calc(pid);
    return{v,stage,body};
  }

  function render(options={}){
    const guides=options.guides??state.showPivots;const outlines=options.outlines??state.showOutlines;
    ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,canvas.width,canvas.height);
    if(!state.transparent||options.forceBackground){
      const g=ctx.createLinearGradient(0,0,0,canvas.height);g.addColorStop(0,'#f2f4f7');g.addColorStop(1,'#dfe5ec');ctx.fillStyle=g;ctx.fillRect(0,0,canvas.width,canvas.height);
      ctx.strokeStyle='rgba(35,45,60,.08)';ctx.lineWidth=1;for(let x=0;x<canvas.width;x+=55){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,canvas.height);ctx.stroke()}for(let y=0;y<canvas.height;y+=55){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(canvas.width,y);ctx.stroke()}
    }
    const {v,stage,body}=matrices();
    const parts=Object.keys(v.parts).sort((a,b)=>v.parts[a].zIndex-v.parts[b].zIndex);
    for(const pid of parts){const A=mul(stage,body[pid]);setCtx(A);ctx.drawImage(images[state.viewId][pid],0,0);if(outlines)ctx.drawImage(outlineImages[state.viewId][pid],0,0);}
    ctx.setTransform(1,0,0,1,0,0);
    handleCache=[];
    if(guides){
      const colors={torso:'#ffd057',arm:'#54c7ff',leg:'#65dc86'};
      for(const pid of parts){const part=v.parts[pid];const parentM=part.parent==='root'?M():body[part.parent];const A=mul(stage,parentM);const q=point(A,part.pivot);let type='torso';if(pid.includes('arm')||pid.includes('forearm')||pid.includes('hand'))type='arm';if(pid.includes('thigh')||pid.includes('calf')||pid.includes('foot'))type='leg';handleCache.push({pid,x:q.x,y:q.y,parentA:A});ctx.fillStyle=colors[type];ctx.strokeStyle='#17202b';ctx.lineWidth=2;ctx.beginPath();ctx.arc(q.x,q.y,8,0,Math.PI*2);ctx.fill();ctx.stroke();}
      const neckParent=mul(stage,body.chest);const nq=point(neckParent,v.pivots.neck_socket);ctx.fillStyle='#fff';ctx.strokeStyle='#17202b';ctx.beginPath();ctx.arc(nq.x,nq.y,8,0,Math.PI*2);ctx.fill();ctx.stroke();ctx.fillStyle='#1f2937';ctx.font='13px system-ui';ctx.fillText('neck_socket',nq.x+11,nq.y-8);
    }
  }

  let drag=null;
  function canvasPoint(e){const r=canvas.getBoundingClientRect();return{x:(e.clientX-r.left)*canvas.width/r.width,y:(e.clientY-r.top)*canvas.height/r.height}}
  function pointerDown(e){const p=canvasPoint(e);let best=null,bestD=18;for(const h of handleCache){const d=Math.hypot(p.x-h.x,p.y-h.y);if(d<bestD){best=h;bestD=d}}if(!best)return;canvas.setPointerCapture(e.pointerId);drag={pid:best.pid,pivot:{x:best.x,y:best.y},startPointer:Math.atan2(p.y-best.y,p.x-best.x),startAngle:state.angles[best.pid]||0};}
  function pointerMove(e){if(!drag)return;const p=canvasPoint(e);const a=Math.atan2(p.y-drag.pivot.y,p.x-drag.pivot.x);let delta=(a-drag.startPointer)*180/Math.PI;while(delta>180)delta-=360;while(delta<-180)delta+=360;const lim=manifest.views[state.viewId].parts[drag.pid].rotationLimitsDeg;state.angles[drag.pid]=Math.max(lim[0],Math.min(lim[1],Math.round(drag.startAngle+delta)));updateControl(drag.pid);render();}
  function pointerUp(e){if(drag){try{canvas.releasePointerCapture(e.pointerId)}catch{}drag=null}}
  function updateControl(pid){const input=document.querySelector(`input[data-part="${pid}"]`);if(input){input.value=state.angles[pid];input.parentElement.querySelector('output').textContent=`${state.angles[pid]}°`;}}

  function exportPng(){const oldP=state.showPivots,oldO=state.showOutlines;render({guides:false,outlines:false});const a=document.createElement('a');a.download=`canonical-base-${state.viewId}-${Date.now()}.png`;a.href=canvas.toDataURL('image/png');a.click();state.showPivots=oldP;state.showOutlines=oldO;render();}
  function savePose(){const data={schemaVersion:manifest.schemaVersion,viewId:state.viewId,angles:state.angles,scale:state.scale,rootRotation:state.rootRotation,flip:state.flip};download(JSON.stringify(data,null,2),`canonical-body-pose-${Date.now()}.json`,'application/json');}
  async function loadPose(e){const f=e.target.files[0];if(!f)return;try{const d=JSON.parse(await f.text());if(d.viewId&&manifest.views[d.viewId]){state.viewId=d.viewId;viewSelect.value=d.viewId}Object.assign(state.angles,d.angles||{});if(typeof d.scale==='number')state.scale=d.scale;if(typeof d.rootRotation==='number')state.rootRotation=d.rootRotation;state.flip=!!d.flip;document.getElementById('scaleSlider').value=state.scale;document.getElementById('rootRotSlider').value=state.rootRotation;document.getElementById('flipToggle').checked=state.flip;buildControls();render();}catch(err){alert('Could not load pose JSON.');console.error(err)}}
  function download(text,name,type){const url=URL.createObjectURL(new Blob([text],{type}));const a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)}
  function loadImage(src){return new Promise((res,rej)=>{const i=new Image();i.onload=()=>res(i);i.onerror=rej;i.src=src})}
})();
