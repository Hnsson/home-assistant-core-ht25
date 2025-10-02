"""Support for moat ble sensors."""

from __future__ import annotations

from moat_ble import DeviceClass, DeviceKey, SensorUpdate, Units

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
    """Set up the Moat BLE sensors."""
    coordinator: PassiveBluetoothProcessorCoordinator = hass.data[DOMAIN][
        entry.entry_id
    ]
    processor = PassiveBluetoothDataProcessor(
        lambda update: sensor_update_to_bluetooth_data_update(
            update, DeviceClass, Units
        )
    )
    entry.async_on_unload(
        processor.async_add_entities_listener(
            MoatBluetoothSensorEntity, async_add_entities
        )
    )
    entry.async_on_unload(coordinator.async_register_processor(processor))


class MoatBluetoothSensorEntity(
    PassiveBluetoothProcessorEntity[
        PassiveBluetoothDataProcessor[float | int | None, SensorUpdate]
    ],
    SensorEntity,
):
    """Representation of a moat ble sensor."""

    @property
    def native_value(self) -> int | float | None:
        """Return the native value."""
        return self.processor.entity_data.get(self.entity_key)
