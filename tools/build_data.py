"""Build compact data files for the public map + verify coordinates against known structures."""
import numpy as np, base64, json, sys; sys.path.insert(0,"/workspace/galaxy/v3")
from c3 import z2r, z2t, sph2xyz
from astropy.coordinates import SkyCoord; from astropy.cosmology import Planck18; import astropy.units as u
from scipy.spatial import cKDTree
rng=np.random.default_rng(2026)
A=np.load("/workspace/galaxy/v3/combined.npy").astype(np.float64)  # x,y,z,redshift,lookback,survey,ra,dec
names=["2MRS","SDSS DR17","DESI DR1 BGS","DESI DR1 LRG","DESI DR1 ELG"]
core_n={0:30000,1:25000,2:20000,3:16000,4:9000}; core=[];more=[]
for s,n in core_n.items():
    i=np.where(A[:,5]==s)[0]; rng.shuffle(i); core.append(i[:n]); more.append(i[n:])
core=np.concatenate(core); more=np.concatenate(more)
def enc(idx):
    X=A[idx]; q=np.round(X[:,:3]*7).astype(np.int16)   # 1/7 Mpc steps, max +/-4681 Mpc
    b=np.empty(len(X),dtype=[("x","<i2"),("y","<i2"),("z","<i2"),("s","u1"),("t","u1")])
    b["x"],b["y"],b["z"]=q[:,0],q[:,1],q[:,2]; b["s"]=X[:,5].astype(np.uint8); b["t"]=np.clip(np.round(X[:,4]*25),0,255).astype(np.uint8)
    return base64.b64encode(b.tobytes()).decode()
open("assets/data_core.js","w").write("window.GAL_CORE={n:%d,b64:'%s'};"%(len(core),enc(core)))
open("assets/data_more.js","w").write("window.GAL_MORE={n:%d,b64:'%s'};"%(len(more),enc(more)))
fil=np.load("/workspace/galaxy/v2/fil_segs.npy"); fil=fil[rng.choice(len(fil),30000,replace=False)]
pred=np.load("/workspace/galaxy/v2/fractal_pred.npy")
open("assets/layers.js","w").write("window.FIL=new Int16Array(Uint8Array.from(atob('%s'),c=>c.charCodeAt(0)).buffer);window.PRED=new Int16Array(Uint8Array.from(atob('%s'),c=>c.charCodeAt(0)).buffer);"%(
 base64.b64encode(np.round(fil.reshape(-1,3)*7).astype("<i2").tobytes()).decode(),base64.b64encode(np.round(pred*7).astype("<i2").tobytes()).decode()))
# ---- structures (positions from NED / literature), verification
S=[("Virgo Cluster",187.706,12.391,0.00428,"Nearest big galaxy cluster, about 1,500 galaxies, centred on giant elliptical M87. Our Local Group is being pulled toward it. Centre: M87 (NED).",True),
 ("Coma Cluster",194.953,27.981,0.0231,"Rich cluster of over 1,000 galaxies (Abell 1656). Fritz Zwicky's 1933 study of Coma gave the first hint of dark matter.",True),
 ("Perseus Cluster",49.951,41.512,0.0179,"Abell 426, one of the brightest X-ray clusters in the sky, centred on NGC 1275. Its hot gas 'hums' a sound wave detected by NASA's Chandra.",True),
 ("Shapley Supercluster",201.99,-31.49,0.048,"The biggest concentration of galaxies in our nearby universe (centre near Abell 3558). It helps pull the Milky Way along.",True),
 ("CfA2 Great Wall (approx.)",195.0,29.0,0.026,"A sheet of galaxies about 600 million light-years long, found in 1989 by Geller & Huchra. It passes through Coma. Marker = rough centre only.",False),
 ("Sloan Great Wall (approx.)",175.0,2.0,0.078,"A huge wall of galaxies about 1.4 billion light-years long, found in SDSS data by Gott et al. (2005). It spans about RA 140-212 deg. Marker = rough centre only.",False)]
P=A[:,:3]; T=cKDTree(P); out=[]; report=[]
for name,ra,dec,z,info,cl in S:
    c=SkyCoord(ra*u.deg,dec*u.deg,distance=Planck18.comoving_distance(z)); ref=np.array([c.cartesian.x.value,c.cartesian.y.value,c.cartesian.z.value])
    mine=sph2xyz(np.array([ra]),np.array([dec]),z2r(np.array([z])))[0]; err=float(np.linalg.norm(ref-mine))
    # density check vs a ring of comparison points at same distance (same survey depth)
    R=8.0; n=len(T.query_ball_point(mine,R))
    dirs=rng.normal(size=(400,3)); dirs/=np.linalg.norm(dirs,axis=1)[:,None]; cmp=[len(T.query_ball_point(d*np.linalg.norm(mine),R)) for d in dirs]
    cmp=np.array(cmp); occ=cmp[cmp>0]; ratio=float(n/np.median(occ)) if len(occ) else None
    report.append(dict(name=name,conv_err_Mpc=err,dist_Mpc=float(np.linalg.norm(mine)),n_within_8Mpc=n,median_elsewhere=float(np.median(occ)) if len(occ) else None,overdensity=ratio))
    out.append(dict(name=name,ra=ra,dec=dec,z=z,d=float(np.linalg.norm(mine)),ly=float(np.linalg.norm(mine))*3.2616e6,lt=float(z2t(np.array([z]))[0]),x=mine.tolist(),info=info,approx=not cl))
open("assets/structures.js","w").write("window.STRUCT="+json.dumps(out)+";")
json.dump(report,open("tools/verification.json","w"),indent=1)
for r in report: print(r)
print("core",len(core),"more",len(more))
