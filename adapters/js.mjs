import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';import readline from 'node:readline';
function walk(root,rel=''){let out=[];for(const ent of fs.readdirSync(path.join(root,rel),{withFileTypes:true})){let r=rel?rel+'/'+ent.name:ent.name;out.push([r,ent.isDirectory()]);if(ent.isDirectory())out.push(...walk(root,r));}return out;}
function sum(b){let h=0;for(const x of b)h=(h*31+x)%1000000007;return h;}
function execute(kind,root,dest,n,variant){let rows=[],lines=[];const entries=walk(root);
if(kind==='relocate'){fs.mkdirSync(dest+'/moved',{recursive:true});for(let x of fs.readdirSync(dest))if(x!=='moved')fs.renameSync(dest+'/'+x,dest+'/moved/'+x);}
for(const [rel,dir] of entries){const p=root+'/'+rel,q=dest+'/'+rel;if(dir){if(kind==='walk')rows.push([rel,-1,0]);continue;}if(kind==='walk'){rows.push([rel,0,0]);continue;}if(kind==='mixed'&&(rel.startsWith('group19/')||! /\.(md|dat)$/.test(rel)))continue;let size=fs.statSync(p).size,v=0;
if(kind==='filter'&&Number(path.basename(rel).slice(1,7))%100>=variant)continue;
if(['read','hash-portable','mirror','detect-hash','clean','manifest','generate','mixed'].includes(kind))v=sum(fs.readFileSync(p));
if(kind==='large-read'){let b=fs.readFileSync(p);v=b[0]*256+b[b.length-1];}
if(kind==='hash-sha256')v=crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
if(kind==='detect-mtime'&&fs.existsSync(q)&&Math.floor(fs.statSync(p).mtimeMs/1000)===Math.floor(fs.statSync(q).mtimeMs/1000))continue;
if(kind==='detect-hash'&&fs.existsSync(q)&&v===sum(fs.readFileSync(q)))continue;
if(kind==='clean'){if(!fs.existsSync(q))rows.push([rel,'missing',0]);else if(v!==sum(fs.readFileSync(q)))rows.push([rel,'modified',0]);continue;}
if(kind==='mixed'&&!/\.(md|dat)$/.test(rel))continue;
if(['write','overwrite','copy','mirror','generate','mixed','large-write'].includes(kind)){fs.mkdirSync(path.dirname(q),{recursive:true});if(kind==='mixed'&&rel.endsWith('.dat'))fs.copyFileSync(p,q);else if(['generate','mixed'].includes(kind))fs.writeFileSync(q+'.generated',Buffer.concat([Buffer.from('generated\n'),fs.readFileSync(p)]));else if(kind==='mirror'){if(!fs.existsSync(q)||v!==sum(fs.readFileSync(q)))fs.copyFileSync(p,q);}else if(kind==='copy')fs.copyFileSync(p,q);else fs.writeFileSync(q,fs.readFileSync(p));}
if(kind==='rename')fs.renameSync(q,q+'.renamed');if(kind==='delete')fs.unlinkSync(q);
if(['manifest','generate','mixed'].includes(kind))lines.push([rel,`${rel}\t${size}\t${v}\n`]);rows.push([rel,size,v]);}
if(['mirror','clean'].includes(kind))for(const [rel,dir] of walk(dest))if(!dir&&!fs.existsSync(root+'/'+rel)){if(kind==='mirror')fs.unlinkSync(dest+'/'+rel);else rows.push([rel,'unexpected',0]);}
if(['manifest','generate','mixed'].includes(kind))fs.writeFileSync(dest+'/manifest.tsv',lines.sort((a,b)=>a[0]<b[0]?-1:a[0]>b[0]?1:0).map(x=>x[1]).join(''));return rows;}
console.log('BOOT');for await(const line of readline.createInterface({input:process.stdin})){let p=line.split('|');console.log(JSON.stringify(execute(p[0],p[1],p[2],+p[3],+p[4])));}
