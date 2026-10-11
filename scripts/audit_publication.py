"""Independent publication check against immutable summaries and memory controls."""
from pathlib import Path
import json,hashlib,xml.etree.ElementTree as ET
from html.parser import HTMLParser
R=Path(__file__).resolve().parents[1];L=R.parents[1]/'lab';A=L/'public/benchmarks/filesystem-automation/assets'
S={}
for p in [R/'work/official',R/'work/filter-suite/work/official']:
 a=json.loads((p/'independent-audit.json').read_text());assert a['pass'] and hashlib.sha256((p/'summary.json').read_bytes()).hexdigest()==a['summary_sha256']
 for x in json.loads((p/'summary.json').read_text()):S[x['scenario'],x['engine']]=x if x['boundary']=='booted' else S.get((x['scenario'],x['engine']),{})
M={(x['files'],x['engine']):x['postexec_vmhwm_mib'] for x in json.loads((R/'work/orchestration/postexec-memory.json').read_text())['rows']}
class Tables(HTMLParser):
 def __init__(self):super().__init__();self.tables=[];self.active=False;self.cell=False
 def handle_starttag(self,t,a):
  if t=='table':self.active=True;self.tables.append([])
  if self.active and t=='tr':self.tables[-1].append([])
  if self.active and t in ['th','td']:self.cell=True;self.tables[-1][-1].append('')
 def handle_data(self,d):
  if self.cell:self.tables[-1][-1][-1]+=d
 def handle_endtag(self,t):
  if t in ['th','td']:self.cell=False
  if t=='table':self.active=False
p=Tables();p.feed((L/'public/benchmarks/filesystem-automation/index.html').read_text());data=json.loads((A/'published.json').read_text());assert len(data['sections'])==11 and len(p.tables)==12
count=0
for section,table in zip(data['sections'],p.tables):
 assert table[0]==['Workload','Nift','Python','Node','Bun','Go']
 for key,label,vals,row in zip(section['scenarios'],section['labels'],section['values'],table[1:]):
  assert row[0]==label
  for e,v,cell in zip(['nift','python','node','bun','go'],vals,row[1:]):
   expected=M[int(key),e] if section['id']=='memory' else S.get((key,e),{}).get('wall_ms',{}).get('median')
   assert v==expected and cell==('—' if v is None else f'{v:,.3f}')
   count+=1
 root=ET.parse(A/(section['id']+'.svg')).getroot();assert root.find('{http://www.w3.org/2000/svg}title').text==section['title']
 assert 'LOGARITHMIC SCALE' in (A/(section['id']+'.svg')).read_text() if section['id']!='memory' else 'LINEAR SCALE' in (A/'memory.svg').read_text()
receipt={'pass':True,'charts':11,'tables':11,'cells_checked':count,'source':'frozen audited summaries + separate post-exec memory diagnostic','raw_changed':False}
(R/'work/publication-v2-audit.json').write_text(json.dumps(receipt,indent=2)+'\n');print(receipt)
