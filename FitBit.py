import asyncio
from os import system
import random
from rauth.service import OAuth2Service
import _thread
import sys
import webbrowser
from threading import Timer
import re
import os
from datetime import datetime
from dateutil import parser
import pyowm
import pytz
import requests
# pip3 insstall rauth
# pip3 install python-dateutil
# pip3 install pyowm

'''
FitBit Module
@class FitBit
@author - Team Wizards of Coz
'''

PROFILE_API = 'https://api.fitbit.com/1/user/-/profile.json'
ACTIVITIES_API = 'https://api.fitbit.com/1/user/-/activities/calories/date/%s/7d.json'
ACTIVITIES_GOAL_API = 'https://api.fitbit.com/1/user/-/activities/goals/daily.json'
FOOD_GOALS_API = 'https://api.fitbit.com/1/user/-/foods/log/goal.json'
FOOD_API = 'https://api.fitbit.com/1/user/-/foods/log/caloriesIn/date/%s/1d.json'

class FitBit():
    
    pollDuration = 600
    timeToEvent = 100
    client_secret = None 
    client_id = None
    authorization_url = None
    redirect_url = None
    apiObj = None
    access_token = None
    header = None
    
    def __init__(self,client_secret,client_id,authorization_url,redirect_url):
        
        self.client_secret = client_secret
        self.client_id = client_id
        self.authorization_url = authorization_url
        self.redirect_url = redirect_url
        
        self.apiObj = OAuth2Service(client_id=self.client_id,client_secret=self.client_secret,authorize_url=self.authorization_url) 
        authorize_url = self.apiObj.get_authorize_url()
        print('Visit this URL in your browser: {url}'.format(url=authorize_url))
        webbrowser.open(authorize_url)
        
        url_with_code = input('Copy URL from your browser\'s address bar: ')
        self.access_token = re.search('\#access_token=([^&]*)', url_with_code).group(1)
        self.headers = {'Authorization': 'Bearer '+self.access_token}
        
    
    
    def getProfileInfo(self):
        return requests.get(PROFILE_API,headers=headers).json()
    
    
    def getActivities(self,dateStr):
        return requests.get(ACTIVITIES_API % dateStr,headers=self.headers).json()
    
    
    def getFoodLog(self,dateStr):
        return requests.get(FOOD_API % dateStr,headers=self.headers).json()

    
    def getFoodGoals(self):
        return requests.get(FOOD_GOALS_API,headers=self.headers).json()
    
    
    def getActivityGoals(self):
        return requests.get(ACTIVITIES_GOAL_API,headers=self.headers).json()
    


if __name__ == '__main__':
    FitBit()