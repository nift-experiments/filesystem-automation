from pathlib import Path
import sys,time,json,subprocess,os
sys.path.insert(0,str(Path(__file__).resolve().parent));import run,fixtures
R=run.R;source=R/'work/reuse-fixture';fixtures.generate(source,1000);out=R/'work/reuse';out.mkdir(exist_ok=True);expected=fixtures.expected('stat',source,out/'dest',1000,0);rows=[]
for e in run.ENGINES:
 p=subprocess.Popen(run.commands()[e],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,bufsize=1);assert p.stdout.readline().strip()=='BOOT'
 for i in range(10):
  t=time.perf_counter();p.stdin.write(f'stat|{source}|{out}/dest|1000|0\n');p.stdin.flush();line=p.stdout.readline();wall=(time.perf_counter()-t)*1000;actual=sorted(json.loads(line));assert actual==expected
  rss=None
  status=Path(f'/proc/{p.pid}/status')
  if status.exists():
   for x in status.read_text().splitlines():
    if x.startswith('VmRSS:'):rss=int(x.split()[1])/1024
  row=dict(engine=e,request=i,wall_ms=wall,rss_mib=rss,correct=True,output_sha256=run.digest(actual));rows.append(row);print(e,i,round(wall,2),flush=True)
 p.stdin.close();assert p.wait()==0
(out/'observations.json').write_text(json.dumps(rows,indent=2)+'\n')
