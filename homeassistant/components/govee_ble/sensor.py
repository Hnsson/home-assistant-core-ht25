"""Support for govee ble sensors."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from govee_ble import DeviceClass, SensorUpdate, Units
from govee_ble.parser import ERROR

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

from .coordinator import GoveeBLEConfigEntry, GoveeBLEPassiveBluetoothDataProcessor

type _SensorValueType = str | int | float | date | datetime | Decimal | None


async def async_setup_entry(
    hass: HomeAssistant,
    entry: GoveeBLEConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Govee BLE sensors."""
    coordinator = entry.runtime_data
    processor = PassiveBluetoothDataProcessor(
        lambda update: sensor_update_to_bluetooth_data_update(
            update, DeviceClass, Units
        )
    )
    entry.async_on_unload(
        processor.async_add_entities_listener(
            GoveeBluetoothSensorEntity, async_add_entities
        )
    )
    entry.async_on_unload(
        coordinator.async_register_processor(processor, SensorEntityDescription)
    )


class GoveeBluetoothSensorEntity(
    PassiveBluetoothProcessorEntity[
        PassiveBluetoothDataProcessor[_SensorValueType, SensorUpdate]
    ],
    SensorEntity,
):
    """Representation of a govee ble sensor."""

    processor: GoveeBLEPassiveBluetoothDataProcessor[_SensorValueType]

    @property
    def available(self) -> bool:
        """Return False if sensor is in error."""
        coordinator = self.processor.coordinator
        return self.processor.entity_data.get(self.entity_key) != ERROR and (
            ((model_info := coordinator.model_info) and model_info.sleepy)
            or super().available
        )

    @property
    def native_value(self) -> _SensorValueType:  # pylint: disable=hass-return-type
        """Return the native value."""
        return self.processor.entity_data.get(self.entity_key)
