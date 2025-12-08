###### DESCRIPTION #################################################
### Handles the Weather API requests and calls to the pill script. Called from David Lynch to simplify the Discord Bot.


###### IMPORTS #################################################
from typing import Dict, List, Tuple
import requests
from datetime import datetime
from wttr import pill   # My script to create pretty weather cards c:
from dotenv import load_dotenv
import os
from weather_classes import *

###### CONSTANTS #################################################
load_dotenv()

API_KEY = os.getenv("WEATHERAPI_KEY")
WEATHERAPI  = 'http://api.weatherapi.com/v1/forecast.json?key={}&q={}&days=3'
HOURS = [9, 12, 15, 18, 21, 23]

###### HELPERS #################################################
def get_code_from_json(forecast) -> str:
    '''Gets the URL to the icon from weatherapi.com and extracts only the 3 digit icon code'''
    code = forecast['condition']['icon'][-7:-4]
    return code

def get_temp(forecast) -> str:
    '''Gets temperature forecast from weatherapi, rounds it to full digit and adds degree symbol'''
    try:    temp = round(forecast['temp_c'])
    except: temp = round(forecast['feelslike_c'])

    return f'{temp}º'

def get_local_time(local_time:str) -> datetime:
    '''Get the local time in datetime format'''
    try:
        local_datetime = datetime.strptime(local_time, '%H:%M').time()
    except:                                                                                                 # in case the localtime is something ' 1:55' with the whitespace, otherwise we get errors
        local_datetime = datetime.strptime(local_time[1:], '%H:%M').time()
    
    return local_datetime

def get_daily_progress(local_datetime:datetime) -> int:
    '''Translates minutes elapsed into corresponding X-Position in the daily timeline'''
    minutes_elapsed = local_datetime.minute + (local_datetime.hour * 60)                                    # gets the total amount of minutes elapsed this day thus far
    w = 133/3                                                                                               # each hour block is 1/3 of the square, and the square is 133px wide
    m = w/60                                                                                                # converts the hour block into minute blocks
    progress = int((m * minutes_elapsed) - 232.5)                                                           # anything before 232.5 minutes does not show up, so shift everything to the left

    return progress

def get_hourly_forecast(forecast_dict:dict) -> Tuple[List[str]]:
    '''Get forecasted temperature and condition at specified hours'''
    temps = [get_temp(forecast_dict[x]) for x in HOURS]                                                     # getting the temperature forecast at each hour specified, rounded to full digit
    codes = [get_code_from_json(forecast_dict[x]) for x in HOURS]                                           # getting the forecast condition code
    codes[-1] = '999'                                                                                       # hardcoding the code at 12AM to be the Moon

    return temps, codes

def get_formatted_date(date_str:str) -> str:
    '''Take a YYYY-MM-DD date string and format it as MONTH day (AUGUST 21)'''
    date = datetime.strptime(date_str, '%Y-%m-%d')                                                          # converting the date to datetime so that we can format it differently
    date_formatted = date.strftime('%B %d').upper()                                                         # formatting the date as AUGUST 21 (month_name day)

    return date_formatted

###

###### WEATHER API #################################################
def fetch_api_data(city:str) -> Dict:
    response = requests.get(WEATHERAPI.format(API_KEY, city))

    if not response.ok:
        raise ValueError(f'400 - City {city} was not found')
    
    return response.json()

def get_weather_report_data(city: str) -> WeatherReport:
    """Fetch weather data and return a Pydantic WeatherReport model"""
    data = fetch_api_data(city)
    current_weather = WeatherCurrent.from_dict(data['current'])
    loc = Location.from_dict(data['location'])
    
    forecasts = [ForecastDay.from_dict(fd) for fd in data['forecast']['forecastday']]

    return WeatherReport(current=current_weather, location=loc, forecast=forecasts)


###### WEATHER FUNCTIONS #################################################

### 2.0 version with hourly forecasts
def weather_report(city:str):
    wr = get_weather_report_data(city)
    local_datetime = get_local_time(wr.location.time)
    
    # Checking if it's nighttime
    if not wr.current.is_day:
        current_code = '999'
    
    forecasts: List[HourlyForecast] = wr.forecast[0].hour

    hourly_temps = [forecasts[i].temp for i in HOURS]
    hourly_codes = [str(forecasts[i].condition.code) for i in HOURS]
    hourly_codes[-1] = '999'
    progress = get_daily_progress(local_datetime)

    # FINALLY creates the image and saves it to memory!
    weather_card = pill.create_weather_card_hourly(city.upper(), wr.current.temp, current_code, wr.location.time, hourly_temps, hourly_codes, progress)
    return weather_card


###############################
def tomorrow(city:str, transparent:bool):
    wr = get_weather_report_data(city)
    tomorrow_forecast = wr.forecast[1]

    avg_temp = round(tomorrow_forecast.day.avgtemp_c)
    avg_temp = f'{avg_temp}º'
    condition_code = tomorrow_forecast.day.condition.code
    
    date = tomorrow_forecast.date
    date_formatted = get_formatted_date(date)

    hourly_temps = [(tomorrow_forecast.hour[x]).temp for x in HOURS]
    hourly_codes = [tomorrow_forecast.hour[x].condition.code for x in HOURS]

    weather_card = pill.create_tomorrow_forecast(city.upper(), avg_temp, condition_code, date_formatted, hourly_temps, hourly_codes, transparent)
    return weather_card


if __name__ == '__main__':
    pass
else:
    print('[WEATHER_REPORT IMPORTED]')