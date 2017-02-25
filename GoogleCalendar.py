import asyncio
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

'''
GoogleCalendar Module
@class GoogleCalendar
@author - Team Wizards of Coz
'''

class GoogleCalendar():
    
    pollDuration = 120
    timeToEvent = 100
    flags = None
    scopes = None
    secret_file = None
    app_name = None
    tz = None
    
    
    def __init__(self,scopes,secret_file,app_name,tz):
        
        self.scopes = scopes
        self.secret_file = secret_file
        self.app_name = app_name
        self.tz = pytz.timezone(tz)
        
        try:
            import argparse
            self.flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        except ImportError:
            self.flags = None
        
    
    
    
    def pollCalendar(self):
        
        # GOOGLE CALENDAR
        credentials = self.getCredentials()
        http = credentials.authorize(httplib2.Http())
        self.service = discovery.build('calendar', 'v3', http=http)
        
        Timer(self.pollDuration, self.pollCalendar).start()
    
    
    
    
    def listNUpcomingEvents(self,num):
        
        now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        print('Getting the upcoming event')
        eventsResult = self.service.events().list(
            calendarId='primary', timeMin=now, maxResults=num, singleEvents=True,
            orderBy='startTime').execute()
        events = eventsResult.get('items', [])
        
        if not events:
            print('No upcoming events found.')
            return []
        else:
            return events
    
    
    
    def todaysEventAndTimeToEvent(self):
        
        events = self.listNUpcomingEvents(5)
        
        if not events:
            print('No upcoming event found today')
            return None,-1
        else:
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                startDate = parser.parse(start)
                todayTZ = self.tz.localize(datetime.today())
                if startDate.date()==todayTZ.date():
                    if startDate>todayTZ:
                        hours,minutes = self.hours_minutes(startDate-todayTZ)
                        totalMinutes = (hours*60) + minutes
                        return event,totalMinutes
            return None,-1    
                    
    
    
    def getCredentials(self):
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,'calendar-python-quickstart.json')
    
        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.secret_file, self.scopes)
            flow.user_agent = self.app_name
            if self.flags:
                credentials = tools.run_flow(flow, store, self.flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials
   
   
     
    def hours_minutes(self,td):
        return td.seconds//3600, (td.seconds//60)%60



if __name__ == '__main__':
    GoogleCalendar()