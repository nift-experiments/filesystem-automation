"""Compact audited summaries only. Never copy raw evidence into Labs."""
from pathlib import Path
import json,hashlib,sys
R=Path(__file__).resolve().parents[1];main=R/'work/official';supp=R/'work/filter-suite/work/official'
raw=[]
for p in [main,supp]:
 audit=json.loads((p/'independent-audit.json').read_text());assert audit['pass']
 assert hashlib.sha256((p/'summary.json').read_bytes()).hexdigest()==audit['summary_sha256']
 raw+=json.loads((p/'summary.json').read_text())
S={(x['scenario'],x['boundary'],x['engine']):x for x in raw};E=['nift','python','node','bun','go']
def rows(names,boundary='booted',metric='wall_ms'):
 out=[];limits={}
 for key,_ in names:
  kind=next(S[(key,boundary,e)]['kind'] for e in E if (key,boundary,e) in S)
  limits[kind]=max(limits.get(kind,0),max(S[(key,boundary,e)][metric]['median'] for e in E if (key,boundary,e) in S))
 for key,label in names:
  vals=[S.get((key,boundary,e),{}).get(metric,{}).get('median') for e in E];hi=limits[next(S[(key,boundary,e)]['kind'] for e in E if (key,boundary,e) in S)]
  out.append([label,[[f'{v:,.3f}',round(v/hi*100,1)] if v is not None else ['—',0] for v in vals]])
 return out
sections=[]
def add(t,names,b='booted',metric='wall_ms'):
 sections.append({'t':t,'c':('Fresh invocation' if b=='fresh' else 'Booted isolated request')+' / '+('process lifetime peak RSS MiB' if metric!='wall_ms' else 'median ms'),'rows':rows(names,b,metric)})
add('scan.log — walk, stat, select',[(f'walk-{n}',f'walk / {n:,}') for n in [1000,10000,100000]]+[(f'stat-{n}',f'stat / {n:,}') for n in [10000,100000]]+[(f'filter-{v}-10000',f'basename {v}% / 10,000') for v in [1,10,50]]+[(f'filter-{v}-10000',f'{v} / 10,000') for v in ['extension','prefix','size']])
add('content.tsv — read, fingerprint, generate',[('read-10000','read + checksum / 10,000'),('read-100000','read + checksum / 100,000'),('large-read-10x10485760','read / 10×10 MiB'),('large-read-100x1048576','read / 100×1 MiB'),('hash-sha256-10000','native SHA-256 / 10,000'),('manifest-10000','manifest / 10,000'),('write-10000','stream write / 10,000'),('large-write-10x10485760','stream write / 10×10 MiB'),('generate-10000','generate / 10,000'),('mixed-10000','mixed workflow / 10,000')])
add('changes.diff — copy, reconcile, remove',[('copy-100000','copy / 100,000'),('mirror-0-10000','mirror clean / 10,000'),('mirror-10-10000','mirror 10% content / 10,000'),('mirror-12-10000','mirror 1% add/delete / 10,000'),('rename-10000','rename files / 10,000'),('delete-10000','delete files / 10,000'),('detect-mtime-3-10000','mtime, restored time / 10,000'),('detect-hash-3-10000','content, restored time / 10,000')])
add('memory.map',[('walk-1000','walk / 1,000'),('walk-10000','walk / 10,000'),('walk-100000','walk / 100,000')],metric='process_maxrss_mib')
add('launch.log — include startup and exit',[('walk-10000','walk / 10,000'),('mixed-10000','mixed workflow / 10,000')],b='fresh')
meta=json.loads(Path(sys.argv[1]).read_text());assert len(meta['evidence_sha'])==40 and meta['audit_pass'];meta['evidence']='https://github.com/nift-experiments/lab-evidence/tree/'+meta['evidence_sha']+'/benchmarks/filesystem-automation/'+meta['series']
p=Path(sys.argv[2]);p.write_text(json.dumps({'meta':meta,'sections':sections},separators=(',',':'))+'\n');print(p,p.stat().st_size)
