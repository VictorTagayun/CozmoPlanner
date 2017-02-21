import asyncio
import cozmo
from Common.woc import WOC
from Common.colors import Colors
from os import system
import random
import _thread
import sys
from threading import Timer
import httplib2
import os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from datetime import datetime
from dateutil import parser
import pytz
# pip3 install python-dateutil

'''
Planner Module
@class Planner
@author - Team Wizards of Coz
'''

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_id.json'
APPLICATION_NAME = 'WizardsOfCoz'
TZ = pytz.timezone('US/Eastern')

class Planner(WOC):
    
    cl = None
    exit_flag = False
    audioThread = None
    cubes = None
    pollDuration = 120
    timeToEvent = 100
    
    
    def __init__(self, *a, **kw):
        
        sys.setrecursionlimit(0x100000)
        cozmo.setup_basic_logging()
        cozmo.connect(self.startResponding)
        
        
        
    def startResponding(self, coz_conn):
        asyncio.set_event_loop(coz_conn._loop)
        self.coz = coz_conn.wait_for_robot()
        
        self.pollCalendar()
        
        while not self.exit_flag:
            asyncio.sleep(0)
        self.coz.abort_all_actions()
    
    
    
    def pollCalendar(self):
        
        credentials = self.getCredentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)
    
        noww = datetime.utcnow()
        now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        print('Getting the upcoming event')
        eventsResult = service.events().list(
            calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
            orderBy='startTime').execute()
        events = eventsResult.get('items', [])
        
        if not events:
            print('No upcoming events found.')
        else:
            self.processEvent(events)
        Timer(self.pollDuration, self.pollCalendar).start()
        
    
    
    def hours_minutes(self,td):
        return td.seconds//3600, (td.seconds//60)%60
    
    
    
    def processEvent(self,events):
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            startDate = parser.parse(start)
            todayTZ = TZ.localize(datetime.today())
            
            if startDate.date()==todayTZ.date():
                hours,minutes = self.hours_minutes(startDate-todayTZ)
                totalMinutes = (hours*60) + minutes
                
                if totalMinutes < self.timeToEvent:
                    self.announceEvent(event,totalMinutes)
    
    
    
    
    def announceEvent(self,event,minutes):
        evtText = "You have "+event['summary']+"in "+str(minutes)+" minutes";
        print(evtText)
#         self.coz.say_text(evtText).wait_for_completed()
    
    
    
    def getCredentials(self):
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,'calendar-python-quickstart.json')
    
        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials
   
            


if __name__ == '__main__':
    Planner()