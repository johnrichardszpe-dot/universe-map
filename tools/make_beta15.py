import json
s=open("/workspace/pub/tools/beta_base_v1.4.html").read()
def R(a,b,all_=False):
    global s
    assert a in s,("missing",a[:80]); s=s.replace(a,b) if all_ else s.replace(a,b,1)
R("v1.4-beta","v1.5-beta",True)
R("BETA (same as stable v1.4 - no beta changes yet)","BETA v1.5-beta")
R('LS.get("umap_seen_ver")!=="v1.5-beta"','LS.get("umap_seen_ver")!=="v1.5-beta"')
R("BETA v1.4: smoother, simpler screen, Home glides back.","BETA v1.5: tap any galaxy, enter the Milky Way (Solar System + 6,400 exoplanets), measure distances.")
R("</style>","""
body.ss #flyto,body.ss #findb,body.ss #simple .tt,body.ss #sNames,body.ss #sAdv,body.ss #ui,body.ss #tog,body.ss #labels,body.ss #sMW,body.ss #help{display:none!important}
body.ss #simple{display:flex;width:auto} #mwback,#slegend,#slabels{display:none} body.ss #mwback{display:block} body.ss #slegend{display:block} body.ss #slabels{display:block}
#mwback{position:fixed;left:10px;top:10px;z-index:7;font-size:15px;padding:9px 14px;border-radius:22px;background:#2a4f9a;border-color:#7af}
#slegend{right:10px;bottom:60px;width:250px;font-size:12px;z-index:5} #slegend i{width:10px;height:10px;border-radius:50%;display:inline-block;margin-right:5px}
.slab{color:#ffe9a8}
#route{left:64px;top:56px;width:310px;max-height:45vh;overflow:auto;display:none;z-index:8;font-size:13px} #route #wpl div{border-bottom:1px solid #223;padding:2px 0}
#route select{max-width:140px;background:#223;color:#dde;border:1px solid #446}
@media (max-width:700px){#route{left:8px;right:8px;width:auto;top:128px;max-height:30vh} #slegend{display:none!important} #simple .big{font-size:12.5px;padding:6px 8px;white-space:nowrap} #simple{gap:5px;padding:6px}}
</style>""")
R('<button class="big" id="sAdv"','<button class="big" id="sMeas" title="Measure distances between points; build a route">&#128207; Measure</button><button class="big" id="sMW" title="Zoom into our own galaxy: Solar System and known exoplanets">&#127756; Milky Way</button><button class="big" id="sAdv"')
R('<button id="aboutb">','<button id="measp">&#128207; Measure / route</button><button id="mwp">&#127756; Enter the Milky Way</button><button id="aboutb">')
R('<div id="info" class="panel"></div>','<div id="info" class="panel"></div><div id="route" class="panel"></div><button id="mwback">&#9664; Back to universe</button><div id="slegend" class="panel"></div><div id="slabels"></div>')
R('const LBOX=["nav","flyto","tog","scale","help","findb","ver","toast","simple","beta"];','const LBOX=["nav","flyto","tog","scale","help","findb","ver","toast","simple","beta","route"];')
R("renderer.render(scene,camera);FR.r++;scalebar();","renderer.render(MODE==='S'?SS.scene:scene,camera);FR.r++;scalebar();if(MODE==='S'){SS.labels();return;}")
R("function goHome(){","function goHome(){if(MODE==='S')return glide(_e.set(0,0,0),1.4,new THREE.Vector3(0.4,0.6,1.2),1500);")
R("const SB={w:'',L:0};function scalebar(){const d=camera.position.distanceTo(controls.target),H=innerHeight,wh=2*d*Math.tan(camera.fov*Math.PI/360),ppm=H/wh;\n const want=160/ppm,p=Math.pow(10,Math.floor(Math.log10(want)));let L=[1,2,5,10].map(k=>k*p).filter(v=>v<=want).pop()||p;",
 "const SB={w:'',L:0};function scalebar(){const d=camera.position.distanceTo(controls.target),H=innerHeight,wh=2*d*Math.tan(camera.fov*Math.PI/360),ppm=H/wh;\n const want=160/ppm,p=Math.pow(10,Math.floor(Math.log10(want)));let L=[1,2,5,10].map(k=>k*p).filter(v=>v<=want).pop()||p;\n if(MODE==='S'){const bw=(L*ppm).toFixed(0)+'px',key=bw+L+(camera.position.length()<4);if(SB.w===key)return;SB.w=key;$('bar').style.width=bw;const ly=L*3.26156;$('stxt').textContent=(ly<10?+ly.toPrecision(2):Math.round(ly).toLocaleString())+' light-years ('+(+L.toPrecision(2))+' pc)'+(camera.position.length()<4?' - Solar System NOT to scale':'');return;}")
js=open("/workspace/v15/v15.js").read().replace("__COSMO__",open("/workspace/v15/cosmo.json").read())
R("// ---- v1.4 Simple / Advanced mode",js+"\n// ---- v1.4 Simple / Advanced mode")
R('<li><b>&#8962; Home</b> glides back to the Milky Way</li>','<li><b>&#8962; Home</b> glides back to the Milky Way</li><li><b>Tap a dot</b> for that galaxy\'s facts; <b>&#128207; Measure</b> to measure distances; <b>&#127756; Milky Way</b> for the Solar System and exoplanets</li>')
R("<h2>What's new</h2>\n","""<h2>What's new</h2>
<h3>v1.5-beta &middot; 14 Oct 2026 (BETA - testing before stable)</h3><ul>
<li><b>Tap any galaxy dot</b>: it is highlighted, the view glides to it, and an info box shows its survey, redshift, distance (Mpc and light-years), lookback time and sky position, plus the closest named object in the index. (A quick tap selects; dragging still rotates.)</li>
<li><b>&#127756; Enter the Milky Way</b>: the Sun, 8 planets and dwarf planets Pluto and Ceres at their real positions on 14 Oct 2026 (JPL Horizons), with facts from the NASA Planetary Fact Sheet. Around them, 4,814 real stars hosting 6,417 confirmed exoplanets from the NASA Exoplanet Archive, at their true sky positions and distances. Tap a planet or star for its known facts ('unknown' where not measured). The Solar System is enlarged so you can see it (not to scale).</li>
<li><b>&#128207; Measure</b>: tap points in order to see each leg and the total distance (Mpc and light-years; AU and light-years in the Milky Way view). Undo, clear, save routes on this device, and fly the route.</li></ul>
""")
R("<h3>Galaxy name index (search)</h3>","""<h3>Milky Way view (v1.5)</h3><p>Planet facts: NASA Planetary Fact Sheet, NSSDCA/Goddard (D. R. Williams, updated 18 Mar 2025), nssdc.gsfc.nasa.gov/planetary/factsheet/, and the per-planet fact sheets for atmospheres. Ceres: NASA Dawn mission results and JPL Horizons (radius 469.7 km, rotation 9.074 h). Planet positions: JPL Horizons heliocentric vectors (ICRF) for 14 Oct 2026. Earth's species estimate: Mora et al. 2011, PLoS Biology 9(8): e1001127 (about 8.7 million eukaryote species). Exoplanets: NASA Exoplanet Archive, Planetary Systems Composite Parameters table (pscomppars), downloaded via TAP on 14 Oct 2026: 6,445 confirmed planets, 6,417 with a known host distance, around 4,814 host stars. This research has made use of the NASA Exoplanet Archive, which is operated by the California Institute of Technology under contract with NASA under the Exoplanet Exploration Program. Planet colours are size classes from the measured radius. Dot info (redshift, lookback time) is worked back from each galaxy's stored 3D position with the Planck 2018 model.</p>
<h3>Galaxy name index (search)</h3>""")
open("/workspace/pub/beta/index.html","w").write(s);print("ok",len(s))
