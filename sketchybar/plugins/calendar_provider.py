#!/usr/bin/python3
"""Shared Calendar data for the next-event label and calendar popup."""
import calendar,datetime as dt,json,os,re,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SB='/opt/homebrew/bin/sketchybar'
CACHE=ROOT/'runtime/calendar.json'
RECORD='\x1e';FIELD='\x1f'
def parse(text,now):
    events=[]
    for record in text.split(RECORD):
        if FIELD not in record:continue
        date_text,title=record.split(FIELD,1)
        date=re.search(r'\d{4}-\d{2}-\d{2}',date_text)
        clock=re.search(r'\b(\d{2}:\d{2})\b',date_text)
        if not clock:continue
        day=date.group() if date else now.strftime('%Y-%m-%d')
        try:start=dt.datetime.strptime(day+' '+clock.group(),'%Y-%m-%d %H:%M')
        except ValueError:continue
        title=' '.join(title.split())
        if start>now and title:events.append({'title':title,'start':start.isoformat()})
    return sorted(events,key=lambda e:e['start'])
def read_events():
    if CACHE.exists():
        try:
            value=json.loads(CACHE.read_text())
            if 0<=time.time()-value['fetched']<60:
                value['events']=[e for e in value['events'] if dt.datetime.fromisoformat(e['start'])>dt.datetime.now()]
                return value
        except (ValueError,KeyError,OSError):pass
    helper=next((p for p in ['/opt/homebrew/bin/icalBuddy','/usr/local/bin/icalBuddy'] if Path(p).exists()),None)
    value={'fetched':time.time(),'events':[],'error':None}
    try:
        if not helper:raise OSError('Calendar helper missing')
        args=[helper,'-nc','-nrd','-npn','-ea','-eed','-b',RECORD,'-ab',RECORD,'-iep','title,datetime','-po','datetime,title','-ps','|'+FIELD+'|','-df','%Y-%m-%d','-tf','%H:%M','eventsToday+1']
        result=subprocess.run(args,capture_output=True,text=True,check=True,timeout=8)
        if result.stderr.strip():raise OSError(result.stderr.strip())
        value['events']=parse(result.stdout,dt.datetime.now())
    except (OSError,subprocess.SubprocessError) as error:value['error']=str(error)
    CACHE.parent.mkdir(parents=True,exist_ok=True)
    temporary=CACHE.with_suffix('.tmp');temporary.write_text(json.dumps(value));temporary.replace(CACHE)
    return value

def label(event,now):
    start=dt.datetime.fromisoformat(event['start'])
    prefix='Tomorrow ' if start.date()==now.date()+dt.timedelta(days=1) else ''
    return f"{event['title']} · {prefix}{start:%H:%M}"

def main():
    data=read_events();now=dt.datetime.now();args=[SB]
    if len(sys.argv)>1 and sys.argv[1]=='popup':
        month=calendar.TextCalendar(firstweekday=0).formatmonth(now.year,now.month).splitlines()
        for i in range(8):args+=['--set',f'clock.cal{i+1}','label='+(month[i] if i<len(month) else '')]
        for i in range(5):
            text=label(data['events'][i],now) if i<len(data['events']) else ''
            if i==0 and not text:text='Calendar unavailable — check access in macOS' if data['error'] else 'No upcoming events today or tomorrow'
            args+=['--set',f'clock.ev{i+1}','label='+text,'drawing='+('on' if text else 'off')]
        args+=['--set','clock','popup.drawing=toggle']
    else:
        args+=['--set',os.environ.get('NAME','calendar_event'),'drawing='+('on' if data['events'] else 'off')]
        if data['events']:args+=['label='+label(data['events'][0],now)]
    subprocess.run(args,check=False,timeout=5)
if __name__=='__main__':main()
