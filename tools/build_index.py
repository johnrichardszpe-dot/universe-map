"""Build the searchable galaxy name index for the universe map.
Sources: UNGC (Karachentsev+2013, VizieR J/AJ/145/101), SIMBAD TAP (names, Messier, bright galaxies B<13, Abell clusters, named groups/clusters, distance measurements),
curated superclusters/walls/voids (literature, approximate). Coordinates: equatorial (x,y,z) -> map (x, z, -y), comoving Mpc (Planck18) as in the map."""
import csv, json, re, sys, numpy as np
sys.path.insert(0,"/workspace/galaxy/v3"); from c3 import z2r
C=299792.458
def sph(ra,dec,d):
    ra,dec=np.radians(ra),np.radians(dec); x,y,z=d*np.cos(dec)*np.cos(ra),d*np.cos(dec)*np.sin(ra),d*np.sin(dec); return [round(x,3),round(z,3),round(-y,3)]
def clean(s): return re.sub(r"\s+"," ",s.replace("NAME ","")).strip()
OT={"G":"galaxy","AGN":"galaxy with active nucleus","SyG":"Seyfert galaxy","Sy1":"Seyfert galaxy","Sy2":"Seyfert galaxy","LIN":"LINER galaxy","SBG":"starburst galaxy","GiG":"galaxy in a group","GiP":"galaxy in a pair","BiC":"brightest galaxy in a cluster","LSB":"low surface brightness galaxy","EmG":"emission-line galaxy","H2G":"HII galaxy","rG":"radio galaxy","GiC":"galaxy in a cluster","bCG":"blue compact galaxy","IG":"interacting galaxies","PaG":"pair of galaxies","G?":"possible galaxy","Sy":"Seyfert galaxy","ClG":"galaxy cluster","GrG":"group of galaxies","CGG":"compact group of galaxies","SCG":"supercluster"}
E={}  # key -> entry
def add(key,name,group,typ,ra,dec,d,dm,z=None,alias=None,note=None):
    if d is None or not np.isfinite(d) or d<=0 or d>4800: return
    e=E.get(key)
    if e is None: e=E[key]=dict(n=name,a=[],g=group,t=typ,ra=round(ra,4),dec=round(dec,4),d=round(d,3),m=dm,z=None if z is None else round(z,5),p=sph(ra,dec,d))
    if note: e["note"]=note
    if alias and alias!=e["n"] and alias not in e["a"]: e["a"].append(alias)
    return e
# --- measured distances (SIMBAD mesDistance, non-redshift methods, median)
md={}
for r in csv.DictReader(open("mesdist.csv")):
    if "redshift" in (r["method"] or "") or not r["dist"]: continue
    f={"Mpc":1,"kpc":1e-3,"pc":1e-6}.get(r["unit"].strip()); 
    if f: md.setdefault(clean(r["main_id"]),[]).append(float(r["dist"])*f)
md={k:float(np.median(v)) for k,v in md.items()}
# --- UNGC Local Volume (measured distances)
def hms(s,deg=False):
    p=[float(x) for x in s.replace("+"," +").split()]; sgn=-1 if s.strip().startswith("-") else 1; p=[abs(x) for x in p]
    v=p[0]+p[1]/60+p[2]/3600; return sgn*v if deg else v*15
ungc=[]
for line in open("ungc.tsv"):
    if line.startswith("#") or not line.strip(): continue
    c=line.rstrip("\n").split("\t")
    if c[0].strip() in ("Name","") or c[0].startswith("-"): continue
    try: ra,dec,d=hms(c[1]),hms(c[2],True),float(c[3])
    except: continue
    nm=c[0].strip(); nm=re.sub(r"^MESSIER0*(\d+)",r"M \1",nm); nm=re.sub(r"^(NGC|IC|UGC)0*(\d)",r"\1 \2",nm)
    ungc.append((nm,ra,dec,d,c[4].strip()))
for n,ra,dec,d,f in ungc:
    g="Local Group" if d<1.6 else "Nearby galaxies (Local Volume)"
    add("U:"+n,n,g,"galaxy",ra,dec,d,f"measured ({f})" if f else "measured")
U=np.array([[u[1],u[2]] for u in ungc]); Uk=["U:"+u[0] for u in ungc]
def near_ungc(ra,dec):
    dd=np.hypot((U[:,0]-ra)*np.cos(np.radians(dec)),U[:,1]-dec); i=int(np.argmin(dd)); return Uk[i] if dd[i]<0.03 else None
def dist_for(mid,z):
    if mid in md and (z is None or z*C<3000): return md[mid],"measured (median of SIMBAD distances)"
    if z is not None and z*C>800 and z<1.6: return float(z2r(z)),"from redshift (Planck18)"
    if mid in md: return md[mid],"measured (median of SIMBAD distances)"
    return None,None
def galrow(r,group,alias=None):
    if not r.get("ra") or not r.get("dec"): return
    mid=clean(r["main_id"]); ra,dec=float(r["ra"]),float(r["dec"]); z=float(r["rvz_redshift"]) if r.get("rvz_redshift") else None
    k=near_ungc(ra,dec)
    if k:  # use the Local Volume entry (better distance), add alias/upgrade group
        e=E[k]; nm=alias or mid
        if nm!=e["n"] and nm not in e["a"]: e["a"].append(nm)
        if mid!=e["n"] and mid not in e["a"]: e["a"].append(mid)
        if group.startswith("Messier") and e["g"]!="Local Group": e["g"]=group
        return
    d,m=dist_for(mid,z); add("S:"+mid,mid,group,OT.get(r["otype"],"galaxy"),ra,dec,d,m,z,alias)
for r in csv.DictReader(open("messier.csv")): galrow(r,"Messier & famous galaxies",clean(r["id"]))
for r in csv.DictReader(open("names.csv")):
    nm=clean(r["id"]); 
    if re.search(r"B\d{4}|J\d{4}|\d{4}[+-]\d{2}",nm): continue   # skip catalogue-like 'names'
    mid=clean(r["main_id"])
    if "S:"+mid in E: E["S:"+mid]["a"].append(nm) if nm not in E["S:"+mid]["a"] else None; continue
    galrow(r,"Messier & famous galaxies",nm)
for r in csv.DictReader(open("bright.csv")): 
    if "S:"+clean(r["main_id"]) in E: continue
    galrow(r,"Bright NGC/IC galaxies")
# rename entries that have a famous common name: show "Common (M nn)"
for e in E.values():
    al=[a for a in e["a"] if not re.match(r"^(M|NGC|IC|UGC|PGC|ESO|MCG)\s?\d",a)]
    if e["g"]!="Bright NGC/IC galaxies" and al and re.match(r"^(M|NGC|IC|UGC|PGC|ESO)\s?\d",e["n"]):
        old=e["n"]; e["n"]=al[0]; e["a"]=[a for a in e["a"] if a!=al[0]]+[old]
# --- clusters
for r in csv.DictReader(open("abell.csv")):
    z=float(r["rvz_redshift"]); 
    if z*C<1500 or not r["ra"]: continue
    mid=clean(r["main_id"]).replace("ACO","Abell"); add("C:"+mid,mid,"Galaxy clusters","galaxy cluster",float(r["ra"]),float(r["dec"]),float(z2r(z)),"from redshift (Planck18)",z)
for r in csv.DictReader(open("namedcl.csv")):
    z=float(r["rvz_redshift"]); mid=clean(r["main_id"]); nm=clean(r["id"])
    if not r["ra"] or z*C<300 or re.search(r"\d{4}[+-]",nm): continue
    grp="Superclusters" if r["otype"]=="SCG" else "Galaxy clusters"
    add("C:"+mid,mid,grp,OT.get(r["otype"],"group"),float(r["ra"]),float(r["dec"]),float(z2r(z)),"from redshift (Planck18)",z,nm)
# --- curated (approximate) large structures
CUR=[("Great Attractor (Norma Cluster, Abell 3627)","Superclusters",243.89,-60.87,0.0163,"The gravitational 'pull' toward which the Milky Way and its neighbours are moving; centred near the Norma Cluster, partly hidden behind our galaxy's dust. Position approximate."),
 ("Perseus–Pisces Supercluster (approx.)","Superclusters",30.0,35.0,0.017,"A long chain of galaxy clusters including the Perseus Cluster. Marker = rough centre."),
 ("Hercules Supercluster (approx.)","Superclusters",241.3,17.7,0.037,"Group of clusters around Abell 2151/2147. Marker = rough centre."),
 ("Horologium–Reticulum Supercluster (approx.)","Superclusters",49.0,-50.0,0.063,"One of the largest superclusters in the nearby universe. Marker = rough centre."),
 ("Corona Borealis Supercluster (approx.)","Superclusters",232.0,29.0,0.07,"A dense supercluster of rich clusters. Marker = rough centre."),
 ("Pisces–Cetus Supercluster Complex (approx.)","Superclusters",10.0,-10.0,0.06,"A huge filament of superclusters that may include our Laniakea. Marker = rough centre."),
 ("Laniakea Supercluster (our home, approx.)","Superclusters",243.89,-60.87,0.0163,"Our home supercluster (Tully et al. 2014), about 160 Mpc across; this marker is at its gravitational centre near the Great Attractor."),
 ("Boötes Void","Walls & voids",218.0,46.0,0.052,"A huge, nearly empty bubble about 100 million light-years across, found in 1981. Marker = approximate centre."),
 ("Sculptor Wall (approx.)","Walls & voids",0.0,-30.0,0.03,"A sheet of galaxies in the southern sky. Marker = rough centre.")]
for n,g,ra,dec,z,note in CUR: add("X:"+n,n,g,"large-scale structure",ra,dec,float(z2r(z)),"approximate (literature)",z,note=note)
S=json.load(open("/workspace/pub/assets/structures.js").read().split("=",1)[1].rstrip(";\n") if False else "[]") if False else None
txt=open("/workspace/pub/assets/structures.js").read(); st=json.loads(txt[txt.index("["):txt.rindex("]")+1])
for s in st:
    g="Walls & voids" if "Wall" in s["name"] else ("Superclusters" if "Supercluster" in s["name"] else "Galaxy clusters")
    add("X:"+s["name"],s["name"],g,"large-scale structure" if g!="Galaxy clusters" else "galaxy cluster",s["ra"],s["dec"],s["d"],"from redshift (Planck18)" if not s["approx"] else "approximate (literature)",s["z"],note=s["info"])
# merge duplicate clusters/structures (same place)
keys=[k for k in E if k[0] in "CX"]; drop=set()
for i,a in enumerate(keys):
    if a in drop: continue
    for b in keys[i+1:]:
        if b in drop: continue
        A,B=E[a],E[b]
        if abs(A["d"]-B["d"])<6 and np.hypot((A["ra"]-B["ra"])*np.cos(np.radians(A["dec"])),A["dec"]-B["dec"])<0.15 and A["g"]==B["g"]:
            keep,lose=(a,b) if (a[0]=="X" or (b[0]!="X" and not re.match(r"^(ACO|Abell)",A["n"]))) else (b,a)
            E[keep]["a"]+= [E[lose]["n"]]+E[lose]["a"]; drop.add(lose)
for k in drop: del E[k]
for e in E.values(): e["n"]=e["n"].replace("ACO ","Abell "); e["a"]=sorted(set(x.replace("ACO ","Abell ") for x in e["a"] if x!=e["n"]))
OV={"M 31":"Andromeda Galaxy (M31)","M 33":"Triangulum Galaxy (M33)","LMC":"Large Magellanic Cloud","SMC":"Small Magellanic Cloud","M 87":"M87 (Virgo A)","NGC 5128":"Centaurus A (NGC 5128)",
 "M 51":"Whirlpool Galaxy (M51)","M 104":"Sombrero Galaxy (M104)","M 81":"Bode's Galaxy (M81)","M 82":"Cigar Galaxy (M82)","M 101":"Pinwheel Galaxy (M101)","M 64":"Black Eye Galaxy (M64)",
 "M 83":"Southern Pinwheel (M83)","NGC 253":"Sculptor Galaxy (NGC 253)","M 63":"Sunflower Galaxy (M63)","NGC 4038":"Antennae Galaxies (NGC 4038)","M 77":"Cetus A (M77)","NGC 1316":"Fornax A (NGC 1316)","NGC 6822":"Barnard's Galaxy (NGC 6822)","M 110":"M110","M 32":"M32"}
for e in E.values():
    allid=[e["n"]]+e["a"]
    for k,v in OV.items():
        if k in allid:
            e["a"]=sorted(set(x for x in allid if x!=v)); e["n"]=v
            if e["g"].startswith("Nearby") or e["g"].startswith("Bright"): e["g"]="Messier & famous galaxies"
            break
    e["a"]=[x for x in e["a"] if x.upper()!="SMOKING GUN"]
E["X:MW"]=dict(n="Milky Way (our galaxy)",a=["Galaxy","MW"],g="Local Group",t="our home galaxy",ra=0,dec=0,d=0.0,m="we are inside it",z=0,p=[0,0,0],note="Our home: a barred spiral galaxy about 100,000 light-years across. The map is centred on it.")
out=list(E.values()); out.sort(key=lambda e:(e["g"],e["d"]))
json.dump(out,open("galaxy_index.json","w"),separators=(",",":"),ensure_ascii=False)
from collections import Counter; print(len(out),Counter(e["g"] for e in out))
for q in ["Andromeda","Triangulum","LMC","SMC","Whirlpool","Sombrero","Centaurus A","M  87","Virgo","Coma","Fornax"]:
    print(q,[ (e["n"],e["d"],e["g"]) for e in out if q.lower() in (e["n"]+" "+" ".join(e["a"])).lower()][:3])
