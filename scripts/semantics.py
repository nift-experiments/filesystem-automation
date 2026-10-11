from pathlib import Path
import sys,subprocess,json,time,os
sys.path.insert(0,str(Path(__file__).resolve().parent));import run,fixtures
R=run.R;out=R/'work/semantics';out.mkdir(exist_ok=True);records=[]
root=out/'paths';root.mkdir(exist_ok=True)
for rel in ['space dir/a b.txt','unicode-ü/naïve.txt','empty.dat']:
 p=root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('abc' if 'empty' not in rel else '')
expected=fixtures.expected('walk',root,out/'dest',3,0);request=f'walk|{root}|{out}/dest|3|0\n'
for e in run.ENGINES:
 actual,metrics=run.measure(e,request,'fresh');assert actual==expected;records.append({'engine':e,'edge_paths_pass':True,'rows_sha256':run.digest(actual)})
missing=out/'missing'
for e in run.ENGINES:
 p=subprocess.run(run.commands()[e],input=f'walk|{missing}|{out}/dest|0|0\n',text=True,capture_output=True,timeout=10)
 # Python os.walk silently returns no entries; others signal errors. Explicitly record rather than invent parity.
 records.append({'engine':e,'missing_directory_exit':p.returncode,'stdout':p.stdout[-500:],'stderr':p.stderr[-700:]})
for expr in ['print(stat("README.md").stringify())','print(sha256("abc"))','make_dir("work/semantics/remove-dir"); remove("work/semantics/remove-dir")']:
 p=subprocess.run([run.commands()['nift'][0],'-e',expr],text=True,capture_output=True,timeout=10);records.append({'engine':'nift','expression':expr,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
# Retain a diagnostic inline-result form, separate from accepted source.
s=(R/'adapters/nift.f').read_text().replace('fn(execute(kind,root,dest,n,variant)) {','fn(execute(kind,root,dest,n,variant)) { print("EXECUTE");').replace('result := execute(p[0],p[1],p[2],p[3].to_int(),p[4].to_int()); print(result.stringify())','print(execute(p[0],p[1],p[2],p[3].to_int(),p[4].to_int()).stringify())')
q=out/'inline-result.f';q.write_text(s);p=subprocess.run([run.commands()['nift'][0],str(q)],input=request,text=True,capture_output=True,timeout=10);records.append({'engine':'nift','inline_form_execute_count':p.stdout.count('EXECUTE'),'stdout':p.stdout,'stderr':p.stderr,'exit':p.returncode})
(out/'observations.json').write_text(json.dumps(records,indent=2)+'\n');print(json.dumps(records[-1]))
