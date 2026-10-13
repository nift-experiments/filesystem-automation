"""Independent accounting audit: recompute expected fingerprints from fixture specification."""
from pathlib import Path
import sys,json,hashlib,collections,math
R=Path(__file__).resolve().parents[1]
def digest(v):return hashlib.sha256(json.dumps(v,separators=(',',':'),sort_keys=True).encode()).hexdigest()
def audit(directory,quick_certify=False):
 p=Path(directory);cases=json.loads((R/'docs/SCENARIOS.json').read_text());raw=[json.loads(x) for x in (p/'observations.jsonl').read_text().splitlines()];summary=json.loads((p/'summary.json').read_text());complete=json.loads((p/'complete.json').read_text());assert bool(complete.get('quick_certification',False))==quick_certify,'Certification/official identity mismatch';assert all(x['correct'] and x['actual_sha256']==x['expected_sha256'] for x in raw)
 assert [x['sequence'] for x in raw]==list(range(len(raw)))
 by=collections.defaultdict(list)
 for x in raw:by[(x['scenario'],x['boundary'],x['engine'],x['phase'])].append(x)
 expected_cells=0
 for c in cases:
  n=c['n'];large='large_bytes' in c;fixture=json.loads((p/f"fixture-{'large-'+str(n) if large else n}.json").read_text());assert len(fixture)==n
  expected=[];dirs=set();changed=max(1,n//100)
  for rel,meta in sorted(fixture.items()):
   parts=rel.split('/');dirs.update('/'.join(parts[:i]) for i in range(1,len(parts)))
   if large:
    i=int(rel[5:8]);b=bytes([65+i%26])*c['large_bytes']
   else:
    i=int(parts[-1][1:7]);seed=f'id={i:06d};kind=project;value={i*17+3}\n'.encode();size=[96,192,384,768,2048][i%5];b=(seed*((size+len(seed)-1)//len(seed)))[:size]
   assert meta['size']==len(b) and meta['sha256']==hashlib.sha256(b).hexdigest() and meta['mtime']==1700000000
   kind=c['kind'];v=0;s=len(b)
   if kind=='walk':s=0
   elif kind=='filter' and i%100>=c['variant']:continue
   elif kind in {'read','mirror','manifest','generate','mixed','detect-hash'}:
    for x in b:v=(v*31+x)%1000000007
    if kind=='mixed' and (rel.startswith('group19/') or not rel.endswith(('.md','.dat'))):continue
    if kind=='detect-hash' and (c['variant']==2 or i>=changed):continue
   elif kind=='hash-sha256':v=hashlib.sha256(b).hexdigest()
   elif kind=='large-read':v=b[0]*256+b[-1]
   elif kind=='detect-mtime':
    if c['variant']==3 or i>=changed:continue
   elif kind=='clean':
    if i==n-1:expected.append([rel,'missing',0])
    elif i<changed:expected.append([rel,'modified',0])
    continue
   expected.append([rel,s,v])
  if c['kind']=='walk':expected.extend([d,-1,0] for d in dirs)
  if c['kind']=='clean':expected.append(['unexpected000000.txt','unexpected',0])
  h=digest(sorted(expected))
  for boundary in ['fresh','booted']:
   for engine in ['nift','python','node','bun','go']:
    if engine=='nift' and c['kind'] in {'hash-sha256','detect-mtime'}:continue
    expected_cells+=1
    for phase,count in [('warmup',0 if quick_certify else 1),('measured',1 if quick_certify else c['samples'])]:
     key=(c['id'],boundary,engine,phase);items=by.pop(key,[]) if count==0 else by.pop(key);assert len(items)==count,key
     assert [x['round'] for x in items]==list(range(count))
     if count==0:continue
     starts={x['start_state_sha256'] for x in items};assert len(starts)==1
     for x in items:
      assert x['actual_sha256']==h,(key,'independent expected differs')
      order=['nift','python','node','bun','go'];j=x['round']%5;assert x['rotation']==order[j:]+order[:j]
    s=[x for x in summary if (x['scenario'],x['boundary'],x['engine'])==(c['id'],boundary,engine)];assert len(s)==1 and s[0]['samples']==(1 if quick_certify else c['samples']) and s[0]['expected_sha256']==h
 assert not by and len(summary)==expected_cells
 assert complete['observations']==len(raw) and complete['measured']==sum(x['phase']=='measured' for x in raw)
 receipt={'pass':True,'quick_certification':quick_certify,'scenarios':len(cases),'supported_cells':expected_cells,'measured':complete['measured'],'warmups':len(raw)-complete['measured'],'observations':len(raw),'independent_fixture_specification_and_row_fingerprints':True,'observations_sha256':hashlib.sha256((p/'observations.jsonl').read_bytes()).hexdigest(),'summary_sha256':hashlib.sha256((p/'summary.json').read_bytes()).hexdigest()};(p/'independent-audit.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))
if __name__=='__main__':audit(sys.argv[1],quick_certify='--quick-certify' in sys.argv)
