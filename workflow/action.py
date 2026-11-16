#!/usr/bin/env python3
"""Runtime actions for the Right Option workflow layer."""
import json,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
KD='/opt/homebrew/bin/kiwidesk'
def run(cmd,*args):
 p=subprocess.run([KD,cmd,*map(str,args)],capture_output=True,text=True,timeout=10)
 if p.returncode:raise RuntimeError(p.stderr or p.stdout)
 try:
  value=json.loads(p.stdout)
  if isinstance(value,dict) and value.get('error'):raise RuntimeError(str(value['error']))
  return value
 except json.JSONDecodeError:return p.stdout

def main():
 action,*args=sys.argv[1:];cfg=json.loads((ROOT/'config.json').read_text())
 if action=='app':
  item=next(x for x in cfg['apps'] if x['keys']==args[0]);bundle=item.get('bundle_id')
  if item['kind']!='app':subprocess.run([sys.executable,str(ROOT/'manage.py'),'run',args[0]],check=True);return
  if item['name']=='Finder':run('move_here',bundle);return
  state=run('get_state')
  windows=state.get('windows',[])+state.get('away_windows',[])
  if item.get('desktop') and not any(w.get('bundle_id','').lower()==(bundle or '').lower() for w in windows):
   run('focus_desktop',item['desktop'])
   run('focus_space','1')
  run('focus_or_spawn',bundle);return
 if action=='cycle-space':
  state=run('get_state');ids=[str(s['id']) for s in state['spaces']];run('focus_space',ids[(ids.index(str(state['active_space']))+1)%len(ids)]);return
 if action=='layout':
  state=run('get_state')
  run('cycle_mode',args[0])
  return
 if action=='guide':subprocess.run(['open',str(ROOT/'SHORTCUTS.md')],check=True);return
 if action=='theme':subprocess.run(['/usr/bin/python3',str(ROOT.parent/'appearance/appearance.py'),'menu'],check=True);return
 if action=='resize':
  state=run('get_state');sid=str(state['active_space']);mode=next(s['mode'] for s in state['spaces'] if str(s['id'])==sid)
  if mode not in ['stack','bsp']:run('resize',args[0],int(args[1])*40);return
  profile=run('get_profile_status').get('name','');file=ROOT.parent/'KiwiDesk/profiles'/f'{profile}.json'
  data=json.loads(file.read_text());settings=data['settings'];axis,delta=args[0],int(args[1])
  name='master_ratio' if mode=='stack' else 'ratio_'+('h' if axis=='x' else 'v')
  # Saved per-Space layout tuning; each profile owns its own values.
  store=ROOT/'ratios.json';ratios=json.loads(store.read_text()) if store.exists() else {}
  key=f'{profile}:{sid}:{mode}:{name}';current=ratios.get(key,settings['layout'][mode].get(name,.5))
  value=max(.15,min(.85,current+.05*delta));run(f'{mode}.set_{name}_override',sid,value)
  ratios[key]=value;store.write_text(json.dumps(ratios,indent=2)+'\n')
  return
 run(action,*args)

if __name__=='__main__':
 try:main()
 except Exception as error:
  with (ROOT/'errors.log').open('a') as f:f.write(time.strftime('%Y-%m-%d %H:%M:%S')+' '+str(error)+'\n')
  raise SystemExit(str(error))
