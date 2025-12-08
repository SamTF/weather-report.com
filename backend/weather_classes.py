from typing import List


class WeatherCurrent:
    """
    Represents the main current weather data structure.
    """
    def __init__(self,
                 condition: dict,
                 feelslike_c: float,
                 humidity: int,
                 is_day: int,
                 last_updated: str,
                 precip_mm: float,
                 temp_c: float):

        self.condition = Condition(
            code=condition['code'],
            icon=condition['icon'],
            text=condition['text']
        )
        self.temp = self.get_temp(temp_c, feelslike_c)
        self.humidity = humidity
        self.is_day = is_day
        self.last_updated = last_updated
        self.precip_mm = precip_mm

    def get_temp(self, temp_c: float, feelslike_c: float) -> str:
        '''Gets temperature forecast from weatherapi, rounds it to full digit and adds degree symbol'''
        try:    temp = round(temp_c)
        except: temp = round(feelslike_c)

        return f'{temp}º'

    @classmethod
    def from_dict(cls, data: dict):
        """Creates an instance directly from a dictionary."""
        return cls(**data)
    
    def to_dict(self) -> dict:
        """Converts the WeatherReport object into a dictionary"""
        return {
            "condition": self.condition.to_dict(),
            "humidity": self.humidity,
            "is_day": self.is_day,
            "last_updated": self.last_updated,
            "precip_mm": self.precip_mm,
            "temp": self.temp
        }

    def __repr__(self):
        return (f"WeatherReport(temp_c={self.temp_c}°C, "
                f"condition={self.condition}, "
                f"last_updated='{self.last_updated}')")

class Condition:
    '''Represents the detailed weather condition, e.g., 'Overcast'.'''
    def __init__(self, code: int, icon: str, text: str):
        self.code = self.get_code_from_icon_url(icon)
        self.icon = icon
        self.text = text
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    def to_dict(self) -> dict:
        '''Converts the Condition object into a dictionary.'''
        return {
            "code": self.code,
            "icon": self.icon,
            "text": self.text
        }
    
    def get_code_from_icon_url(self, icon) -> str:
        '''Gets the URL to the icon from weatherapi.com and extracts only the 3 digit icon code'''
        return str(icon[-7:-4])

    def __repr__(self):
        return f"Condition(code={self.code}, text='{self.text}')"

class Location:
    '''Represents the geographic and time information for a specific location.'''
    def __init__(self, country: str, lat: float, localtime: str, 
                 localtime_epoch: int, lon: float, name: str, 
                 region: str, tz_id: str):
        
        self.country = country
        self.localtime = localtime
        self.localtime_epoch = localtime_epoch
        self.name = name
        self.region = region
        self.tz_id = tz_id
        self._split_date_and_time()

    def _split_date_and_time(self) -> None:
        date, time = self.localtime.split(" ")
        self.date = date
        self.time = time

    @classmethod
    def from_dict(cls, data: dict):
        '''Creates a Location instance directly from a dictionary.'''
        return cls(**data)

    def to_dict(self) -> dict:
        '''Converts the Location object back into a dictionary.'''
        return {
            "country": self.country,
            "name": self.name,
            "region": self.region,
            "tz_id": self.tz_id,
            "local_time": self.time,
            "local_date": self.date
        }
    
    def __repr__(self):
        return f"Location(name='{self.name}', country='{self.country}', lat={self.lat}, lon={self.lon})"

class HourlyForecast:
    '''Represents the weather forecast for a single hour.'''
    def __init__(self,
                 condition: dict,
                 feelslike_c: float,
                 heatindex_c: float,
                 is_day: int,
                 snow_cm: float,
                 temp_c: float,
                 time: str,
                 will_it_rain: int,
                 will_it_snow: int,
                 windchill_c: float):

        # Instantiate the Condition object from the nested dictionary
        if isinstance(condition, Condition):
            self.condition = condition
        else:
            self.condition = Condition(
                code=condition['code'],
                icon=condition['icon'],
                text=condition['text']
            )

        self.feelslike_c = feelslike_c
        self.heatindex_c = heatindex_c
        self.is_day = is_day
        self.snow_cm = snow_cm
        self.temp_c = temp_c
        self.time = time
        self.will_it_rain = will_it_rain
        self.will_it_snow = will_it_snow
        self.windchill_c = windchill_c
    
    @property
    def temp(self) -> str:
        return f'{round(self.temp_c)}º'

    @classmethod
    def from_dict(cls, data: dict):
        '''Creates an instance directly from a dictionary.'''
        return cls(**data)

    def to_dict(self) -> dict:
        return {
            "condition": self.condition.to_dict(),
            "feelslike_c": self.feelslike_c,
            "heatindex_c": self.heatindex_c,
            "is_day": self.is_day,
            "snow_cm": self.snow_cm,
            "temp_c": self.temp_c,
            "time": self.time,
            "will_it_rain": self.will_it_rain,
            "will_it_snow": self.will_it_snow,
            "windchill_c": self.windchill_c
        }

    def __repr__(self):
        return (f"HourlyForecast(time='{self.time}', "
                f"temp_c={self.temp_c}°C, "
                f"condition='{self.condition.text}')")

class Astro:
    """Represents astronomical data for the day (sun/moon times)."""
    def __init__(self, is_moon_up: int, is_sun_up: int, moon_illumination: int, 
                 moon_phase: str, moonrise: str, moonset: str, 
                 sunrise: str, sunset: str):
        self.is_moon_up = is_moon_up
        self.is_sun_up = is_sun_up
        self.moon_illumination = moon_illumination
        self.moon_phase = moon_phase
        self.moonrise = moonrise
        self.moonset = moonset
        self.sunrise = sunrise
        self.sunset = sunset

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    def to_dict(self) -> dict:
        return self.__dict__

class DaySummary:
    """Represents the overall weather summary for the entire day."""
    def __init__(self, avgtemp_c: float, condition: dict, daily_will_it_rain: int,
                 daily_will_it_snow: int, maxtemp_c: float, mintemp_c: float, 
                 totalsnow_cm: float):
        
        if isinstance(condition, Condition):
            self.condition = condition
        else:
            self.condition = Condition.from_dict(condition)

        self.avgtemp_c = avgtemp_c
        self.daily_will_it_rain = daily_will_it_rain
        self.daily_will_it_snow = daily_will_it_snow
        self.maxtemp_c = maxtemp_c
        self.mintemp_c = mintemp_c
        self.totalsnow_cm = totalsnow_cm

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    def to_dict(self) -> dict:
        return {
            "avgtemp_c": self.avgtemp_c,
            "condition": self.condition.to_dict(),
            "daily_will_it_rain": self.daily_will_it_rain,
            "daily_will_it_snow": self.daily_will_it_snow,
            "maxtemp_c": self.maxtemp_c,
            "mintemp_c": self.mintemp_c,
            "totalsnow_cm": self.totalsnow_cm
        }
    
class ForecastDay:
    '''Represents the complete weather forecast data for a single calendar day.'''
    def __init__(self, astro: dict, date: str, day: dict, hour: list):
        
        # Nested Objects
        self.astro = Astro.from_dict(astro)
        self.day_summary = DaySummary.from_dict(day)
        
        # List of nested HourlyForecast objects
        self.hourly_forecasts = []
        for hourly_dict in hour:
            self.hourly_forecasts.append(HourlyForecast.from_dict(hourly_dict))
        
        self.date = date

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            astro=data['astro'],
            date=data['date'],
            day=data['day'],
            hour=data['hour']
        )

    def to_dict(self) -> dict:
        return {
            "astro": self.astro.to_dict(),
            "date": self.date,
            "day": self.day_summary.to_dict(),
            "hour": [h.to_dict() for h in self.hourly_forecasts]
        }
    
    def __repr__(self):
        return (f"ForecastDay(date='{self.date}', "
                f"MaxTemp={self.day_summary.maxtemp_c}°C, "
                f"HourlyCount={len(self.hourly_forecasts)})")

class WeatherReport:
    def __init__(self, current_weather: WeatherCurrent, location: Location, forecasts: List[ForecastDay]):
        self.current = current_weather
        self.location = location
        self.forecasts = forecasts

    def to_dict(self) -> dict:
        return {
            "current": self.current.to_dict(),
            "location": self.location.to_dict(),
            "forecast": [f.to_dict() for f in self.forecasts]
        }