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

from OpenWeather import OpenWeather

'''
CheckWeather Module
@class CheckWeather
@author - Team Wizards of Coz
'''

PYOWM_API_KEY = '<OPEN WEATHER API KEY>'

class CheckWeather(WOC):
    
    cl = None
    exit_flag = False
    audioThread = None
    curEvent = None
    owm = None
    calendar = None
    idleAnimations = ['anim_sparking_idle_03','anim_sparking_idle_02','anim_sparking_idle_01']
    attractAttentionAnimations = ['anim_keepaway_pounce_02','reacttoblock_triestoreach_01']
    animCtr = 0
    face = None
    faceFound = False
    messageDelivered = False
    lookingForFace = False
    weatherObj = None
    city = 'Pittsburgh'
    
    
    def __init__(self, *a, **kw):
        
        sys.setrecursionlimit(0x100000)
        
        self.weatherObj = OpenWeather(PYOWM_API_KEY,self.city)
        
        cozmo.setup_basic_logging()
        cozmo.connect(self.startResponding)
        
        
        
    def startResponding(self, coz_conn):
        asyncio.set_event_loop(coz_conn._loop)
        self.coz = coz_conn.wait_for_robot()
        
        self.audioThread = _thread.start_new_thread(self.startAudioThread, ())
        
        self.playIdle()
        
        while not self.exit_flag:
            asyncio.sleep(0)
        self.coz.abort_all_actions()
    
    
    
    
    def startAudioThread(self):
        try:
            print("Take input");
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.startListening())
        except Exception as e:
            print(e)
    
    
    
    
    async def startListening(self):
        
        print("Taking input");
        
        r = sr.Recognizer()
        r.energy_threshold = 5000
        print(r.energy_threshold)
        with sr.Microphone(chunk_size=512) as source:
            audio = r.listen(source)
    
        try:
            speechOutput = r.recognize_google(audio)
            self.processSpeech(speechOutput);
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
        if self.face is None:
            if 'cozmo' in speechOutput or 'Cozmo' in speechOutput or 'Cosmo' in speechOutput or 'buddy' in speechOutput or 'body' in speechOutput or 'osmo' in speechOutput or 'Kosmos' in speechOutput or 'Kosmo' in speechOutput:
                self.lookingForFace = True
                self.lookForFace()
        else:
            if 'going' in speechOutput or 'out' in speechOutput:
                print(self.weatherObj.getWeatherNow())
                
                count = 0
                self.coz.play_anim('anim_sparking_getin_01').wait_for_completed()
                self.coz.set_head_angle(cozmo.util.Angle(degrees=40))
                
                #show weather animation
                while True:
                    img = Image.open("Images/rain_"+ str(count % 4) + ".png")
                    resized_img = img.resize(cozmo.oled_face.dimensions(), Image.BICUBIC)
                    screen_data = cozmo.oled_face.convert_image_to_screen_data(resized_img) 
                    self.coz.display_oled_face_image(screen_data, in_parallel=True, duration_ms=1).wait_for_completed()
                    count += 1               
                    if count==25:
                        break
                self.coz.say_text("looks like it might rain today! Take an umbrella with you!",duration_scalar=1,voice_pitch=-1,in_parallel=True).wait_for_completed()
                
            elif 'thanks' in speechOutput or 'thank' in speechOutput:
                self.coz.play_anim("anim_greeting_happy_01").wait_for_completed()

        
        
        
    def lookForFace(self):
        find_face = self.coz.start_behavior(cozmo.behavior.BehaviorTypes.FindFaces)
        try:
            self.face = self.coz.world.wait_for_observed_face(timeout=20)
            print("Found a face!", self.face)
        except asyncio.TimeoutError:
            find_face.stop()
            self.coz.say_text("Look at me").wait_for_completed()
        finally:
            find_face.stop()
            if self.face is not None:
                self.coz.play_anim("anim_greeting_happy_01").wait_for_completed()
                self.lookingForFace = False
                self.coz.set_head_angle(cozmo.util.Angle(degrees=40))
                
                
    
               
    
    def playIdle(self):
        if self.lookingForFace == False:
            self.coz.play_anim(self.idleAnimations[self.animCtr]).wait_for_completed()
            self.playIdle()
            
            

if __name__ == '__main__':
    CheckWeather()