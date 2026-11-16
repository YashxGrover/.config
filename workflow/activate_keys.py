#!/usr/bin/env python3
"""Generate Karabiner's Right Option layer from the shared catalog."""
import json,shlex
from pathlib import Path
ROOT=Path(__file__).resolve().parent
config=json.loads((ROOT/'config.json').read_text())
path=ROOT.parent/'karabiner/karabiner.json';data=json.loads(path.read_text())
profile=next(x for x in data['profiles'] if x.get('selected'))
condition={'type':'variable_if','name':'yash_workflow','value':1}
mods=[]
def add(keys,action,args=(),mandatory=()):
 source={'key_code':keys} if isinstance(keys,str) else {'simultaneous':[{'key_code':k} for k in keys],'simultaneous_options':{'detect_key_down_uninterruptedly':True,'key_down_order':'insensitive','key_up_order':'insensitive','key_up_when':'any'}}
 source['modifiers']={'mandatory':list(mandatory),'optional':['caps_lock']}
 mods.append({'type':'basic','from':source,'conditions':[condition],'to':[{'shell_command':shlex.join(['/usr/bin/python3',str(ROOT/'action.py'),action,*map(str,args)])}]})
# Chords precede single keys, so i+1 is one operation regardless of key order.
for n in range(1,7):add(['q',str(n)],'move_to_desktop',[n])
for a in sorted(config['apps'],key=lambda x:-len(x['keys'])):add(a['keys'].split('+') if '+' in a['keys'] else a['keys'],'app',[a['keys']])
for key,direction in zip('wasd',['up','left','down','right']):
 add(key,'focus',[direction]);add(key,'swap',[direction],['shift'])
for key,axis,delta in [('a','x',-1),('d','x',1),('w','y',-1),('s','y',1)]:add(key,'resize',[axis,delta],['control'])
for n in range(1,7):
 add(str(n),'focus_desktop',[n]);add(str(n),'move_to_desktop_and_follow',[n],['shift'])
for key,action,args in [('left_arrow','focus',['left']),('right_arrow','focus',['right']),('return_or_enter','toggle_maximized',[]),('delete_or_backspace','pocket',[]),('spacebar','toggle_floating',[]),('slash','guide',[]),('e','theme',[])]:add(key,action,args,['shift'] if key in ('spacebar','e') else [])
mods.insert(0,{'type':'basic','from':{'key_code':'right_option','modifiers':{'optional':['any']}},'to':[{'set_variable':{'name':'yash_workflow','value':1}}],'to_after_key_up':[{'set_variable':{'name':'yash_workflow','value':0}}]})
rules=profile.setdefault('complex_modifications',{}).setdefault('rules',[])
rules[:]=[r for r in rules if r.get('description')!='Yash workflow — Right Option']
rules.append({'description':'Yash workflow — Right Option','manipulators':mods})
path.write_text(json.dumps(data,indent=2)+'\n')
print('Installed',len(mods),'Right Option mappings in selected Karabiner profile')
