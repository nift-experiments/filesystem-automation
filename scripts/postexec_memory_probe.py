"""Separate single-request post-exec memory diagnostic; not official timing data."""
from pathlib import Path
import json,subprocess,os,sys,hashlib
R=Path('/opt/filesystem/suite');os.chdir(R);sys.path.insert(0,str(R/'scripts'))
import fixtures
from run import commands,affinity,digest
rows=[]
for n in [1000,10000,100000]:
 root=R/f'work/fixtures/{n}';dest=R/'work/memory-diagnostic-dest'
 expected=fixtures.expected('walk',root,dest,n,0)
 for engine,command in commands().items():
  p=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,preexec_fn=affinity,start_new_session=True)
  assert p.stdout.readline()==b'BOOT\n'
  p.stdin.write(f'walk|{root}|{dest}|{n}|0\n'.encode());p.stdin.flush()
  actual=sorted(json.loads(p.stdout.readline()));assert actual==expected
  fields={x.split(':')[0]:x.split(':')[1].strip() for x in Path(f'/proc/{p.pid}/status').read_text().splitlines() if x.startswith(('VmHWM:','VmRSS:'))}
  rows.append({'engine':engine,'files':n,'postexec_vmhwm_mib':int(fields['VmHWM'].split()[0])/1024,'postexec_vmrss_mib':int(fields['VmRSS'].split()[0])/1024,'correct':True,'output_sha256':digest(actual)})
  p.stdin.close();assert p.stdout.read()==b'';assert p.wait()==0,p.stderr.read().decode()
print(json.dumps({'diagnostic':'Single walk request per engine/size; /proc VmHWM after complete response before exit, after exec; separate from official wait4 distributions','pass':True,'rows':rows},indent=2))
