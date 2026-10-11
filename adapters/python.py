import os,sys,json,hashlib,shutil
from pathlib import Path

def checksum(b):
 h=0
 for x in b:h=(h*31+x)%1000000007
 return h

def walk(root):
 for base,dirs,files in os.walk(root):
  for d in dirs:yield os.path.relpath(os.path.join(base,d),root),True
  for f in files:yield os.path.relpath(os.path.join(base,f),root),False

def execute(kind,root,dest,n,variant):
 rows=[];entries=list(walk(root));lines=[]
 if kind=='relocate':
  os.makedirs(dest+'/moved',exist_ok=True)
  for name in os.listdir(dest):
   if name!='moved':os.rename(dest+'/'+name,dest+'/moved/'+name)
 for rel,directory in entries:
  p=root+'/'+rel;q=dest+'/'+rel
  if directory:
   if kind=='walk':rows.append([rel,-1,0])
   continue
  size=0;v=0
  if kind=='walk':rows.append([rel,0,0]);continue
  if kind=='mixed' and (rel.startswith('group19/') or not rel.endswith(('.md','.dat'))):continue
  size=os.stat(p).st_size
  if kind=='filter':
   if int(Path(rel).stem[1:])%100>=variant:continue
  if kind in {'read','hash-portable','mirror','detect-hash','clean','manifest','generate','mixed'}:v=checksum(Path(p).read_bytes())
  if kind=='large-read':
   b=Path(p).read_bytes();v=b[0]*256+b[-1]
  if kind=='hash-sha256':v=hashlib.sha256(Path(p).read_bytes()).hexdigest()
  if kind=='detect-mtime':
   if os.path.exists(q) and int(os.stat(p).st_mtime)==int(os.stat(q).st_mtime):continue
  if kind=='detect-hash':
   if os.path.exists(q) and v==checksum(Path(q).read_bytes()):continue
  if kind=='clean':
   if not os.path.exists(q):rows.append([rel,'missing',0])
   elif v!=checksum(Path(q).read_bytes()):rows.append([rel,'modified',0])
   continue
  if kind=='mixed' and not rel.endswith(('.md','.dat')):continue
  if kind in {'write','overwrite','copy','mirror','generate','mixed','large-write'}:
   os.makedirs(os.path.dirname(q),exist_ok=True)
   if kind=='mixed' and rel.endswith('.dat'):shutil.copyfile(p,q)
   elif kind in {'generate','mixed'}:Path(q+'.generated').write_bytes(b'generated\n'+Path(p).read_bytes())
   elif kind=='mirror':
    if not os.path.exists(q) or v!=checksum(Path(q).read_bytes()):shutil.copyfile(p,q)
   elif kind=='copy':shutil.copyfile(p,q)
   else:Path(q).write_bytes(Path(p).read_bytes())
  if kind=='rename':os.rename(q,q+'.renamed')
  if kind=='delete':os.unlink(q)
  if kind in {'manifest','generate','mixed'}:lines.append((rel,f'{rel}\t{size}\t{v}\n'))
  rows.append([rel,size,v])
 if kind in {'mirror','clean'}:
  for rel,d in walk(dest):
   if not d and not os.path.exists(root+'/'+rel):
    if kind=='mirror':os.unlink(dest+'/'+rel)
    else:rows.append([rel,'unexpected',0])
 if kind in {'manifest','generate','mixed'}:Path(dest+'/manifest.tsv').write_text(''.join(v for _,v in sorted(lines)))
 return rows
print('BOOT',flush=True)
for line in sys.stdin:
 p=line.strip().split('|');print(json.dumps(execute(p[0],p[1],p[2],int(p[3]),int(p[4])),separators=(',',':')),flush=True)
