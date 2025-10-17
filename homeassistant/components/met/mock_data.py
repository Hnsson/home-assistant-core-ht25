"""Mock data for Met.no integration."""

from typing import Any

# Current weather mock values to trigger ALERT_RULES
MOCK_VALUES: dict[str, Any] = {
    # "temperature": -1,  # Triggers heavy_snow and snowstorm_warning
    # "templow": -5,  # Optional, used for additional testing
    # "pressure": 1000,  # Default value
    # "humidity": 90,  # Triggers flood_warning
    # "wind_speed": 25,  # Triggers storm_warning and snowstorm_warning
    # "wind_bearing": 180,  # Default value
    # "wind_gust": 35,  # Triggers wind_gust_warning
    # "dew_point": -2,  # Default value
    # "uv_index": 8,  # Triggers uv_alert
    # "condition": "mocked_weather",  # Default value
    # "precipitation": 35,  # Triggers flood_warning and rainstorm
    # "precipitation_probability": 100,  # Default value
}

# Daily forecast mock values to trigger ALERT_RULES
MOCK_FORECAST_DAILY: dict[str, Any] = {
    # "temperature": -1,  # Triggers heavy_snow and snowstorm_warning
    # "templow": -5,  # Optional, used for additional testing
    # "pressure": 1000,  # Default value
    # "humidity": 90,  # Triggers flood_warning
    # "wind_speed": 25,  # Triggers storm_warning and snowstorm_warning
    # "wind_bearing": 180,  # Default value
    # "wind_gust": 35,  # Triggers wind_gust_warning
    # "dew_point": -2,  # Default value
    # "uv_index": 8,  # Triggers uv_alert
    # "condition": "mocked_daily",  # Default value
    # "precipitation": 35,  # Triggers flood_warning and rainstorm
    # "precipitation_probability": 100,  # Default value
}

# Hourly forecast mock values to trigger ALERT_RULES
MOCK_FORECAST_HOURLY: dict[str, Any] = {
    # "temperature": -1,  # Triggers heavy_snow and snowstorm_warning
    # "templow": -5,  # Optional, used for additional testing
    # "pressure": 1000,  # Default value
    # "humidity": 90,  # Triggers flood_warning
    # "wind_speed": 25,  # Triggers storm_warning and snowstorm_warning
    # "wind_bearing": 180,  # Default value
    # "wind_gust": 35,  # Triggers wind_gust_warning
    # "dew_point": -2,  # Default value
    # "uv_index": 8,  # Triggers uv_alert
    # "condition": "mocked_hourly",  # Default value
    # "precipitation": 35,  # Triggers flood_warning and rainstorm
    # "precipitation_probability": 100,  # Default value
}
