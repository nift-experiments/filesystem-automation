"""Independent distribution audit, separate from measured runner and fixture oracle."""
from pathlib import Path
import json,sys,hashlib,collections,math,statistics
p=Path(sys.argv[1]);raw=[json.loads(line) for line in (p/'observations.jsonl').read_text().splitlines()];groups=collections.defaultdict(list)
for x in raw:
 assert x['correct'] and x['actual_sha256']==x['expected_sha256']
 if x['phase']=='measured':groups[(x['scenario'],x['boundary'],x['engine'])].append(x)
# Reconstruct destructive starting manifests independently of fixtures.prepare.
cases=json.loads((p.parents[1]/'docs/SCENARIOS.json').read_text());starts={}
for c in cases:
 n=c['n'];kind=c['kind'];v=c['variant'];name='large-'+str(n) if 'large_bytes' in c else str(n)
 base=json.loads((p/f'fixture-{name}.json').read_text());start={}
 if kind in {'overwrite','rename','relocate','delete','mirror','detect-mtime','detect-hash','clean'}:start={k:dict(x) for k,x in base.items()}
 if kind in {'mirror','detect-mtime','detect-hash','clean'}:
  ratio=1 if kind.startswith('detect') else 10 if v==11 else 0 if v==12 else v
  for i in range(max(1,n*ratio//100) if ratio else 0):
   ext=['md','json','cpp','txt','dat'][i%5];rel=f'group{i%20:02d}/depth{i%3}/bucket{i//1000:03d}/f{i:06d}.{ext}'
   seed=f'id={i:06d};kind=project;value={i*17+3}\n'.encode();size=[96,192,384,768,2048][i%5];b=(seed*((size+len(seed)-1)//len(seed)))[:size]
   if not (v==2 and kind.startswith('detect')):b=b'X'+b[1:]
   start[rel]={'size':len(b),'sha256':hashlib.sha256(b).hexdigest(),'mtime':1700000000 if v==3 and kind.startswith('detect') else 1700000100}
  if kind=='clean' or v in [11,12]:
   for j in range(1 if kind=='clean' else max(1,n//100)):
    i=n-1-j;ext=['md','json','cpp','txt','dat'][i%5];rel=f'group{i%20:02d}/depth{i%3}/bucket{i//1000:03d}/f{i:06d}.{ext}';del start[rel]
    start[f'unexpected{j:06d}.txt']={'size':11,'sha256':hashlib.sha256(b'unexpected\n').hexdigest(),'mtime':1700000000}
 starts[c['id']]=hashlib.sha256(json.dumps(start,separators=(',',':'),sort_keys=True).encode()).hexdigest()
for x in raw:assert x['start_state_sha256']==starts[x['scenario']],(x['scenario'],'independent reset manifest differs')
summary=json.loads((p/'summary.json').read_text());derived=[]
for s in summary:
 g=groups.pop((s['scenario'],s['boundary'],s['engine']));assert len(g)==s['samples']
 for k in ['wall_ms','cpu_ms','process_maxrss_mib','context_switches']:
  v=sorted(x[k] for x in g);assert all(math.isfinite(x) and x>=0 for x in v)
  expected=dict(median=statistics.median(v),min=v[0],max=v[-1],p95=v[math.ceil(.95*len(v))-1]);assert s[k]==expected,(s['scenario'],s['engine'],k)
 n=s['n'];ms=s['wall_ms']['median'];d=dict(scenario=s['scenario'],boundary=s['boundary'],engine=s['engine'],files_per_second=n*1000/ms)
 if s['kind'] in {'read','write','overwrite','copy','large-read','large-write'}:
  name='large-'+str(n) if s['kind'].startswith('large') else str(n);m=json.loads((p/f'fixture-{name}.json').read_text());d['source_mib_per_second']=sum(x['size'] for x in m.values())/1048576*1000/ms
 derived.append(d)
assert not groups
(p/'derived-throughput.json').write_text(json.dumps({'note':'Operational rates, not device bandwidth; byte reads/checksums and stream writes include stated work. Files/sec is input-tree rate, not selected-output rate.','rows':derived},indent=2)+'\n')
r=dict(pass_=True,method='Independent reset-state manifests, nearest-rank p95 and all metric distributions; no dropped observations',cells=len(summary),measured=sum(s['samples'] for s in summary),summary_sha256=hashlib.sha256((p/'summary.json').read_bytes()).hexdigest());r['pass']=r.pop('pass_');(p/'distribution-audit.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
