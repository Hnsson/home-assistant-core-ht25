"""Fixtures for Met weather testing."""

from unittest.mock import AsyncMock, patch

import pytest


@pytest.fixture
def mock_weather():
    """Mock weather data."""
    with (
        patch("metno.MetWeatherData") as mock_data,
        patch(
            "homeassistant.components.met.coordinator.MetWeatherData.evaluate_alert"
        ) as mock_alert,
    ):
        mock_data = mock_data.return_value
        mock_data.fetching_data = AsyncMock(return_value=True)
        mock_data.get_current_weather.return_value = {
            "condition": "cloudy",
            "temperature": 15,
            "pressure": 100,
            "humidity": 50,
            "wind_speed": 10,
            "wind_bearing": 90,
            "dew_point": 12.1,
            "uv_index": 1.1,
        }
        mock_data.get_forecast.return_value = {

        }
        mock_alert.return_value = {"message": "test alert", "severity": "low"}

        yield mock_data

@pytest.fixture
def mock_weather_alert_storm():
    """Mock storm alert."""
    with (
        patch("metno.MetWeatherData") as mock_data):
        mock_data = mock_data.return_value
        mock_data.fetching_data = AsyncMock(return_value=True)
        mock_data.get_current_weather.return_value = {
            "wind_speed": 30
        }
        mock_data.get_forecast.return_value = {}

        yield mock_data

@pytest.fixture
def mock_weather_alert_wind_gust():
    """Mock wind gust alert."""
    with (
        patch("metno.MetWeatherData") as mock_data):
        mock_data = mock_data.return_value
        mock_data.fetching_data = AsyncMock(return_value=True)
        mock_data.get_current_weather.return_value = {
            "wind_gust": 35
        }
        mock_data.get_forecast.return_value = {}

        yield mock_data

@pytest.fixture
def mock_weather_alert_heavy_rain():
    """Mock heavy rain alert."""
    with (
        patch("metno.MetWeatherData") as mock_data):
        mock_data = mock_data.return_value
        mock_data.fetching_data = AsyncMock(return_value=True)
        mock_data.get_current_weather.return_value = {"uv_index": 10}
        mock_data.get_forecast.return_value = [
            {"precipitation": 20}
        ]

        yield mock_data

@pytest.fixture
def mock_weather_alert_rainstorm():
    """Mock rainstorm alert"""
    with (
        patch("metno.MetWeatherData") as mock_data):
        mock_data = mock_data.return_value
        mock_data.fetching_data = AsyncMock(return_value=True)
        mock_data.get_current_weather.return_value = {
            "temperature": 10,
            "wind_speed": 15
            }
        mock_data.get_forecast.return_value = [
            {"precipitation": 25 }
        ]

        yield mock_data


@pytest.fixture
def mock_weather_alert_flood_warning():
    """Mock flood warning alert"""
    with (
        patch("metno.MetWeatherData") as mock_data):
        mock_data = mock_data.return_value
        mock_data.fetching_data = AsyncMock(return_value=True)
        mock_data.get_current_weather.return_value = {
            "humidity": 90
            }
        mock_data.get_forecast.return_value = [
            {"precipitation": 35 }
        ]

        yield mock_data

@pytest.fixture
def mock_weather_alert_heavy_snow():
    """Mock heavy snow alert"""
    with (
        patch("metno.MetWeatherData") as mock_data):
        mock_data = mock_data.return_value
        mock_data.fetching_data = AsyncMock(return_value=True)
        mock_data.get_current_weather.return_value = {
            "temperature": -5
            }
        mock_data.get_forecast.return_value = [
            {"precipitation": 10 }
        ]

        yield mock_data

@pytest.fixture
def mock_weather_alert_uv():
    """Mock uv alert"""
    with (
        patch("metno.MetWeatherData") as mock_data):
        mock_data = mock_data.return_value
        mock_data.fetching_data = AsyncMock(return_value=True)
        mock_data.get_current_weather.return_value = {
            "uv_index": 20
        }
        mock_data.get_forecast.return_value = {}

        yield mock_data

@pytest.fixture
def mock_weather_alert_snow_storm():
    """Mock snow storm alert"""
    with (
        patch("metno.MetWeatherData") as mock_data):
        mock_data = mock_data.return_value
        mock_data.fetching_data = AsyncMock(return_value=True)
        mock_data.get_current_weather.return_value = {
            "temperature": -5,
            "wind_speed": 15
        }
        mock_data.get_forecast.return_value = [
            {"precipitation": 10}
        ]

        yield mock_data