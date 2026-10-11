import json
from pathlib import Path
rows=[]
for n in [1000,10000,100000]:
 for kind in ['walk','stat','read','hash-sha256','manifest','write','overwrite','copy','rename','relocate','delete','generate','mixed','clean']:
  rows.append(dict(id=f'{kind}-{n}',kind=kind,n=n,variant=1 if kind=='clean' else 0))
 for ratio in [1,10,50]:rows.append(dict(id=f'filter-{ratio}-{n}',kind='filter',n=n,variant=ratio))
 for ratio in [0,1,10,11,12]:rows.append(dict(id=f'mirror-{ratio}-{n}',kind='mirror',n=n,variant=ratio))
 for kind in ['detect-mtime','detect-hash']:
  for variant in [1,2,3]:rows.append(dict(id=f'{kind}-{variant}-{n}',kind=kind,n=n,variant=variant))
rows=[x for x in rows if x['n']<100000 or x['kind'] in {'walk','stat','filter','read','hash-sha256','copy'}]
for count,size in [(10,10485760),(100,1048576)]:
 for kind in ['large-read','large-write']:rows.append(dict(id=f'{kind}-{count}x{size}',kind=kind,n=count,variant=0,large_bytes=size))
# Costs and counts are frozen only after local feasibility.
if __name__=='__main__':
 p=Path('docs/SCENARIOS.json')
 if p.exists() and any('samples' in x for x in json.loads(p.read_text())):raise SystemExit('Frozen sample matrix exists; do not overwrite it')
 p.write_text(json.dumps(rows,indent=2)+'\n')
