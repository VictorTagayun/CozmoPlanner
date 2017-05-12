# Cozmo Planner
## Project Description
Various Third party apis have been integrated with Cozmo here to allow him to be aware of your day to day activities.
1. Google Calendar - Cozmo checks for events on your calendar and reminds you an hour before
2. Open Weather - Cozmo checks for weather changes and when you tell cozmo that you are going out, he checks the weather and gives you a suggestion (for example, if it's raining, he will remind you to take an umbrella)
3. Fitbit API - Cozmo keeps track of your calorie limit for the day, and if it exceeds it, he will get annoyed at you

## Video
https://www.youtube.com/watch?v=HJXg_scHQ64

## Implementation Details
Each experience starts with Cozmo being in an idle mode polling for updates from the 3rd party API. Once Cozmo gets the update, Cozmo looks for your face and tries to get your attention. Then Cozmo relays the update through speech and images on his face

## Instructions
### Dependencies
1. Common - ( Download it from https://github.com/Wizards-of-Coz/Common )
2. SpeechRecognition (pip3 install SpeechRecognition)
3. python-dateutil (pip3 install python-dateutil)
4. pyowm (pip3 install pyowm)
5. pytz (pip3 install pytz)
6. pillow (pip3 install pillow)

### Google Calendar Integration 
Set up a Google App as mentioned in Step 1 here. Replace the json file path in CLIENT_SECRET_FILE and app Name from google Apps to APPLICATION_NAME in Planner.py.

### Open Weather Integration 
Create an account in https://home.openweathermap.org/. Go to API Keys and generate a key for your app. Replace this in CheckWeather.py in PYOWM_API_KEY.

### FitBit Integration 
This uses OAuth2 to open the browser and login to Fitbit. Cozmo then gets access to the Fitbit APIs. If the player goes above his/her daily quota, cozmo gets angry and throws a fit.


## Thoughts for the Future
This prototype opens possibilities of integrating Cozmo to a variety of other 3rd party APIs to make him connected and integrated with the player’s lifestyle.
