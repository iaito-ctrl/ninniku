const { chromium } = require('playwright');
const fs=require('fs');const path=require('path');
const dir=__dirname;const mode=process.argv[2]||'preview';
const durs=fs.readFileSync(path.join(dir,'durs.txt'),'utf8').trim().split('\n').map(Number);
const PAD=0.55, LEAD=0.25;let t=0;const sc=durs.map((d,i)=>{const s={start:t,dur:d+PAD+(i==0?LEAD:0)+(i==8?1.2:0)};t+=s.dur;return s;});
fs.writeFileSync(path.join(dir,'scenes.json'),JSON.stringify(sc));
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
 await p.goto('file://'+path.join(dir,'anim.html'));await p.evaluate(()=>document.fonts.ready);
 await p.evaluate(sc=>window.setup(sc),sc);
 const total=t;console.log('total',total.toFixed(2));
 if(mode==='preview'){for(let i=0;i<sc.length;i++){const T=sc[i].start+sc[i].dur*0.6;await p.evaluate(T=>window.render(T),T);
   await p.locator('canvas').screenshot({path:path.join(dir,`prev${i+1}.png`)});}}
 else{const fps=24;fs.mkdirSync(path.join(dir,'frames'),{recursive:true});const n=Math.ceil(total*fps);
   for(let f=0;f<n;f++){await p.evaluate(T=>window.render(T),f/fps);await p.locator('canvas').screenshot({path:path.join(dir,'frames',String(f).padStart(5,'0')+'.png'),type:'png'});}
   console.log('frames',n);}
 await b.close();})();
