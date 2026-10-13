"""Frozen rotated campaign; prepare/verify outside clock, all observations retained."""
from pathlib import Path
import os,sys,json,time,subprocess,hashlib,statistics,signal,threading,argparse
R=Path(__file__).resolve().parents[1];os.chdir(R);sys.path.insert(0,str(R/'scripts'))
import fixtures
ENGINES=['nift','python','node','bun','go']
def commands():
 t=R/'work/tools'
 return {'nift':[str(R/'work/nift-source/nift'),'adapters/nift.f'],'python':[str(next((t/'python').glob('*/bin/python3'))),'adapters/python.py'],'node':[str(t/'node-v24.21.0-linux-x64/bin/node'),'adapters/js.mjs'],'bun':[str(t/'bun-linux-x64/bun'),'adapters/js.mjs'],'go':[str(R/'work/go-adapter')]}
def unavailable(e,c):return 'No located native SHA-256 API' if e=='nift' and c['kind']=='hash-sha256' else 'stat exposes no mtime' if e=='nift' and c['kind']=='detect-mtime' else None
def digest(v):return hashlib.sha256(json.dumps(v,separators=(',',':'),sort_keys=True).encode()).hexdigest()
def affinity():os.sched_setaffinity(0,sorted(os.sched_getaffinity(0))[:4])
def measure(e,request,boundary,timeout=600):
 stderr=R/'work/last.stderr';err=stderr.open('wb');start=time.perf_counter_ns();p=subprocess.Popen(commands()[e],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=err,preexec_fn=affinity,start_new_session=True)
 timer=threading.Timer(timeout,lambda:os.killpg(p.pid,signal.SIGKILL) if p.poll() is None else None);timer.daemon=True;timer.start()
 try:
  boot=p.stdout.readline();assert boot==b'BOOT\n',(e,boot,stderr.read_text()[-1000:])
  if boundary=='booted':start=time.perf_counter_ns()
  p.stdin.write(request.encode());p.stdin.flush();raw=p.stdout.readline();stop=time.perf_counter_ns();p.stdin.close();rest=p.stdout.read();pid,status,usage=os.wait4(p.pid,0);p.returncode=os.waitstatus_to_exitcode(status)
  if boundary=='fresh':stop=time.perf_counter_ns()
  assert p.returncode==0 and not rest,(e,p.returncode,stderr.read_text()[-1000:]);assert raw.endswith(b'\n'),(e,'no complete response')
  return sorted(json.loads(raw)),{'wall_ms':(stop-start)/1e6,'cpu_ms':(usage.ru_utime+usage.ru_stime)*1000,'process_maxrss_mib':usage.ru_maxrss/1024,'context_switches':usage.ru_nvcsw+usage.ru_nivcsw,'raw_stdout_sha256':hashlib.sha256(raw).hexdigest()}
 finally:timer.cancel();err.close()

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--directory',default='work/official');ap.add_argument('--quick',action='store_true');args=ap.parse_args();out=R/args.directory;out.mkdir(parents=True,exist_ok=False)
 cases=json.loads((R/'docs/SCENARIOS.json').read_text());suite=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();environment={'suite_sha':suite,'nift_source_sha':subprocess.check_output(['git','-C','work/nift-source','rev-parse','HEAD'],text=True).strip(),'nift_version':subprocess.check_output([commands()['nift'][0],'version'],text=True).strip(),'compiler':subprocess.check_output(['g++','--version'],text=True).strip(),'versions':json.loads(Path(os.environ.get('NIFT_BENCH_VERSIONS_JSON',str(R/'docs/VERSIONS.json'))).read_text()),'platform':subprocess.check_output(['uname','-a'],text=True).strip(),'cpu':subprocess.check_output(['lscpu'],text=True),'filesystem':subprocess.check_output(['findmnt','-T',str(R),'-o','SOURCE,FSTYPE,OPTIONS'],text=True),'df':subprocess.check_output(['df','-B1',str(R)],text=True),'affinity':sorted(os.sched_getaffinity(0))[:4],'binaries':{e:hashlib.sha256(Path(cmd[0]).read_bytes()).hexdigest() for e,cmd in commands().items()}}
 (out/'environment.json').write_text(json.dumps(environment,indent=2));observations=out/'observations.jsonl';summary=[];seq=0
 for c in cases:
  n=c['n'];root=R/f"work/fixtures/{'large-'+str(n) if 'large_bytes' in c else n}";dest=R/'work/destination'
  if not root.exists():
   m=fixtures.generate_large(root,n,c['large_bytes']) if 'large_bytes' in c else fixtures.generate(root,n)
   (out/f"fixture-{root.name}.json").write_text(json.dumps(m,separators=(',',':')))
  else:
   m=fixtures.manifest(root);(out/f"fixture-{root.name}.json").write_text(json.dumps(m,separators=(',',':')))
  base=fixtures.prepare(c['kind'],root,dest,n,c['variant']);expect=fixtures.expected(c['kind'],root,dest,n,c['variant']);expected_sha=digest(expect);request=f"{c['kind']}|{root}|{dest}|{n}|{c['variant']}\n";counts=1 if args.quick else c['samples'];warmups=0 if args.quick else 1
  for boundary in ['fresh','booted']:
   cells={e:[] for e in ENGINES if not unavailable(e,c)}
   for phase,rounds in [('warmup',warmups),('measured',counts)]:
    for rnd in range(rounds):
     order=ENGINES[rnd%5:]+ENGINES[:rnd%5]
     for e in order:
      if e not in cells:continue
      start_state=fixtures.prepare(c['kind'],root,dest,n,c['variant']);assert digest(start_state)==digest(base),'fixture reset differs'
      actual,metrics=measure(e,request,boundary);assert actual==expect,(e,c['id'],'output rows differ');fixtures.verify_output(c['kind'],root,dest,start_state,n)
      rec={'sequence':seq,'engine':e,'scenario':c['id'],'boundary':boundary,'phase':phase,'round':rnd,'rotation':order,'expected_sha256':expected_sha,'actual_sha256':digest(actual),'start_state_sha256':digest(start_state),'output_rows':len(actual),'correct':True,**metrics};seq+=1
      with observations.open('a') as f:f.write(json.dumps(rec,separators=(',',':'))+'\n')
      if phase=='measured':cells[e].append(rec)
      print(c['id'],boundary,phase,rnd,e,round(metrics['wall_ms'],3),flush=True)
   for e,recs in cells.items():
    d={'engine':e,'scenario':c['id'],'kind':c['kind'],'n':n,'variant':c['variant'],'boundary':boundary,'samples':len(recs),'expected_sha256':expected_sha}
    for metric in ['wall_ms','cpu_ms','process_maxrss_mib','context_switches']:
     a=sorted(r[metric] for r in recs);d[metric]={'median':statistics.median(a),'min':a[0],'max':a[-1],'p95':a[min(len(a)-1,__import__('math').ceil(.95*len(a))-1)]}
    summary.append(d)
   (out/'summary.json').write_text(json.dumps(summary,indent=2))
 (out/'complete.json').write_text(json.dumps({'pass':True,'quick_certification':args.quick,'scenarios':len(cases),'supported_cells':len(summary),'observations':seq,'measured':sum(x['samples'] for x in summary),'suite_sha':suite,'observations_sha256':hashlib.sha256(observations.read_bytes()).hexdigest()},indent=2))
if __name__=='__main__':main()
