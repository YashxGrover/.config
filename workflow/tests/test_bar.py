import importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('workspaces',ROOT/'sketchybar/plugins/workspaces.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class RenderTests(unittest.TestCase):
 def test_desktops_current_space_and_app_deduplication(self):
  config=json.loads((ROOT/'sketchybar/workspaces.json').read_text())
  palette=module.colors()
  state={'desktop':2,'active_space':'3','spaces':[{'id':str(n),'mode':'monocle','windows':[1,2] if n==3 else []} for n in range(1,5)],'windows':[{'id':1,'bundle_id':'example.app','app':'Example'},{'id':2,'bundle_id':'example.app','app':'Example'}]}
  args=module.render(state,'Browse',config,palette);items={}
  for i,arg in enumerate(args):
   if arg=='--set':
    name=args[i+1];end=next((j for j in range(i+2,len(args)) if args[j]=='--set'),len(args));items.setdefault(name,[]).extend(args[i+2:end])
  self.assertIn('label=Browse',items['desktop.tab2']);self.assertIn('label=',items['desktop.tab1'])
  self.assertIn('label=3',items['kiwi.current'])
  for n in range(1,5):self.assertIn('drawing=off',items['kiwi.tab'+str(n)])
  self.assertIn('drawing=on',items['window.tab1']);self.assertIn('drawing=off',items['window.tab2'])
  self.assertTrue(any(' app example.app' in v for v in items['window.tab1']))
 def test_removed_features_are_not_created(self):
  config=(ROOT/'sketchybar/sketchybarrc').read_text()
  self.assertNotIn('for resource in',config)
  self.assertIn('--add item media q',config);self.assertIn('--add item calendar_event e',config)
  self.assertIn('update_freq=0',config)
if __name__=='__main__':unittest.main()
