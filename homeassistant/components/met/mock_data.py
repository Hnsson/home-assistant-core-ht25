from typing import Any
# Only these keys will be overridden when USE_MOCK is True

# Current weather mock values
MOCK_VALUES: dict[str, Any] = {
    "temperature": 999,  # °C
    "templow": 0,  # optional if needed
    "pressure": 999,  # hPa
    "humidity": 999,  # %
    "wind_speed": 999,  # km/h
    "wind_bearing": 999,  # degrees
    "wind_gust": 999,  # km/h
    "dew_point": 999,  # °C
    "uv_index": 999,  # UV index
    "condition": "mocked_weather",  # e.g., sunny, cloudy
    "precipitation": 999,  # mm
    "precipitation_probability": 999,  # %
}

# Daily forecast mock values
MOCK_FORECAST_DAILY: dict[str, Any] = {
    "temperature": 777,
    "templow": 0,  # optional if needed
    "pressure": 777,
    "humidity": 777,
    "wind_speed": 777,
    "wind_bearing": 777,
    "wind_gust": 777,
    "dew_point": 777,
    "uv_index": 777,
    "condition": "mocked_daily",
    "precipitation": 777,
    "precipitation_probability": 777,
}

# Hourly forecast mock values
MOCK_FORECAST_HOURLY: dict[str, Any] = {
    "temperature": 888,
    "templow": 0,  # optional
    "pressure": 888,
    "humidity": 888,
    "wind_speed": 888,
    "wind_bearing": 888,
    "wind_gust": 888,
    "dew_point": 888,
    "uv_index": 888,
    "condition": "mocked_hourly",
    "precipitation": 888,
    "precipitation_probability": 888,
}
