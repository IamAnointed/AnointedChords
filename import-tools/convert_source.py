"""Best-effort SOURCE-only Excel converter. Run: python convert_source.py drive_chords.zip
Requires: pip install openpyxl. Output: songs.json and review.csv.
Only imports source-side chord cells; not transposed-side. Review all output manually.
"""
import sys,zipfile,io,json,csv,re
from pathlib import Path
from openpyxl import load_workbook
CHORD=re.compile(r'^[A-G](?:#|b)?(?:m|maj|min|dim|aug|sus|add|M|\d|\+|\-|/|\(|\)|#|b)*$',re.I)
LABEL=re.compile(r'^(intro|verse|chorus|bridge|refrain|pre.?chorus|outro|instrumental|instru|bassline|interlude|tag|ending|v\d+|c\d+)',re.I)
def convert(name,content):
 w=load_workbook(io.BytesIO(content),read_only=True,data_only=True)
 sh=w.active
 # SOURCE occupies left block; TRANSPOSED begins around column T in source templates.
 rows=list(sh.iter_rows(min_row=1,max_col=19,values_only=True))
 title=Path(name).stem.strip();key=''; sections=[]; current=None; counts=0
 for row in rows:
  vals=[str(x).strip() if x is not None else '' for x in row]
  for j,v in enumerate(vals):
   if v.lower()=='key:' and j+1<len(vals):key=vals[j+1].strip()
  items=[v for v in vals if v]
  if not items:continue
  first=items[0]
  if LABEL.match(first) and len(first)<35:
   current={'name':first,'rows':[]};sections.append(current);continue
  chords=[v for v in vals if v and CHORD.fullmatch(v) and len(v)<18]
  if chords:
   if current is None:current={'name':'Intro','rows':[]};sections.append(current)
   current['rows'].append({'cells':[{'count':4,'chord':c} for c in chords]});counts+=len(chords)
 return {'title':title,'key':key or 'C','sections':[x for x in sections if x['rows']]},counts

def main(path):
 src=Path(path);entries=[]
 if src.is_dir():entries=[(p.name,p.read_bytes()) for p in src.rglob('*.xlsx')]
 else:
  with zipfile.ZipFile(src) as z:entries=[(n,z.read(n)) for n in z.namelist() if n.lower().endswith('.xlsx') and not Path(n).name.startswith('~$')]
 out=[];review=[]
 for name,blob in entries:
  try:
   song,count=convert(name,blob);out.append(song)
   review.append([name,song['title'],song['key'],len(song['sections']),count,'REVIEW: source only; lyrics not included by grid format'])
  except Exception as e:review.append([name,'','','','','ERROR: '+str(e)])
 Path('songs.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
 with open('review.csv','w',newline='',encoding='utf-8-sig') as f:
  writer=csv.writer(f);writer.writerow(['file','title','key','sections','chord_cells','status']);writer.writerows(review)
 print('Converted',len(out),'of',len(entries),'files. Review songs.json and review.csv before import.')
if __name__=='__main__':
 if len(sys.argv)!=2:raise SystemExit('Usage: python convert_source.py drive_chords.zip')
 main(sys.argv[1])
