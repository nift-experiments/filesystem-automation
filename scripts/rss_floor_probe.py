"""Post-campaign launch-accounting diagnostic, never an official timing cell."""
import json,os,subprocess,sys
if len(sys.argv)>1:
 retained=bytearray(int(sys.argv[1])*1024*1024)
 for i in range(0,len(retained),4096):retained[i]=1
 parent=[x.strip() for x in open('/proc/self/status') if x.startswith(('VmRSS:','VmHWM:'))]
 def affinity():os.sched_setaffinity(0,sorted(os.sched_getaffinity(0))[:4])
 p=subprocess.Popen(['/usr/bin/true'],preexec_fn=affinity,start_new_session=True)
 _,status,u=os.wait4(p.pid,0);p.returncode=os.waitstatus_to_exitcode(status)
 assert p.returncode==0
 print(json.dumps({'parent_allocated_mib':int(sys.argv[1]),'parent_status':parent,'true_child_wait4_maxrss_mib':u.ru_maxrss/1024,'returncode':p.returncode}))
else:
 rows=[json.loads(subprocess.check_output([sys.executable,__file__,str(n)],text=True)) for n in [0,64]]
 assert rows[1]['true_child_wait4_maxrss_mib']-rows[0]['true_child_wait4_maxrss_mib']>50
 print(json.dumps({'diagnostic':'fork/preexec wait4 RSS floor; no runtime work in true child','python':sys.version,'kernel':os.uname().release,'pass':True,'controls':rows},indent=2))
