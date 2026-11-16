#!/usr/bin/env python3
"""Apply agreed per-profile window routing without contacting KiwiDesk."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
ROUTES={
 'Study':{
  'md.obsidian':'1','com.apple.Safari.WebApp.3E44B9DB-6CFD-40C1-B59A-113A79BAAB91':'1',
  'com.apple.Safari.WebApp.7D6FA221-2D9B-4ED7-8B48-017456C26BBA':'1','com.index0.app':'1',
  'com.microsoft.edgemac.app.pclfgflcpfaoljnfkkdaehijdkagjkgj':'2','com.apple.Preview':'2'},
 'Browse':{
  'com.pauldavis.crest':'1','com.phibrowser.Mac':'2','net.imput.helium':'2',
  'com.apple.Safari':'2','com.microsoft.edgemac':'2'},
 'Create':{
  'com.microsoft.VSCode':'1','com.github.GitHubClient':'1','com.apple.dt.Xcode':'1','net.kovidgoyal.kitty':'1',
  'com.todesktop.230313mzl4w4u92':'2','com.google.antigravity':'2','ai.opencode.desktop':'2'},
 'Personal':{
  'com.hnc.Discord':'1','com.apple.MobileSMS':'1','com.apple.mail':'1','com.spotify.client':'2'},
}
for name,routes in ROUTES.items():
 path=ROOT/'KiwiDesk/profiles'/f'{name}.json';data=json.loads(path.read_text())
 spaces=['1','2']
 if data.get('spaces')!=spaces:raise SystemExit(f'{name}: expected 2 spaces, found {data.get("spaces")}')
 data['app_rules']=routes
 data['space_modes']={s:('bsp' if name in ('Create','Personal') else 'monocle') for s in spaces}
 data['settings']['float_placement']='keep'
 data['settings']['gap']['global']={'inner':{'horizontal':8,'vertical':8},'outer':{'top':48,'bottom':8,'left':8,'right':8}}
 path.write_text(json.dumps(data,indent=2)+'\n')
# Make root behavior safe: absent per-profile app rule means default-placement, no global routing.
gui_path=ROOT/'KiwiDesk/gui.json';gui=json.loads(gui_path.read_text());gui['app_rules']={}
gui['spaces']=['1','2'];gui['mode_cycle']=['monocle','stack','bsp','grid','track','scrolling']
gui['float_placement']='keep'
gui_path.write_text(json.dumps(gui,indent=2)+'\n')
print('Updated four profiles with per-profile routing and kept gap/float settings.')
