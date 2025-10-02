"""Support for sensorpush ble sensors."""

from __future__ import annotations

from sensorpush_ble import DeviceClass, DeviceKey, SensorUpdate, Units

from homeassistant.components.bluetooth.passive_update_processor import (
    PassiveBluetoothDataProcessor,
    PassiveBluetoothProcessorEntity,
)
from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
)

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.sensor import sensor_update_to_bluetooth_data_update

from . import SensorPushConfigEntry


async def async_setup_entry(
    hass: HomeAssistant,
    entry: SensorPushConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the SensorPush BLE sensors."""
    coordinator = entry.runtime_data
    processor = PassiveBluetoothDataProcessor(
        lambda update: sensor_update_to_bluetooth_data_update(
            update, DeviceClass, Units
        )
    )
    entry.async_on_unload(
        processor.async_add_entities_listener(
            SensorPushBluetoothSensorEntity, async_add_entities
        )
    )
    entry.async_on_unload(
        coordinator.async_register_processor(processor, SensorEntityDescription)
    )


class SensorPushBluetoothSensorEntity(
    PassiveBluetoothProcessorEntity[
        PassiveBluetoothDataProcessor[float | int | None, SensorUpdate]
    ],
    SensorEntity,
):
    """Representation of a sensorpush ble sensor."""

    @property
    def native_value(self) -> int | float | None:
        """Return the native value."""
        return self.processor.entity_data.get(self.entity_key)
