"""DataUpdateCoordinator for Met.no integration."""

from __future__ import annotations

from collections.abc import Callable, Mapping
import datetime
from datetime import timedelta
import logging
from random import randrange
from typing import Any, Self

from homeassistant.helpers.template import combine
import metno

from .mock_data import MOCK_VALUES, MOCK_FORECAST_DAILY, MOCK_FORECAST_HOURLY

from homeassistant.components.weather.const import (
    ATTR_WEATHER_ALERT,
    ATTR_WEATHER_ALERT_SEVERITY,
    ATTR_WEATHER_SUNRISE,
    ATTR_WEATHER_SUNSET,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_ELEVATION,
    CONF_LATITUDE,
    CONF_LONGITUDE,
    EVENT_CORE_CONFIG_UPDATE,
)
from homeassistant.core import Event, HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util

from .const import ALERT_RULES, CONF_TRACK_HOME, DOMAIN, SEVERITY_ORDER

# Dedicated Home Assistant endpoint - do not change!
URL = "https://aa015h6buqvih86i1.api.met.no/weatherapi/locationforecast/2.0/complete"
SUNRISE_URL = "https://aa015h6buqvih86i1.api.met.no/weatherapi/sunrise/3.0/sun"

_LOGGER = logging.getLogger(__name__)

# --------------------------------------------------------------------
# MOCK SETTINGS
# Toggle mock data injection (True = use mock values)
USE_MOCK = True
USE_MOCK_FORECAST = True

type MetWeatherConfigEntry = ConfigEntry["MetDataUpdateCoordinator"]


class CannotConnect(HomeAssistantError):
    """Unable to connect to the web site."""


class MetWeatherData:
    """Keep data for Met.no weather entities."""

    def __init__(self, hass: HomeAssistant, config: Mapping[str, Any]) -> None:
        """Initialise the weather entity data."""
        self.hass = hass
        self._config = config
        self._weather_data: metno.MetWeatherData
        self.current_weather_data: dict = {}
        self.alert: dict[str, str] = {}
        self.daily_forecast: list[dict] = []
        self.hourly_forecast: list[dict] = []
        self.sun_data: dict = {}
        self._coordinates: dict[str, str] | None = None

    def set_coordinates(self) -> bool:
        """Weather data initialization - set the coordinates."""
        if self._config.get(CONF_TRACK_HOME, False):
            latitude = self.hass.config.latitude
            longitude = self.hass.config.longitude
            elevation = self.hass.config.elevation
        else:
            latitude = self._config[CONF_LATITUDE]
            longitude = self._config[CONF_LONGITUDE]
            elevation = self._config[CONF_ELEVATION]

        coordinates = {
            "lat": str(latitude),
            "lon": str(longitude),
            "msl": str(elevation),
        }
        if coordinates == self._coordinates:
            return False
        self._coordinates = coordinates

        self._weather_data = metno.MetWeatherData(
            coordinates, async_get_clientsession(self.hass), api_url=URL
        )
        return True

    def evaluate_alert(
        self, weather_data: dict, daily_forecast: list[dict]
    ) -> dict[str, str]:
        """From all available current weather metrics, create alert messages."""
        precipitation = [
            day.get("precipitation", 0)
            for day in daily_forecast
            if isinstance(day.get("precipitation"), (int, float))
        ]
        avg_precipitation = (
            sum(precipitation) / len(precipitation) if precipitation else 0
        )

        combined_data = {**weather_data, "precipitation": avg_precipitation}

        matched_rules = [
            rule
            for rule in ALERT_RULES
            if all(
                metric in combined_data and condition(combined_data[metric])
                for metric, condition in rule["conditions"].items()
            )
        ]

        if not matched_rules:
            return {"message": "No alerts", "severity": "None"}

        most_relevant = max(
            matched_rules,
            key=lambda r: (SEVERITY_ORDER.get(r["severity"], 0), len(r["conditions"])),
        )
        return {
            "message": most_relevant["message"],
            "severity": most_relevant["severity"],
        }

    async def fetch_data(self) -> Self:
        """Fetch data from API - (current weather and forecast)."""
        resp = await self._weather_data.fetching_data()
        if not resp:
            raise CannotConnect

        # Get real data
        self.current_weather_data = self._weather_data.get_current_weather()
        time_zone = dt_util.get_default_time_zone()
        self.daily_forecast = self._weather_data.get_forecast(time_zone, False, 0)
        self.hourly_forecast = self._weather_data.get_forecast(time_zone, True)

        # Inject mock data (override or add missing keys)
        if USE_MOCK:
            _LOGGER.warning("Using mock weather data override: %s", MOCK_VALUES)
            for key, mock_val in MOCK_VALUES.items():
                self.current_weather_data[key] = (
                    mock_val  # Add missing keys with mock values
                )

        # Inject mock daily forecast
        if USE_MOCK_FORECAST:
            _LOGGER.warning(
                "Using mock daily forecast override: %s", MOCK_FORECAST_DAILY
            )
            for day in self.daily_forecast:
                for key, mock_val in MOCK_FORECAST_DAILY.items():
                    day[key] = mock_val  # Add missing keys with mock values

        # Inject mock hourly forecast
        if USE_MOCK_FORECAST:
            _LOGGER.warning(
                "Using mock hourly forecast override: %s", MOCK_FORECAST_HOURLY
            )
            for hour in self.hourly_forecast:
                for key, mock_val in MOCK_FORECAST_HOURLY.items():
                    hour[key] = mock_val  # Add missing keys with mock values
        # Continue with normal alert logic
        alert_result = self.evaluate_alert(
            self.current_weather_data, self.daily_forecast
        )
        self.alert = {
            ATTR_WEATHER_ALERT: alert_result["message"],
            ATTR_WEATHER_ALERT_SEVERITY: alert_result["severity"],
        }
        self.sun_data = await self.fetch_sun_data(time_zone)
        return self

    async def fetch_sun_data(
        self, time_zone: datetime.tzinfo
    ) -> dict[str, datetime.time]:
        """Fetch sunrise and sunset data from Met.no API."""
        if not self._coordinates:
            return {}
        try:
            session = async_get_clientsession(self.hass)
            now = dt_util.now(time_zone)
            date_str = now.strftime("%Y-%m-%d")
            utc_offset = now.strftime("%z")
            if utc_offset:
                offset = f"{utc_offset[:3]}:{utc_offset[3:]}"
            else:
                offset = "+00:00"
            params = {
                "lat": self._coordinates["lat"],
                "lon": self._coordinates["lon"],
                "date": date_str,
                "offset": offset,
            }
            async with session.get(SUNRISE_URL, params=params) as response:
                if response.status != 200:
                    _LOGGER.warning(
                        "Error fetching sunrise data: HTTP %s", response.status
                    )
                    return {}

                data = await response.json()
                return self._parse_sun_data(data)

        except Exception as err:
            _LOGGER.error("Error fetching sunrise data: %s", err)
            return {}

    def _parse_sun_data(self, data: dict) -> dict[str, datetime.time]:
        """Parse sunrise and sunset from API response."""
        sun_data = {}
        props = data.get("properties", {})

        for key in [ATTR_WEATHER_SUNRISE, ATTR_WEATHER_SUNSET]:
            if props.get(key):
                time_str = props[key].get("time")
                if time_str:
                    dt = dt_util.parse_datetime(time_str)
                    if dt:
                        sun_data[key] = dt.time()
        return sun_data


class MetDataUpdateCoordinator(DataUpdateCoordinator[MetWeatherData]):
    """Class to manage fetching Met data."""

    config_entry: MetWeatherConfigEntry

    def __init__(
        self, hass: HomeAssistant, config_entry: MetWeatherConfigEntry
    ) -> None:
        """Initialize global Met data updater."""
        self._unsub_track_home: Callable[[], None] | None = None
        self.weather = MetWeatherData(hass, config_entry.data)
        self.weather.set_coordinates()

        update_interval = timedelta(minutes=randrange(55, 65))

        super().__init__(
            hass,
            _LOGGER,
            config_entry=config_entry,
            name=DOMAIN,
            update_interval=update_interval,
        )

    async def _async_update_data(self) -> MetWeatherData:
        """Fetch data from Met."""
        try:
            return await self.weather.fetch_data()
        except Exception as err:
            raise UpdateFailed(f"Update failed: {err}") from err

    def track_home(self) -> None:
        """Start tracking changes to HA home setting."""
        if self._unsub_track_home:
            return

        async def _async_update_weather_data(_event: Event | None = None) -> None:
            """Update weather data."""
            if self.weather.set_coordinates():
                await self.async_refresh()

        self._unsub_track_home = self.hass.bus.async_listen(
            EVENT_CORE_CONFIG_UPDATE, _async_update_weather_data
        )

    def untrack_home(self) -> None:
        """Stop tracking changes to HA home setting."""
        if self._unsub_track_home:
            self._unsub_track_home()
            self._unsub_track_home = None
