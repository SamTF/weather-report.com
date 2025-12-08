from typing import List
from pydantic import BaseModel, Field, field_validator, computed_field, ConfigDict


class Condition(BaseModel):
    """Represents the detailed weather condition, e.g., 'Overcast'."""
    code: int | str
    icon: str
    text: str

    def model_post_init(self, __context) -> None:
        """Extract code from icon after all fields are set"""
        object.__setattr__(self, 'code', str(self.icon[-7:-4]))

    @classmethod
    def from_dict(cls, data: dict):
        """Creates an instance directly from a dictionary."""
        return cls(**data)

    def __repr__(self) -> str:
        return f"Condition(code={self.code}, text='{self.text}')"


class WeatherCurrent(BaseModel):
    """Represents the main current weather data structure."""
    condition: Condition
    feelslike_c: float
    humidity: int
    is_day: int
    last_updated: str
    precip_mm: float
    temp_c: float

    @computed_field
    @property
    def temp(self) -> str:
        """Gets temperature forecast from weatherapi, rounds it to full digit and adds degree symbol"""
        temp_value = round(self.temp_c)
        return f'{temp_value}º'

    @classmethod
    def from_dict(cls, data: dict):
        """Creates an instance directly from a dictionary."""
        return cls(**data)

    def __repr__(self) -> str:
        return (f"WeatherReport(temp_c={self.temp_c}°C, "
                f"condition={self.condition}, "
                f"last_updated='{self.last_updated}')")


class Location(BaseModel):
    """Represents the geographic and time information for a specific location."""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    country: str
    lat: float
    localtime: str
    localtime_epoch: int
    lon: float
    name: str
    region: str
    tz_id: str
    date: str = ""
    time: str = ""

    def model_post_init(self, __context) -> None:
        """Split date and time after initialization"""
        date, time = self.localtime.split(" ")
        object.__setattr__(self, 'date', date)
        object.__setattr__(self, 'time', time)

    @classmethod
    def from_dict(cls, data: dict):
        """Creates a Location instance directly from a dictionary."""
        return cls(**data)

    def __repr__(self) -> str:
        return f"Location(name='{self.name}', country='{self.country}', lat={self.lat}, lon={self.lon})"


class HourlyForecast(BaseModel):
    """Represents the weather forecast for a single hour."""
    condition: Condition
    feelslike_c: float
    heatindex_c: float
    is_day: int
    snow_cm: float
    temp_c: float
    time: str
    will_it_rain: int
    will_it_snow: int
    windchill_c: float

    @computed_field
    @property
    def temp(self) -> str:
        """Returns formatted temperature string"""
        return f'{round(self.temp_c)}º'

    @classmethod
    def from_dict(cls, data: dict):
        """Creates an instance directly from a dictionary."""
        return cls(**data)

    def __repr__(self) -> str:
        return (f"HourlyForecast(time='{self.time}', "
                f"temp_c={self.temp_c}°C, "
                f"condition='{self.condition.text}')")


class Astro(BaseModel):
    """Represents astronomical data for the day (sun/moon times)."""
    is_moon_up: int
    is_sun_up: int
    moon_illumination: int
    moon_phase: str
    moonrise: str
    moonset: str
    sunrise: str
    sunset: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


class DaySummary(BaseModel):
    """Represents the overall weather summary for the entire day."""
    avgtemp_c: float
    condition: Condition
    daily_will_it_rain: int
    daily_will_it_snow: int
    maxtemp_c: float
    mintemp_c: float
    totalsnow_cm: float

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

class ForecastDay(BaseModel):
    """Represents the complete weather forecast data for a single calendar day."""
    astro: Astro
    date: str
    day: DaySummary
    hour: List[HourlyForecast]

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            astro=data['astro'],
            date=data['date'],
            day=data['day'],
            hour=data['hour']
        )

    def __repr__(self) -> str:
        return (f"ForecastDay(date='{self.date}', "
                f"MaxTemp={self.day.maxtemp_c}°C, "
                f"HourlyCount={len(self.hour)})")


class WeatherReport(BaseModel):
    """Main weather report containing current weather, location, and forecasts."""
    current: WeatherCurrent
    location: Location
    forecast: List[ForecastDay]

    def to_dict(self) -> dict:
        return {
            "current": self.current.to_dict(),
            "location": self.location.to_dict(),
            "forecast": [f.to_dict() for f in self.forecast]
        }