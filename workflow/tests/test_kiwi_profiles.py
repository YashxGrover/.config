import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
class KiwiProfileTests(unittest.TestCase):
 def test_four_profiles_have_four_monocle_spaces_and_geometry(self):
  for name in ['Study','Browse','Create','Personal']:
   d=json.loads((ROOT/'KiwiDesk/profiles'/f'{name}.json').read_text())
   self.assertEqual(d['spaces'],['1','2','3','4'])
   self.assertEqual(d['space_modes'],{str(i):'monocle' for i in range(1,5)})
   self.assertEqual(d['settings']['float_placement'],'keep')
   self.assertEqual(d['settings']['gap']['global']['outer'],{'top':48,'bottom':8,'left':8,'right':8})
 def test_profile_routes_match_approved_assignments(self):
  expected={'Study':{'md.obsidian':'1','com.apple.Preview':'2'},'Browse':{'com.pauldavis.crest':'1','com.apple.Safari':'2'},'Create':{'net.kovidgoyal.kitty':'1','ai.opencode.desktop':'2'},'Personal':{'com.spotify.client':'2','com.apple.mail':'1'}}
  for profile,routes in expected.items():
   actual=json.loads((ROOT/'KiwiDesk/profiles'/f'{profile}.json').read_text())['app_rules']
   for bundle,space in routes.items():self.assertEqual(actual[bundle],space)
 def test_global_app_routes_do_not_override_profiles(self):
  d=json.loads((ROOT/'KiwiDesk/gui.json').read_text())
  self.assertEqual(d['app_rules'],{})
  self.assertEqual(d['spaces'],['1','2','3','4'])
  self.assertEqual(d['mode_cycle'],['monocle','stack','bsp','grid','track','scrolling'])
if __name__=='__main__':unittest.main()
