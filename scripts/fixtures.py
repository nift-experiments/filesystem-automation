"""Independent deterministic fixture source, lifecycle and correctness oracle."""
from pathlib import Path
import os,json,hashlib,shutil
BASE_MTIME=1700000000

def content(i):
 seed=f'id={i:06d};kind=project;value={i*17+3}\n'.encode()
 size=[96,192,384,768,2048][i%5]
 return (seed*((size+len(seed)-1)//len(seed)))[:size]
def relpath(i):
 ext=['md','json','cpp','txt','dat'][i%5]
 return f'group{i%20:02d}/depth{i%3}/bucket{i//1000:03d}/f{i:06d}.{ext}'
def manifest(root):
 root=Path(root);out={}
 for p in sorted(root.rglob('*')):
  if p.is_file():
   b=p.read_bytes();s=p.stat();out[p.relative_to(root).as_posix()]={'size':len(b),'sha256':hashlib.sha256(b).hexdigest(),'mtime':int(s.st_mtime)}
 return out
def generate(root,n):
 root=Path(root);root.mkdir(parents=True,exist_ok=True)
 for i in range(n):
  p=root/relpath(i);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(content(i));os.utime(p,(BASE_MTIME,BASE_MTIME))
 return manifest(root)
def warm(root):
 for p in Path(root).rglob('*'):
  if p.is_file():p.read_bytes();p.stat()
def prepare(kind,source,dest,n,variant=0):
 source=Path(source);dest=Path(dest)
 if dest.exists():shutil.rmtree(dest)
 dest.mkdir(parents=True)
 if kind in {'overwrite','rename','relocate','delete','mirror','detect-mtime','detect-hash','clean'}:
  shutil.copytree(source,dest,dirs_exist_ok=True)
 if kind in {'mirror','detect-mtime','detect-hash','clean'}:
  ratio=(1 if kind.startswith("detect") else 10 if variant==11 else 0 if variant==12 else variant)
  changed=max(1,n*ratio//100) if ratio else 0
  for i in range(changed):
   p=dest/relpath(i);p.write_bytes(b'X'+content(i)[1:]);os.utime(p,(BASE_MTIME+100,BASE_MTIME+100))
  if kind=='clean' or variant in {11,12}:
   for j in range(1 if kind=='clean' else max(1,n//100)):
    (dest/relpath(n-1-j)).unlink();p=dest/f'unexpected{j:06d}.txt';p.write_bytes(b'unexpected\n');os.utime(p,(BASE_MTIME,BASE_MTIME))
  if variant==2 and kind.startswith('detect'):
   # content unchanged, time changed; isolate semantics rather than equate modes
   for i in range(changed):
    p=dest/relpath(i);p.write_bytes(content(i));os.utime(p,(BASE_MTIME+100,BASE_MTIME+100))
  if variant==3 and kind.startswith('detect'):
   for i in range(changed):os.utime(dest/relpath(i),(BASE_MTIME,BASE_MTIME))
 warm(source);warm(dest)
 return manifest(dest)
def checksum(b):
 h=0
 for x in b:h=(h*31+x)%1000000007
 return h

def expected(kind,source,dest,n,variant):
 source=Path(source);dest=Path(dest);rows=[]
 for p in source.rglob('*'):
  rel=p.relative_to(source).as_posix()
  if p.is_dir():
   if kind=='walk':rows.append([rel,-1,0])
   continue
  b=p.read_bytes();size=len(b)
  if kind=='walk':rows.append([rel,0,0])
  elif kind=='stat':rows.append([rel,size,0])
  elif kind=='filter':
   i=int(p.stem[1:])
   if i%100<variant and p.suffix in {'.md','.json','.cpp','.txt','.dat'} and p.parent.parts[-3].startswith('group') and size>=96:rows.append([rel,size,0])
  elif kind in {'read','hash-portable','detect-hash','clean','mirror','manifest','generate','mixed'}:
   if kind.startswith('detect'):
    q=dest/rel
    if not q.exists() or checksum(q.read_bytes())!=checksum(b):rows.append([rel,size,checksum(b)])
   elif kind=='clean':
    q=dest/rel
    if not q.exists():rows.append([rel,'missing',0])
    elif hashlib.sha256(q.read_bytes()).digest()!=hashlib.sha256(b).digest():rows.append([rel,'modified',0])
   elif kind=='mixed':
    if not rel.startswith('group19/') and p.suffix in {'.md','.dat'}:rows.append([rel,size,checksum(b)])
   else:rows.append([rel,size,checksum(b)])
  elif kind=='large-read':rows.append([rel,size,b[0]*256+b[-1]])
  elif kind=='hash-sha256':rows.append([rel,size,hashlib.sha256(b).hexdigest()])
  elif kind=='detect-mtime':
   q=dest/rel
   if not q.exists() or int(q.stat().st_mtime)!=int(p.stat().st_mtime):rows.append([rel,size,0])
  else:rows.append([rel,size,0])
 if kind=='clean':
  for p in dest.rglob('*'):
   if p.is_file() and not (source/p.relative_to(dest)).exists():rows.append([p.relative_to(dest).as_posix(),'unexpected',0])
 return sorted(rows)

def verify_output(kind,source,dest,start,n):
 source=Path(source);dest=Path(dest)
 if kind in {'write','overwrite','copy','mirror','large-write'}:
  a=manifest(source);b=manifest(dest);assert {k:(v['size'],v['sha256']) for k,v in a.items()}=={k:(v['size'],v['sha256']) for k,v in b.items()}
 elif kind=='rename':
  expected={k+'.renamed':v['sha256'] for k,v in manifest(source).items()};assert {k:v['sha256'] for k,v in manifest(dest).items()}==expected
 elif kind=='relocate':
  expected={'moved/'+k:v['sha256'] for k,v in manifest(source).items()};assert {k:v['sha256'] for k,v in manifest(dest).items()}==expected
 elif kind=='delete':assert not manifest(dest)
 elif kind in {'generate','mixed'}:
  paths=manifest(source);selected={k for k in paths if kind=='generate' or (not k.startswith('group19/') and k.endswith(('.md','.dat')))};actual=manifest(dest);assert set(actual)=={k+'.generated' for k in selected}|{'manifest.tsv'}
  for k in selected:assert (dest/(k+'.generated')).read_bytes()==b'generated\n'+(source/k).read_bytes()
  lines=''.join(f'{k}\t{paths[k]["size"]}\t{checksum((source/k).read_bytes())}\n' for k in sorted(selected));assert (dest/'manifest.tsv').read_text()==lines
 elif kind=='manifest':
  paths=manifest(source);lines=''.join(f'{k}\t{paths[k]["size"]}\t{checksum((source/k).read_bytes())}\n' for k in sorted(paths));assert (dest/'manifest.tsv').read_text()==lines
 if kind=='mirror':
  finish=manifest(dest)
  for k,v in start.items():
   if k in finish and v['sha256']==finish[k]['sha256']:assert v['mtime']==finish[k]['mtime'],('identical overwritten',k)

def generate_large(root,count,size):
 root=Path(root);root.mkdir(parents=True,exist_ok=True)
 for i in range(count):
  p=root/f"asset{i:03d}.dat";p.write_bytes(bytes([65+i%26])*size);os.utime(p,(BASE_MTIME,BASE_MTIME))
 return manifest(root)
