"""Support for RAPT Pill hydrometers."""

from __future__ import annotations

from rapt_ble import SensorUpdate

from homeassistant import config_entries
from homeassistant.components.bluetooth.passive_update_processor import (
    PassiveBluetoothDataProcessor,
    PassiveBluetoothProcessorCoordinator,
    PassiveBluetoothProcessorEntity,
)
from homeassistant.components.sensor import (
    SensorEntity,
)

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.sensor import sensor_update_to_bluetooth_data_update

from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: config_entries.ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the RAPT Pill BLE sensors."""
    coordinator: PassiveBluetoothProcessorCoordinator = hass.data[DOMAIN][
        entry.entry_id
    ]
    processor = PassiveBluetoothDataProcessor(sensor_update_to_bluetooth_data_update)
    entry.async_on_unload(
        processor.async_add_entities_listener(
            RAPTPillBluetoothSensorEntity, async_add_entities
        )
    )
    entry.async_on_unload(coordinator.async_register_processor(processor))


class RAPTPillBluetoothSensorEntity(
    PassiveBluetoothProcessorEntity[
        PassiveBluetoothDataProcessor[float | int | None, SensorUpdate]
    ],
    SensorEntity,
):
    """Representation of a RAPT Pill BLE sensor."""

    @property
    def native_value(self) -> int | float | None:
        """Return the native value."""
        return self.processor.entity_data.get(self.entity_key)
