"""Enforce refresh-only capability/exactly-once findings from retained semantics probes."""
from pathlib import Path
import hashlib,json,subprocess
import run
R=run.R
candidate='7f7e487c47a87e871dfef53345e2b71288008bff'
source=R/'work/nift-source'
assert subprocess.check_output(['git','-C',str(source),'rev-parse','HEAD'],text=True).strip()==candidate
assert not subprocess.check_output(['git','-C',str(source),'status','--porcelain'],text=True).strip()
rows=json.loads((R/'work/semantics/observations.json').read_text())
assert sum(bool(x.get('edge_paths_pass')) for x in rows)==5
missing=next(x for x in rows if x.get('engine')=='nift' and 'missing_directory_exit' in x)
assert missing['missing_directory_exit']!=0,'Nift missing-directory behavior changed; review capability contract'
stat=next(x for x in rows if x.get('expression','').startswith('print(stat('))
value=json.loads(stat['stdout']);assert stat['exit']==0 and {'exists','type','size'}<=value.keys()
assert not any('time' in k.lower() for k in value),'New timestamp capability requires a documented supplement'
sha=next(x for x in rows if 'sha256' in x.get('expression',''))
assert sha['exit']!=0 and 'undefined callable: sha256' in sha['stderr'],'SHA capability changed; certify native supplement'
remove=next(x for x in rows if 'make_dir' in x.get('expression',''))
assert remove['exit']!=0 and 'directories are not removed recursively' in remove['stderr']
inline=next(x for x in rows if 'inline_form_execute_count' in x)
assert inline['exit']==0 and inline['inline_form_execute_count']==1,'Exactly-once correctness blocker'
outputs={}
for name in ['inline-loop.f','bound-loop.f']:
 p=subprocess.run([run.commands()['nift'][0],str(R/'repro'/name)],input='walk|3\n',text=True,capture_output=True,timeout=10)
 assert p.returncode==0 and p.stdout.count('CALLED')==1,(name,p.stdout,p.stderr)
 assert json.loads(p.stdout.splitlines()[-1])==[['walk',3,0]]
 outputs[name]={'execute_count':1,'stdout_sha256':hashlib.sha256(p.stdout.encode()).hexdigest()}
receipt={'pass':True,'candidate_sha':candidate,'scope':'untimed refresh semantic/capability gates','edge_path_engines':5,'inline_execute_count':1,'repro':outputs,'remaining_gaps':['native SHA-256','stat timestamp','recursive directory removal'],'missing_directory_behavior':'Nift errors; Python empty-success behavior retained as non-equivalence'}
(R/'work/refresh-semantic-acceptance.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt))
