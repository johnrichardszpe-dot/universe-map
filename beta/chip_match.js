// Chip's offline question matcher (no network, no API). Exposes CHIPM.ask(query, facts).
(function(G){
const STOP=new Set("a an the of is are was were be been to in on at for and or me tell about please what whats what's which who's how does do did can could would will i we us it its this that there their there's show give know any some much many so very just like really hey hi hello chip's".split(" "));
const INTENTS=[["size",/\b(how big|how large|size|diameter|wide|width|radius|across|bigger|biggest|largest)\b/],["dist",/\b(how far|distance|far away|how distant|away|light years away|from earth)\b/],["temp",/\b(how hot|how cold|temperature|temp|hot|cold|degrees)\b/],["moons",/\b(moons?|satellites?)\b/],["day",/\b(days?|day length|length of (a )?day|how long is a day|rotation|spin|rotate)\b/],["year",/\b(year|orbit the sun|orbital period|how long to orbit)\b/],["mass",/\b(mass|heavy|weigh|weight)\b/],["grav",/\b(gravity)\b/],["age",/\b(how old|age)\b/],["stars",/\b(how many stars)\b/]];
const INTW=new Set("big large size diameter wide width radius across far distance away distant hot cold temperature temp degrees moon moons satellite satellites day rotation spin year orbit mass heavy weigh weight gravity old age long length".split(" "));
function norm(s){return (s||"").toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g,"").replace(/[’']/g,"").replace(/[^a-z0-9]+/g," ").trim();}
function toks(s,keepInt){return norm(s).split(" ").filter(t=>t&&!STOP.has(t)&&(keepInt||!INTW.has(t)));}
// Damerau-Levenshtein (optimal string alignment)
function dl(a,b){const m=a.length,n=b.length;if(!m)return n;if(!n)return m;const d=[];for(let i=0;i<=m;i++){d[i]=[i];}for(let j=0;j<=n;j++)d[0][j]=j;
 for(let i=1;i<=m;i++)for(let j=1;j<=n;j++){const c=a[i-1]===b[j-1]?0:1;d[i][j]=Math.min(d[i-1][j]+1,d[i][j-1]+1,d[i-1][j-1]+c);if(i>1&&j>1&&a[i-1]===b[j-2]&&a[i-2]===b[j-1])d[i][j]=Math.min(d[i][j],d[i-2][j-2]+1);}return d[m][n];}
function sim(q,a){if(q===a)return 1;if(/\d/.test(q)||/\d/.test(a))return 0; // numbers/designations must match exactly
 const L=Math.max(q.length,a.length);if(Math.min(q.length,a.length)<4)return (a.length>=4&&q.length>=3&&a.startsWith(q))?0.6:0;
 if(a.length>=5&&q.length>=4&&a.startsWith(q))return 0.88;const s=1-dl(q,a)/L;return s>=0.7?s:0;}
let IDX=null;
function build(F){IDX=F.map(e=>{const al=[e.n].concat(e.k||[]).map(x=>{const t=toks(x,true);return {t,c:t.join("")};}).filter(x=>x.t.length);return {e,al};});}
function scoreEntry(it,qt,qc,nInt){let best=0;
 for(const al of it.al){let cov=0;const used=new Set();
  for(const at of al.t){let b=0,bi=-1;qt.forEach((q,i)=>{const s=sim(q,at);if(s>b){b=s;bi=i;}});if(bi>=0)used.add(bi);cov+=b;}
  cov/=al.t.length;
  if(al.c.length>=3&&qc.has(al.c))cov=Math.max(cov,1);
  // penalise leftover query words a little; reward longer aliases (more specific)
  let nl=0;qt.forEach((q,i)=>{if(!used.has(i)&&!INTW.has(q))nl++;});const nq=qt.filter(q=>!INTW.has(q)).length||1;const left=nl/nq;
  const sc=cov*(1-0.18*left)+Math.min(al.t.length,4)*0.01;
  if(sc>best)best=sc;}
 return best;}
function ask(q,F){if(!IDX)build(F);const raw=norm(q);let intent=null;for(const [k,re] of INTENTS)if(re.test(raw)){intent=k;break;}
 const qt=toks(q,true);
 const qc=new Set();for(let i=0;i<qt.length;i++){let c="";for(let j=i;j<Math.min(qt.length,i+4);j++){c+=qt[j];qc.add(c);}}
 const sc=IDX.map(it=>({e:it.e,s:scoreEntry(it,qt,qc)})).filter(x=>x.s>0).sort((a,b)=>b.s-a.s);
 const top=sc[0];if(!top||top.s<0.55)return {kind:"none",sugg:sc.slice(0,3).filter(x=>x.s>=0.4).map(x=>x.e)};
 const close=sc.filter(x=>x.s>=top.s-0.04&&x.e.id!==top.e.id);
 if(top.s>=0.84&&!(close.length&&top.s<0.95))return {kind:"answer",e:top.e,intent,score:top.s,also:close.slice(0,2).map(x=>x.e)};
 return {kind:"maybe",sugg:sc.slice(0,3).map(x=>x.e),intent,score:top.s};}
function answerText(e,intent){const i=e.i||{};return intent&&i[intent]?i[intent]+(i[intent]!==e.a?"":""):e.a;}
G.CHIPM={ask,norm,toks,answerText,_dl:dl};
})(typeof window!=="undefined"?window:globalThis);
