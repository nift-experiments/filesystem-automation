from pathlib import Path
import sys,json,time
sys.path.insert(0,str(Path(__file__).resolve().parent))
import local,fixtures
from scenarios import rows
R=local.R
log=[]
for n in [1000,10000,100000]:
 root=R/f'work/fixtures/{n}'
 m=fixtures.generate(root,n);(R/f'work/fixture-{n}.json').write_text(json.dumps(m,separators=(',',':')))
 for c in [x for x in rows if x['n']==n and 'large_bytes' not in x]:
  for e in local.commands():
   if local.unsupported(e,c['kind']):continue
   rec=local.one(e,c,n);log.append(rec);print(e,c['id'],round(rec['wall_s'],3),flush=True);(R/'work/feasibility.json').write_text(json.dumps(log,indent=2))
for c in [x for x in rows if 'large_bytes' in x]:
 root=R/f"work/fixtures/{c['n']}";m=fixtures.generate_large(root,c['n'],c['large_bytes']);(R/f"work/fixture-large-{c['n']}.json").write_text(json.dumps(m,separators=(',',':')))
 for e in local.commands():
  rec=local.one(e,c,c['n']);log.append(rec);print(e,c['id'],round(rec['wall_s'],3),flush=True);(R/'work/feasibility.json').write_text(json.dumps(log,indent=2))
assert len(log)==sum(not local.unsupported(e,c['kind']) for c in rows for e in local.commands())
print('LOCAL CERTIFICATION PASS',len(log),flush=True)
