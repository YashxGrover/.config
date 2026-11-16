import copy,json,uuid
from pathlib import Path
root=Path(__file__).resolve().parent.parent
cfg=json.loads((root/'workflow/config.json').read_text());base=json.loads((root/'KiwiDesk/profiles/Study.json').read_text())
for desktop in cfg['desktops']:
 p=root/'KiwiDesk/profiles'/f"{desktop['name']}.json";d=json.loads(p.read_text()) if p.exists() else copy.deepcopy(base)
 d.update(name=desktop['name'],default=desktop['number']==1,spaces=['1','2'],space_modes={str(i):('bsp' if desktop['name'] in ('Create','Personal') else 'monocle') for i in range(1,3)},main_spaces=['1'],starter_setup=False)
 if not p.exists():d['id']=str(uuid.uuid4()).upper()
 settings=d['settings'];settings['gap']['global']={'inner':{'horizontal':8,'vertical':8},'outer':{'top':48,'bottom':8,'left':8,'right':8}}
 settings['space_bar']['visibility']='hidden';settings['space_bar']['reserve']=False;settings['kiwishelf']['pocket_visibility']='hidden'
 settings['float_placement']='keep'
 p.write_text(json.dumps(d,indent=2)+'\n')
p=root/'KiwiDesk/gui.json';d=json.loads(p.read_text());d['mode_cycle']=cfg['spaces']['mode_cycle'];d['spaces']=['1','2'];d['space']['slide_duration']=0
for layer in d['layers']:
 if layer['name']=='default':
  layer['bindings']=[{'combo':'control+'+key,'kind':'custom','label':label,'lua':'KiwiDesk.exec('+json.dumps('/usr/bin/python3 '+str(root/'workflow/action.py')+' layout '+direction)+')'} for key,label,direction in [('comma','Previous layout','prev'),('period','Next layout','next')]]
d['look']['style']['gap.global']=base['settings']['gap']['global']={'inner':{'horizontal':8,'vertical':8},'outer':{'top':48,'bottom':8,'left':8,'right':8}}
p.write_text(json.dumps(d,indent=2)+'\n')
(root/'sketchybar/workspaces.json').write_text(json.dumps({'desktops':cfg['desktops'],'space_labels':{}},indent=2)+'\n')
