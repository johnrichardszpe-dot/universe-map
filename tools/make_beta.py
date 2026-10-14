# Builds beta/index.html from stable index.html + v1.4 patches (assets shared via ../assets/)
import re,sys
s=open("/workspace/pub/index.html").read()
def R(a,b,cnt=1):
    global s
    assert s.count(a)>=1,("missing",a[:70]); s=s.replace(a,b) if cnt==0 else s.replace(a,b,cnt)
R('src="assets/','src="../assets/',0)
R("<title>Interactive Universe Map","<title>[BETA] Interactive Universe Map")
# ---- CSS
R("</style>","""
#beta{position:fixed;left:50%;top:8px;transform:translateX(-50%);z-index:9;background:#b8860b;color:#000;font-weight:700;font-size:12px;padding:3px 10px;border-radius:12px;white-space:nowrap}
#beta a{color:#001a66;margin-left:6px}
#simple{position:fixed;left:50%;bottom:44px;transform:translateX(-50%);z-index:6;display:none;gap:8px;align-items:center;flex-wrap:wrap;justify-content:center;width:min(640px,94vw);box-sizing:border-box}
body.simple #simple{display:flex} body.simple #ui,body.simple #tog,body.simple #help,body.simple #legendS{display:none!important}
#simple .big{font-size:15px;padding:9px 14px;border-radius:22px;background:rgba(20,24,45,.95)} #simple .big.on{background:#2a4f9a;border-color:#7af}
#simple .tt{flex:1 1 220px;min-width:200px;font-size:13px} #simple .tt input{width:100%}
body.simple #scale{bottom:4px;padding:3px 8px;font-size:12px}
#advsw{font-size:13px} #nav button{transition:background .2s}
@media (max-width:700px){#simple{bottom:6px;gap:6px;padding:8px} #simple .big{font-size:14px;padding:7px 11px} #simple .tt{order:3;flex-basis:100%} #beta{top:56px;left:auto;right:8px;transform:none;font-size:11px} body.simple #scale{bottom:auto;top:88px;left:auto;right:8px;transform:none} body.simple #scale small{display:none} body:not(.collapsed):not(.simple) #beta{display:none}}
</style>""")
# ---- HTML: badge, simple bar, advanced switch in panel
R('<canvas id="c"></canvas>','<canvas id="c"></canvas>\n<div id="beta">BETA v1.4-beta <a href="../">back to stable v1.3</a></div>\n'
 '<div id="simple" class="panel"><button class="big on" id="sNames">&#127991; Show names</button>'
 '<div class="tt">&#9203; Time travel: <span id="sTv"></span><input type="range" id="sT" min="1" max="100" value="100"></div>'
 '<button class="big" id="sAdv" title="Show all options: layers, surveys, colours, point counts">&#9881; Advanced</button></div>')
R('<h1>Interactive Universe Map</h1>','<h1>Interactive Universe Map</h1><button id="advoff" title="Back to the simple, clean screen">&#8592; Simple mode</button><br>')
R('<div id="ver" title="What\'s new">v1.3</div>','<div id="ver" title="What\'s new">v1.4-beta</div>')
R('What\'s new in v1.3</button>','What\'s new in v1.4-beta</button>')
R('What\'s new (v1.3)','What\'s new (v1.4-beta)')
R('<li><b>Controls</b> (colours, time, layers): the &#9776; button at top right</li>','<li><b>Simple mode</b> (default): names on/off and a time-travel slider at the bottom. Tap <b>&#9881; Advanced</b> for all options (colours, surveys, layers, 724k points)</li><li><b>&#8962; Home</b> glides back to the Milky Way</li>')
R('title="Reset view">&#8962;','title="Home: glide back to the Milky Way">&#8962;')
# ---- renderer: pixel-ratio cap on phones
R("renderer.setPixelRatio(Math.min(devicePixelRatio,2));","const PHONE=matchMedia('(pointer:coarse)').matches||Math.min(screen.width,screen.height)<700;renderer.setPixelRatio(Math.min(devicePixelRatio,PHONE?1.5:2));")
R("controls.dampingFactor=0.08;","controls.dampingFactor=0.1;controls.rotateSpeed=0.8;controls.panSpeed=0.8;controls.maxDistance=20000;")
# ---- smooth camera: generic glide (position+target), cancelled by user input
R("function view(d){camera.position.set(d*0.55,d*0.45,d*0.7);controls.target.set(0,0,0);controls.update();}",
"""const HOMEDIR=new THREE.Vector3(0.55,0.45,0.7).normalize();
function view(d){camera.position.copy(HOMEDIR).multiplyScalar(d*1.0524);controls.target.set(0,0,0);controls.update();}
let anim=null;const _a=new THREE.Vector3(),_b=new THREE.Vector3(),_c=new THREE.Vector3(),_d=new THREE.Vector3(),_e=new THREE.Vector3();
const ease=k=>k<.5?4*k*k*k:1-Math.pow(-2*k+2,3)/2;
// glide camera to target tv at distance d along direction dir (default: keep current viewing direction)
function glide(tv,d,dir,ms){const t0=controls.target.clone(),p0=camera.position.clone(),d0=Math.max(1e-6,p0.distanceTo(t0)),u0=p0.clone().sub(t0).normalize(),t1=tv.clone(),u1=(dir||u0).clone().normalize();
 const T0=performance.now();ms=ms||1500;anim={step(now){const k=Math.min(1,(now-T0)/ms),e=ease(k);controls.target.lerpVectors(t0,t1,e);
  const lg=Math.exp(Math.log(d0)*(1-e)+Math.log(d)*e);_a.copy(u0).lerp(u1,e);if(_a.lengthSq()<1e-8)_a.copy(u1);_a.normalize();camera.position.copy(controls.target).addScaledVector(_a,lg);if(k>=1)anim=null;}};}
function goHome(){glide(_e.set(0,0,0),5200*1.0524,HOMEDIR,1500);}
window.goHome=goHome;""")
R('$("home").onclick=()=>view(5200);$("local").onclick=()=>view(260);','$("home").onclick=goHome;$("local").onclick=()=>glide(_e.set(0,0,0),260*1.0524,HOMEDIR,1500);')
R('function zoomBy(f){const off=camera.position.clone().sub(controls.target).multiplyScalar(f);if(off.length()<0.5||off.length()>20000)return;camera.position.copy(controls.target).add(off);}',
 'function zoomBy(f){const cur=camera.position.distanceTo(controls.target);const d=Math.min(controls.maxDistance,Math.max(controls.minDistance,(anim&&anim.zd||cur)*f));glide(controls.target,d,null,450);anim.zd=d;}')
R('$("rst").onclick=()=>view(5200);','$("rst").onclick=goHome;')
R("let anim=null;\nwindow.flyTo","window.flyTo")
i=s.index("function flyToVec(tv,d){"); j=s.index("labels.forEach(l=>{const o=document.createElement(\"option\")")
s=s[:i]+"function flyToVec(tv,d){glide(tv,d,null,1600);}\n"+s[j:]
# cancel glide when user grabs controls
R("controls.touches={ONE:THREE.TOUCH.ROTATE,TWO:THREE.TOUCH.DOLLY_PAN};","controls.touches={ONE:THREE.TOUCH.ROTATE,TWO:THREE.TOUCH.DOLLY_PAN};\ncontrols.addEventListener('start',()=>{anim=null;});canvas.addEventListener('wheel',()=>{anim=null;},{passive:true});")
# ---- keys: no per-frame allocations, clear on blur
R("function fly(){const d=camera.position.distanceTo(controls.target)*0.015,f=new THREE.Vector3();camera.getWorldDirection(f);const r=new THREE.Vector3().crossVectors(f,camera.up).normalize();const m=new THREE.Vector3();",
  "const _f=new THREE.Vector3(),_r=new THREE.Vector3(),_m=new THREE.Vector3();addEventListener('blur',()=>{for(const k in keys)keys[k]=0;});\nfunction fly(){if(!(keys.w||keys.s||keys.a||keys.d||keys.q||keys.e))return;anim=null;const d=camera.position.distanceTo(controls.target)*0.015,f=_f;camera.getWorldDirection(f);const r=_r.crossVectors(f,camera.up).normalize();const m=_m.set(0,0,0);")
R('if(e.target.tagName!="INPUT")keys','if(e.target.tagName!="INPUT"&&!e.ctrlKey&&!e.metaKey)keys')
# ---- scalebar: only touch DOM when changed
R('$("bar").style.width=(L*ppm).toFixed(0)+"px";const ly=L*3.2616;$("stxt").textContent=',
  'const bw=(L*ppm).toFixed(0)+"px";if(bw===SB.w&&L===SB.L)return;SB.w=bw;SB.L=L;$("bar").style.width=bw;const ly=L*3.2616;$("stxt").textContent=')
R("function scalebar(){","const SB={w:'',L:0};function scalebar(){")
# ---- loop: on-demand rendering + throttled labels
i=s.index("function loop(){"); j=s.index("function placeLabels(")
s=s[:i]+"""let DIRTY=2,lastLab=0,camKey="",UIR=null;const _pm=new THREE.Matrix4();window.markDirty=()=>{DIRTY=2;};
['input','change','click','keydown','resize'].forEach(ev=>addEventListener(ev,()=>{DIRTY=2;UIR=null;},true));
window.FR={n:0,r:0};
function loop(now){requestAnimationFrame(loop);now=now||performance.now();FR.n++;if(anim)anim.step(now);fly();controls.update();
 const cd=camera.position.distanceTo(controls.target),cm=camera.position.length();
 const key=camera.position.x.toFixed(5)+camera.position.y.toFixed(5)+camera.position.z.toFixed(5)+camera.quaternion.x.toFixed(6)+camera.quaternion.y.toFixed(6)+camera.quaternion.z.toFixed(6);
 const moved=key!==camKey;camKey=key;if(!moved&&!DIRTY)return; if(DIRTY)DIRTY--;
 mwMesh.scale.setScalar(Math.min(1,Math.max(0.0004,Math.min(cd,cm)*0.004)));const nr=Math.max(0.00005,Math.min(0.1,cd*0.01));if(Math.abs(camera.near-nr)>nr*0.1){camera.near=nr;camera.updateProjectionMatrix();}
 renderer.render(scene,camera);FR.r++;scalebar();
 // declutter: full collision pass at most every 120 ms while moving; otherwise just re-position placed labels
 if(!moved||now-lastLab>120){lastLab=now;placeLabels(true);}else placeLabels(false);}
function hit(a,b){return a.x<b.x+b.w&&a.x+a.w>b.x&&a.y<b.y+b.h&&a.y+a.h>b.y;}
"""+s[j:]
# placeLabels: cached UI rects, fast path reuses previous slot offsets
R('function placeLabels(){const placed=[],W=innerWidth,H=innerHeight;\n for(const id of ["nav","flyto","tog","scale","help","findb","ver","toast"]){const r=$(id).getBoundingClientRect();if(r.width)placed.push({x:r.left-3,y:r.top-3,w:r.width+6,h:r.height+6});}',
'''const LBOX=["nav","flyto","tog","scale","help","findb","ver","toast","simple","beta"];
function placeLabels(full){const W=innerWidth,H=innerHeight;
 if(!full){for(const l of labels){if(!l.vis)continue;tmp.copy(l.v).project(camera);if(!(tmp.z<1&&Math.abs(tmp.x)<1.02&&Math.abs(tmp.y)<1.02))continue;const px=(tmp.x+1)/2*W,py=(1-tmp.y)/2*H;
   l.dot.style.transform=`translate(${px|0}px,${py|0}px)`;l.el.style.transform=`translate(${(px+l.ox)|0}px,${(py+l.oy)|0}px)`;if(l.far){l.ln.setAttribute("x1",px|0);l.ln.setAttribute("y1",py|0);l.ln.setAttribute("x2",(l.ox<0?px+l.ox+l.w:px+l.ox)|0);l.ln.setAttribute("y2",(py+l.oy+l.h/2)|0);}}return;}
 if(!UIR){UIR=[];for(const id of LBOX){const el=$(id);if(!el)continue;const r=el.getBoundingClientRect();if(r.width)UIR.push({x:r.left-3,y:r.top-3,w:r.width+6,h:r.height+6});}}
 const placed=UIR.slice();if($("labels").style.display==="none")return;''')
R('if(!on){l.el.style.visibility=l.dot.style.visibility="hidden";l.ln.setAttribute("visibility","hidden");continue;}',
  'if(!on){if(l.vis!==0){l.el.style.visibility=l.dot.style.visibility="hidden";l.ln.setAttribute("visibility","hidden");}l.vis=0;continue;}')
R('if(!best){l.el.style.visibility="hidden";l.ln.setAttribute("visibility","hidden");placed.push({x:px-4,y:py-4,w:8,h:8});continue;}',
  'if(!best){l.el.style.visibility="hidden";l.ln.setAttribute("visibility","hidden");l.vis=0;placed.push({x:px-4,y:py-4,w:8,h:8});continue;}\n  l.vis=1;l.ox=best.x-px;l.oy=best.y-py;')
R('const far=Math.abs(best.y+h/2-py)>h*0.6;','const far=Math.abs(best.y+h/2-py)>h*0.6;l.far=far;')
# time sweep: smooth rAF instead of 120ms steps
R('let t=0;$("play").innerHTML="&#9632; stop";playing=setInterval(()=>{t+=1;if(t>97)t=0;$("tmin").value=Math.max(0,t-8);$("tmax").value=t+3;tupd();},120);};',
  'let T0=performance.now();$("play").innerHTML="&#9632; stop";playing=1;(function sw(now){if(!playing)return;const t=((now-T0)/1000*8)%97;$("tmin").value=Math.max(0,t-8);$("tmax").value=t+3;tupd();DIRTY=2;requestAnimationFrame(sw);})(T0);};')
R('if(playing){clearInterval(playing);playing=null;','if(playing){playing=null;')
R('$("tmin").oninput=$("tmax").oninput=tupd;tupd();','$("tmin").oninput=$("tmax").oninput=tupd;tupd();')
# tupd: range sliders are step=1 integers; allow fractional during sweep
R('<input type="range" id="tmin" min="0" max="100" value="0" step="1">','<input type="range" id="tmin" min="0" max="100" value="0" step="any">')
R('<input type="range" id="tmax" min="0" max="100" value="100" step="1">','<input type="range" id="tmax" min="0" max="100" value="100" step="any">')
# ---- Simple / Advanced mode + simple controls (before loop start)
R('loop();$("load").style.display="none";','''// ---- v1.4 Simple / Advanced mode
function setMode(adv,user){document.body.classList.toggle("simple",!adv);LS.set("umap_mode",adv?"adv":"simple");if(adv&&user)setPanel(true);UIR=null;DIRTY=2;}
$("sAdv").onclick=()=>setMode(true,1);$("advoff").onclick=()=>setMode(false,1);
function syncNames(){const on=$("Llab").checked;$("sNames").classList.toggle("on",on);$("sNames").innerHTML=(on?"&#127991; Names: on":"&#127991; Names: off");}
$("sNames").onclick=()=>{$("Llab").checked=!$("Llab").checked;$("Llab").dispatchEvent(new Event("change"));syncNames();};$("Llab").addEventListener("change",syncNames);syncNames();
function sTupd(){const v=+$("sT").value;$("tmin").value=0;$("tmax").value=v;tupd();const b=v/10;$("sTv").textContent=v>=100?"everything (up to 10 billion years ago)":b<0.15?"just our neighbourhood":"up to "+b.toFixed(1)+" billion years ago";}
$("sT").oninput=sTupd;$("tmax").addEventListener("input",()=>{$("sT").value=Math.max(1,+$("tmax").value);});sTupd();
setMode(LS.get("umap_mode")==="adv");
requestAnimationFrame(loop);$("load").style.display="none";''')
# fly-to menu: reset to placeholder; labels info click
R('LS.set("umap_seen_ver","v1.3")','LS.set("umap_seen_ver","v1.4-beta")',0)
R('LS.get("umap_seen_ver")!=="v1.3"','LS.get("umap_seen_ver")!=="v1.4-beta"')
R('t.innerHTML="New in v1.3: search 4,000+ named galaxies with &#128269; Find. <u style=\'cursor:pointer\'>What\'s new</u>";',
  't.innerHTML="BETA v1.4: smoother, simpler screen, Home glides back. <u style=\'cursor:pointer\'>What\'s new</u>";')
R("<h2>What's new</h2>\n","""<h2>What's new</h2>
<h3>v1.4-beta &middot; 14 Oct 2026 (BETA - testing before stable)</h3><ul><li><b>Simple mode</b> is now the default: a clean screen with Find, Fly to, zoom, Home, help, a big <i>Names on/off</i> button and a <i>Time travel</i> slider. Tap <b>&#9881; Advanced</b> for every option (colours, surveys, layers, 724k points). Your choice is remembered.</li>
<li><b>Home</b> now glides smoothly back to the Milky Way instead of jumping. Zoom buttons, Fly-to and search also glide; touching the map stops a glide straight away.</li>
<li><b>Smoother</b>: the map only redraws when something changes, labels are rearranged less often while moving, and phones use a lighter pixel density.</li>
<li>Fixes: zoom buttons stopped working very close in (Local Group); keys could get stuck after switching windows; time sweep was jerky.</li></ul>
""")
open("/workspace/pub/beta/index.html","w").write(s); print("ok",len(s))
