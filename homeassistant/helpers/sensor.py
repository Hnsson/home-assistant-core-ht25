"""Common functions related to sensor device management."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant import const

from .device_registry import DeviceInfo

if TYPE_CHECKING:
    # `sensor_state_data` is a second-party library (i.e. maintained by Home Assistant
    # core members) which is not strictly required by Home Assistant.
    # Therefore, we import it as a type hint only.
    from sensor_state_data import SensorDeviceInfo
    from bluetooth_sensor_state_data.sensor_state_data import (
        DeviceKey,
        SensorUpdate,
        SensorDeviceInfo,
    )


def sensor_device_info_to_hass_device_info(
    sensor_device_info: SensorDeviceInfo,
) -> DeviceInfo:
    """Convert a sensor_state_data sensor device info to a HA device info."""
    device_info = DeviceInfo()
    if sensor_device_info.name is not None:
        device_info[const.ATTR_NAME] = sensor_device_info.name
    if sensor_device_info.manufacturer is not None:
        device_info[const.ATTR_MANUFACTURER] = sensor_device_info.manufacturer
    if sensor_device_info.model is not None:
        device_info[const.ATTR_MODEL] = sensor_device_info.model
    return device_info


# HELPER FUNCTIONS FOR SENSOR SETUP:
from homeassistant.components.bluetooth.passive_update_processor import (
    PassiveBluetoothDataUpdate,
    PassiveBluetoothEntityKey,
)

# from homeassistant.components.bluetooth import DeviceKey, SensorUpdate


from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass,
)

from homeassistant.const import (
    PERCENTAGE,
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    UnitOfElectricPotential,
    UnitOfTemperature,
    UnitOfPressure,
)


def build_sensor_descriptions(DeviceClass, Units):
    """Test,"""
    return {
        (DeviceClass.TEMPERATURE, Units.TEMP_CELSIUS): SensorEntityDescription(
            key=f"{DeviceClass.TEMPERATURE}_{Units.TEMP_CELSIUS}",
            device_class=SensorDeviceClass.TEMPERATURE,
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        (DeviceClass.TEMPERATURE, Units.TEMP_FAHRENHEIT): SensorEntityDescription(
            key=f"{DeviceClass.TEMPERATURE}_{Units.TEMP_FAHRENHEIT}",
            device_class=SensorDeviceClass.TEMPERATURE,
            native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        (DeviceClass.HUMIDITY, Units.PERCENTAGE): SensorEntityDescription(
            key=f"{DeviceClass.HUMIDITY}_{Units.PERCENTAGE}",
            device_class=SensorDeviceClass.HUMIDITY,
            native_unit_of_measurement=PERCENTAGE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        (DeviceClass.BATTERY, Units.PERCENTAGE): SensorEntityDescription(
            key=f"{DeviceClass.BATTERY}_{Units.PERCENTAGE}",
            device_class=SensorDeviceClass.BATTERY,
            native_unit_of_measurement=PERCENTAGE,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        (DeviceClass.PRESSURE, Units.PRESSURE_MBAR): SensorEntityDescription(
            key=f"{DeviceClass.PRESSURE}_{Units.PRESSURE_MBAR}",
            device_class=SensorDeviceClass.PRESSURE,
            native_unit_of_measurement=UnitOfPressure.MBAR,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        (DeviceClass.VOLTAGE, Units.ELECTRIC_POTENTIAL_VOLT): SensorEntityDescription(
            key=f"{DeviceClass.VOLTAGE}_{Units.ELECTRIC_POTENTIAL_VOLT}",
            device_class=SensorDeviceClass.VOLTAGE,
            native_unit_of_measurement=UnitOfElectricPotential.VOLT,
            state_class=SensorStateClass.MEASUREMENT,
        ),
        (DeviceClass.SPECIFIC_GRAVITY, Units.SPECIFIC_GRAVITY): SensorEntityDescription(
            key=f"{DeviceClass.SPECIFIC_GRAVITY}_{Units.SPECIFIC_GRAVITY}",
            state_class=SensorStateClass.MEASUREMENT,
        ),
        (
            DeviceClass.SIGNAL_STRENGTH,
            Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
        ): SensorEntityDescription(
            key=f"{DeviceClass.SIGNAL_STRENGTH}_{Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT}",
            device_class=SensorDeviceClass.SIGNAL_STRENGTH,
            native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            state_class=SensorStateClass.MEASUREMENT,
            entity_registry_enabled_default=False,
        ),
        (
            DeviceClass.PM25,
            Units.CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        ): SensorEntityDescription(
            key=f"{DeviceClass.PM25}_{Units.CONCENTRATION_MICROGRAMS_PER_CUBIC_METER}",
            device_class=SensorDeviceClass.PM25,
            native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
            state_class=SensorStateClass.MEASUREMENT,
        ),
    }


def _device_key_to_bluetooth_entity_key(
    device_key: DeviceKey,
) -> PassiveBluetoothEntityKey:
    """Convert a device key to an entity key."""
    return PassiveBluetoothEntityKey(device_key.key, device_key.device_id)


def sensor_update_to_bluetooth_data_update(
    sensor_update: SensorUpdate,
    DeviceClass,
    Units,
) -> PassiveBluetoothDataUpdate:
    """Convert a sensor update to a bluetooth data update."""
    return PassiveBluetoothDataUpdate(
        devices={
            device_id: sensor_device_info_to_hass_device_info(device_info)
            for device_id, device_info in sensor_update.devices.items()
        },
        entity_descriptions={
            _device_key_to_bluetooth_entity_key(device_key): build_sensor_descriptions(
                DeviceClass, Units
            )[(description.device_class, description.native_unit_of_measurement)]
            for device_key, description in sensor_update.entity_descriptions.items()
            if description.device_class and description.native_unit_of_measurement
        },
        entity_data={
            _device_key_to_bluetooth_entity_key(device_key): sensor_values.native_value
            for device_key, sensor_values in sensor_update.entity_values.items()
        },
        entity_names={
            _device_key_to_bluetooth_entity_key(device_key): sensor_values.name
            for device_key, sensor_values in sensor_update.entity_values.items()
        },
    )
