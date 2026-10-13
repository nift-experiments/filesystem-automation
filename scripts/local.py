from pathlib import Path
import os,sys,json,time,subprocess,hashlib
R=Path(__file__).resolve().parents[1];os.chdir(R);sys.path.insert(0,str(R/'scripts'))
import fixtures
from scenarios import rows
# Historical default borrows concurrency tools; fresh single-suite hosts opt in.
C=R if os.environ.get('FS_STANDALONE_TOOLS')=='1' else R.parent/'concurrency'
def commands():
 tools=C/'work/tools'
 return {'nift':[str(C/'work/nift-source/nift'),'adapters/nift.f'],'python':[str(next((R/'work/tools/python').glob('*/bin/python3'))),'adapters/python.py'],'node':[str(tools/'node-v24.21.0-linux-x64/bin/node'),'adapters/js.mjs'],'bun':[str(tools/'bun-linux-x64/bun'),'adapters/js.mjs'],'go':[str(R/'work/go-adapter')]}
def unsupported(e,kind):return e=='nift' and kind in {'hash-sha256','detect-mtime'}
def one(e,c,n=20):
 source=R/f'work/fixtures/{n}';dest=R/'work/destination';start=fixtures.prepare(c['kind'],source,dest,n,c['variant']);expect=fixtures.expected(c['kind'],source,dest,n,c['variant']);req=f"{c['kind']}|{source}|{dest}|{n}|{c['variant']}\n"
 t=time.monotonic();p=subprocess.run(commands()[e],input=req,text=True,capture_output=True,timeout=300);elapsed=time.monotonic()-t
 if p.returncode:raise RuntimeError((e,c['id'],p.stderr[-2000:],p.stdout[-1000:]))
 lines=p.stdout.splitlines();assert lines[0]=='BOOT';actual=sorted(json.loads(lines[-1]));assert actual==expect,(e,c['id'],actual[:4],expect[:4]);fixtures.verify_output(c['kind'],source,dest,start,n)
 return {'engine':e,'scenario':c['id'],'n':n,'pass':True,'wall_s':elapsed,'rows':len(actual),'output_sha256':hashlib.sha256(json.dumps(actual,separators=(',',':')).encode()).hexdigest()}
if __name__=='__main__':
 log=[];n=int(sys.argv[1]) if len(sys.argv)>1 else 20;fixtures.generate(R/f'work/fixtures/{n}',n)
 cases=[x for x in rows if x['n']==1000]
 for c in cases:
  for e in commands():
   if unsupported(e,c['kind']):continue
   rec=one(e,c,n);log.append(rec);print(e,c['id'],round(rec['wall_s'],3),flush=True);(R/f'work/local-{n}.json').write_text(json.dumps(log,indent=2))
