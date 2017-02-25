import asyncio
import cozmo
from Common.woc import WOC
from Common.colors import Colors
from os import system
import random
import _thread
import sys
from threading import Timer
import speech_recognition as sr
import os
from datetime import datetime
from dateutil import parser
import pytz
from PIL import Image

from FitBit import FitBit
# pip3 install python-dateutil
# pip3 install pyowm

'''
Fitness Module
@class Fitness
@author - Team Wizards of Coz
'''

CLIENT_ID ='<CLIENT ID FROM FITBIT DEV ACCOUNT>'
CLIENT_SECRET = '<CLIENT SECRET FROM FITBIT DEV ACCOUNT>'
REDIRECT_URL = '<REDIRECT_URL FROM FITBIT DEV ACCOUNT>'
AUTH_URL = "https://www.fitbit.com/oauth2/authorize?response_type=token&client_id="+CLIENT_ID+"&redirect_uri="+REDIRECT_URL+"&scope=activity%20heartrate%20location%20nutrition%20profile%20settings%20sleep%20social%20weight&expires_in=604800"

class Fitness(WOC):
    
    cl = None
    exit_flag = False
    audioThread = None
    cubes = None
    timeRemaining = 100
    curEvent = None
    owm = None
    calendar = None
    idleAnimations = ['anim_sparking_idle_03','anim_sparking_idle_02','anim_sparking_idle_01']
    attractAttentionAnimations = ['anim_keepaway_pounce_02','reacttoblock_triestoreach_01']
    animCtr = 0
    face = None
    faceFound = False
    messageDelivered = False
    fit = None
    calorieGoals = None
    
    
    def __init__(self, *a, **kw):
        
        sys.setrecursionlimit(0x100000)
        
        self.setUpFitBit()
        
        cozmo.setup_basic_logging()
        cozmo.connect(self.startResponding)
        
        
        
    def startResponding(self, coz_conn):
        asyncio.set_event_loop(coz_conn._loop)
        self.coz = coz_conn.wait_for_robot()
        self.playIdle()
         
        self.audioThread = _thread.start_new_thread(self.startAudioThread, ())
        
        while not self.exit_flag:
            asyncio.sleep(0)
        self.coz.abort_all_actions()
    
    
    
    def setUpFitBit(self):
        self.fit = FitBit(CLIENT_SECRET,CLIENT_ID,AUTH_URL,REDIRECT_URL)
    
    
    def checkCalories(self):
       
        self.calorieGoals = self.fit.getFoodGoals()['goals']['calories']
        
        foodLog = self.fit.getFoodLog(datetime.today().date())['foods-log-caloriesIn']
        
        if int(foodLog[0]['value']) > self.calorieGoals:
            self.coz.play_anim('anim_sparking_getin_01').wait_for_completed()
            self.coz.play_anim("anim_driving_upset_loop_02").wait_for_completed()
            self.findFaceAndShout()
        
#         # GOOGLE CALENDAR
#         self.calendar = GoogleCalendar(SCOPES,CLIENT_SECRET_FILE,APPLICATION_NAME,TZ)
#         self.calendar.pollCalendar()
#         event,timeToEvent = self.calendar.todaysEventAndTimeToEvent()
#         
#         if event is not None:
#             start = event['start'].get('dateTime', event['start'].get('date'))
# #             print(start)
#             if timeToEvent < self.timeRemaining:
#                 self.coz.play_anim('anim_sparking_getin_01').wait_for_completed()
#                 self.findFaceAndInform(timeToEvent)
        
    
    
    def findFaceAndShout(self):
        find_face = self.coz.start_behavior(cozmo.behavior.BehaviorTypes.FindFaces)
        try:
            self.face = self.coz.world.wait_for_observed_face(timeout=10)
            print("Found a face!", self.face)
            find_face.stop()
        except asyncio.TimeoutError:
            find_face.stop()
            self.coz.say_text("Look at me!",duration_scalar=1.5,voice_pitch=-1,in_parallel=True).wait_for_completed()
            self.coz.play_anim(random.choice(self.attractAttentionAnimations)).wait_for_completed()
            self.findFaceAndShout()
        
        if self.faceFound == False:
            self.faceFound = True
            if self.face is not None:
                find_face.stop()
                self.coz.play_anim("anim_memorymatch_failgame_cozmo_02").wait_for_completed()
                self.coz.abort_all_actions()
                self.coz.set_head_angle(cozmo.util.Angle(degrees=40))
                count = 0
                while True:
                    img = Image.open("Images/fat_"+ str(count % 4) + ".png")
                    resized_img = img.resize(cozmo.oled_face.dimensions(), Image.BICUBIC)
                    screen_data = cozmo.oled_face.convert_image_to_screen_data(resized_img) 
                    self.coz.display_oled_face_image(screen_data, in_parallel=True, duration_ms=250).wait_for_completed()
                    count += 1               
                    if count==25:
                        break
                self.coz.say_text("Enough eating today!! You will become fat!!",duration_scalar=1.5,voice_pitch=-1,in_parallel=True).wait_for_completed()
                self.coz.play_anim("anim_reacttoblock_frustrated_int2_01").wait_for_completed()
                self.messageDelivered = True
                
                
     
    
    def startAudioThread(self):
        try:
            print("Take input");
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.startListening())
        except Exception as e:
            print(e)
    
    
    
    async def startListening(self):
        if self.faceFound:
            print("Taking input");
            
            r = sr.Recognizer()
            r.energy_threshold = 5000
            print(r.energy_threshold)
            with sr.Microphone(chunk_size=512) as source:
                audio = r.listen(source)
    
            try:
                speechOutput = r.recognize_google(audio)
                if self.messageDelivered == True:
                    self.processSpeech(speechOutput)
                await asyncio.sleep(1);
                await self.startListening()
    
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
                await asyncio.sleep(0);
                await self.startListening()
    
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
                           
     
    def processSpeech(self,speechOutput):
        print(speechOutput)
        if 'thanks' in speechOutput or 'thank' in speechOutput:
            self.coz.play_anim("anim_greeting_happy_01").wait_for_completed()
            self.messageDelivered = False
               
    
    def playIdle(self):
        self.coz.play_anim(self.idleAnimations[self.animCtr]).wait_for_completed()
        self.animCtr += 1
        
        if self.animCtr==3:
            self.checkCalories()
        else: 
            self.playIdle()

if __name__ == '__main__':
    Fitness()