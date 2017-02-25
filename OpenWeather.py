import asyncio
from os import system
import random
import _thread
import sys
from threading import Timer
import os
from datetime import datetime
from dateutil import parser
import pyowm
import pytz
# pip3 install python-dateutil
# pip3 install pyowm

'''
OpenWeather Module
@class OpenWeather
@author - Team Wizards of Coz
'''

class OpenWeather():
    
    pollDuration = 600
    timeToEvent = 100
    api_key = None
    city = None
    owm = None
    
    def __init__(self,api_key,city):
        
        self.api_key = api_key
        self.city = city
        
        self.owm = pyowm.OWM(api_key)
        
        
    def getWeatherNow(self):
        
        obs = self.owm.weather_at_place(self.city)
        w = obs.get_weather()
        return w.get_status()
#         fc =  self.owm.three_hours_forecast(self.city)
#         f = fc.get_forecast()
#         
#         for weather in f:
#             print (weather.get_reference_time('iso'),weather.get_status())
#         
#         utc_dt = str(date.astimezone(pytz.utc))
#         utc_dt = utc_dt[:-3]
#         
#         return fc.get_weather_at(utc_dt).get_status()
    
    
    def pollWeather(self):
        
        Timer(self.pollDuration, self.pollWeather).start()
    
    
    
    
    



if __name__ == '__main__':
    OpenWeather()