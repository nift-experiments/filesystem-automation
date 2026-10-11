"""Build separately frozen predicate supplement; never alter the primary cohort."""
from pathlib import Path
import subprocess,json,os
R=Path(__file__).resolve().parents[1]
BASE='999defe8dae3f9d15e9a17225e6014020be04574'
D=R/'work/filter-suite'
assert not D.exists(),'Supplement directory already exists'
D.mkdir(parents=True)
for rel in subprocess.check_output(['git','ls-tree','-r','--name-only',BASE],cwd=R,text=True).splitlines():
 p=D/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(subprocess.check_output(['git','show',BASE+':'+rel],cwd=R))
def replace(rel,a,b):
 p=D/rel;s=p.read_text();assert s.count(a)==1,(rel,a);p.write_text(s.replace(a,b))
replace('adapters/python.py','if int(Path(rel).stem[1:])%100>=variant:continue',"if (variant==101 and not rel.endswith('.md')) or (variant==102 and not rel.startswith('group00/')) or (variant==103 and size<768):continue")
replace('adapters/js.mjs',"if(kind==='filter'&&Number(path.basename(rel).slice(1,7))%100>=variant)continue;","if(kind==='filter'&&((variant===101&&!rel.endsWith('.md'))||(variant===102&&!rel.startsWith('group00/'))||(variant===103&&size<768)))continue;")
replace('adapters/nift.f','names := rel.split("/"); fname := names[names.size()-1]; id := fname.substr(1,6).to_int(); if(id%100 >= variant) { continue }','if((variant == 101 && !rel.ends_with(".md")) || (variant == 102 && !rel.starts_with("group00/")) || (variant == 103 && size < 768)) { continue }')
replace('adapters/go.go','id,e:=strconv.Atoi(filepath.Base(rel)[1:7]);must(e);if id%100>=variant{continue}','if (variant==101&&!strings.HasSuffix(rel,".md"))||(variant==102&&!strings.HasPrefix(rel,"group00/"))||(variant==103&&size<768){continue}')
replace('scripts/fixtures.py',"if i%100<variant and p.suffix in {'.md','.json','.cpp','.txt','.dat'} and p.parent.parts[-3].startswith('group') and size>=96:rows.append([rel,size,0])","if (variant==101 and p.suffix=='.md') or (variant==102 and rel.startswith('group00/')) or (variant==103 and size>=768):rows.append([rel,size,0])")
replace('scripts/audit.py',"elif kind=='filter' and i%100>=c['variant']:continue","elif kind=='filter' and not ((c['variant']==101 and rel.endswith('.md')) or (c['variant']==102 and rel.startswith('group00/')) or (c['variant']==103 and s>=768)):continue")
replace('scripts/run.py',";dest=R/'work/destination'",";root=root.resolve();dest=R/'work/destination'")
cases=[dict(id=f'filter-{label}-{n}',kind='filter',n=n,variant=v,samples={1000:50,10000:20,100000:3}[n]) for n in [1000,10000,100000] for label,v in [('extension',101),('prefix',102),('size',103)]]
(D/'docs/SCENARIOS.json').write_text(json.dumps(cases,indent=2)+'\n')
(D/'work').mkdir()
for name in ['tools','nift-source']:(D/'work'/name).symlink_to(R/'work'/name)
(D/'work/fixtures').mkdir()
for n in [1000,10000,100000]:(D/f'work/fixtures/{n}').symlink_to(R/f'work/fixtures/{n}')
go=R/'work/tools/go/bin/go'
env=dict(os.environ,GOCACHE='/tmp/filesystem-go-cache')
subprocess.run([str(go),'build','-o',str(D/'work/go-adapter'),str(D/'adapters/go.go')],check=True,env=env)
print(D)
