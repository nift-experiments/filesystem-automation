"""Independent distribution audit, separate from measured runner and fixture oracle."""
from pathlib import Path
import json,sys,hashlib,collections,math,statistics
p=Path(sys.argv[1]);raw=[json.loads(line) for line in (p/'observations.jsonl').read_text().splitlines()];groups=collections.defaultdict(list)
for x in raw:
 assert x['correct'] and x['actual_sha256']==x['expected_sha256']
 if x['phase']=='measured':groups[(x['scenario'],x['boundary'],x['engine'])].append(x)
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
r=dict(pass_=True,method='Independent nearest-rank p95 and all metric distributions, no dropped observations',cells=len(summary),measured=sum(s['samples'] for s in summary),summary_sha256=hashlib.sha256((p/'summary.json').read_bytes()).hexdigest());r['pass']=r.pop('pass_');(p/'distribution-audit.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
