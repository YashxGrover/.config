#!/usr/bin/env python3
"""Manage the shared desktop workflow catalog without editing generated files."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent
CONFIG = ROOT / 'config.json'

def read():
    return json.loads(CONFIG.read_text())

def validate(data):
    seen = set()
    for app in data['apps']:
        key = app['keys'].lower()
        if key in seen:
            raise ValueError('Duplicate shortcut: ' + key)
        if key.split('+')[0] in {'w','a','s','d','e'}:
            raise ValueError('Reserved workflow shortcut: ' + key)
        seen.add(key)
        if app.get('desktop') is not None and app['desktop'] not in range(1,7):
            raise ValueError('Desktop must be 1–6')
        if app.get('space') is not None and str(app['space']) not in {'1','2','3','4'}:
            raise ValueError('Kiwi Space must be 1–4')
        if app['kind'] == 'app' and not (app.get('bundle_id') or app.get('name')):
            raise ValueError('App needs a name or bundle identifier')
        if app['kind'] == 'command' and not isinstance(app.get('argv'), list):
            raise ValueError('Commands need an argv array, not a shell string')

def save(data):
    validate(data)
    with tempfile.NamedTemporaryFile(mode='w', dir=ROOT, delete=False) as file:
        json.dump(data,file,indent=2,ensure_ascii=False);file.write('\n'); temporary=file.name
    os.replace(temporary,CONFIG)
    guide(data)

def guide(data):
    lines=['# Workflow app shortcuts','','Hold Right Option with all listed keys together.','','| Keys | App/action | Desktop | Kiwi Space |','|---|---|---|---|']
    for item in data['apps']:
        lines.append('| '+ ' | '.join(str(item.get(k) or '—').replace('|','\\|') for k in ['keys','name','desktop','space']) +' |')
    (ROOT/'SHORTCUTS.md').write_text('\n'.join(lines)+'\n')

def ask(label,default=''):
    value=input(label+(' ['+str(default)+']' if default else '')+': ').strip()
    return value or default

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['add','edit','list','validate','guide','open','run'])
    parser.add_argument('key',nargs='?')
    args=parser.parse_args();data=read();validate(data)
    if args.action=='validate':print('Workflow catalog is valid.');return
    if args.action=='guide':guide(data);print(ROOT/'SHORTCUTS.md');return
    if args.action=='open':subprocess.run(['open',str(CONFIG)],check=True);return
    if args.action=='list':
        for item in data['apps']:print(item['keys'].ljust(7),item['name'])
        return
    existing=next((a for a in data['apps'] if a['keys']==args.key),None)
    if args.action=='run':
        if not existing:parser.error('Unknown shortcut')
        if existing['kind']=='app':
            subprocess.run(['open','-b',existing['bundle_id']] if existing.get('bundle_id') else ['open','-a',existing['name']],check=True)
        elif existing['kind']=='url':subprocess.run(['open',existing['url']],check=True)
        else:subprocess.Popen(existing['argv'],shell=False)
        return
    if args.action=='edit' and not existing:parser.error('Use edit KEY with an existing shortcut')
    item=dict(existing or {})
    item['name']=ask('App/action name',item.get('name',''))
    item['keys']=ask('Keys alongside Right Option, e.g. u+5',item.get('keys',args.key or '')).lower()
    item['kind']=ask('Kind: app, url, command',item.get('kind','app'))
    if item['kind']=='app':item['bundle_id']=ask('Bundle identifier (optional)',item.get('bundle_id',''))
    elif item['kind']=='url':item['url']=ask('URL',item.get('url',''))
    elif item['kind']=='command':item['argv']=json.loads(ask('Command argv as JSON',json.dumps(item.get('argv',[]))))
    else:parser.error('Unsupported action kind')
    desktop=ask('Desktop 1–4; blank for no assignment',item.get('desktop') or '')
    space=ask('Kiwi Space 1–4; blank for no assignment',item.get('space') or '')
    item['desktop']=int(desktop) if desktop else None;item['space']=str(space) if space else None
    if existing:data['apps'][data['apps'].index(existing)]=item
    else:data['apps'].append(item)
    save(data);print('Saved catalog and regenerated shortcut guide.')
    print('Live keybindings must be regenerated after catalog changes; this command does not reload the keyboard mapper.')

if __name__=='__main__':
    try:main()
    except (ValueError,OSError,subprocess.CalledProcessError) as error:raise SystemExit(str(error))
