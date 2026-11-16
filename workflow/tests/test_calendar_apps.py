import datetime as dt,importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def load(name):
 spec=importlib.util.spec_from_file_location(name,ROOT/'sketchybar/plugins'/f'{name}.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
calendar=load('calendar_provider');apps=load('shelf_action')
class CalendarTests(unittest.TestCase):
 def test_filters_started_and_preserves_title_numbers(self):
  now=dt.datetime(2026,11,14,10)
  text='\x1e2026-11-14 at 09:00\x1fOld event\n\x1e2026-11-15 at 08:30\x1fTest 12:45 chapter\n\x1e2026-11-14 at 13:00\x1fToday\n'
  result=calendar.parse(text,now)
  self.assertEqual([r['title'] for r in result],['Today','Test 12:45 chapter'])
  self.assertEqual(calendar.label(result[1],now),'Test 12:45 chapter · Tomorrow 08:30')
 def test_empty_and_malformed(self):
  self.assertEqual(calendar.parse('error\x1ebad date\x1fNo time',dt.datetime.now()),[])
class WindowTests(unittest.TestCase):
 def state(self,focused):return {'active_space':'1','spaces':[{'id':'1','focused':focused}], 'windows':[{'id':10,'bundle_id':'app'},{'id':20,'bundle_id':'app'},{'id':30,'bundle_id':'other'}]}
 def test_first_click_returns_to_remembered_window(self):self.assertEqual(apps.choose_app_window(self.state(30),'app',{'app':20}),20)
 def test_repeated_click_cycles_and_wraps(self):
  self.assertEqual(apps.choose_app_window(self.state(10),'app',{}),20)
  self.assertEqual(apps.choose_app_window(self.state(20),'app',{}),10)
 def test_closed_remembered_window_falls_back(self):self.assertEqual(apps.choose_app_window(self.state(30),'app',{'app':999}),10)
if __name__=='__main__':unittest.main()
