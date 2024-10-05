"""Weather component for IMS Envista."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from homeassistant.components.weather import (
    ATTR_CONDITION_CLEAR_NIGHT,
    ATTR_CONDITION_POURING,
    ATTR_CONDITION_RAINY,
    ATTR_CONDITION_SUNNY,
    WeatherEntity,
)
from homeassistant.const import (
    UnitOfLength,
    UnitOfPressure,
    UnitOfSpeed,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant, callback

from .const import (
    LATEST_KEY,
)

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity_platform import AddEntitiesCallback
    from homeassistant.helpers.typing import DiscoveryInfoType

    from .coordinator import ImsEnvistaUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

weather = None


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,  # noqa: ARG001
) -> None:
    """Set up IMS Weather entity based on a config entry."""
    coordinator = config_entry.runtime_data.coordinator
    station_id = config_entry.runtime_data.station_id
    station_name = coordinator.get_station_info(station_id).name.title()

    ims_weather = IMSEnvistaWeather(station_name, coordinator, station_id)

    async_add_entities([ims_weather])


class IMSEnvistaWeather(WeatherEntity):
    """Implementation of an IMSWeather sensor."""

    _attr_should_poll = False
    _attr_has_entity_name = True
    _attr_native_precipitation_unit = UnitOfLength.MILLIMETERS
    _attr_native_pressure_unit = UnitOfPressure.HPA
    _attr_native_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_native_wind_speed_unit = UnitOfSpeed.METERS_PER_SECOND

    def __init__(
        self,
        station_name: str,
        coordinator: ImsEnvistaUpdateCoordinator,
        station_id: int,
    ) -> None:
        """Initialize the sensor."""
        self._coordinator = coordinator
        self._station_id = station_id
        self._unique_id = f"ims_envista_station_{station_id!s}_weather"
        self._attr_translation_key = "ims_envista_weather"
        self._attr_translation_placeholders = {"station_name": station_name}

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        super()._handle_coordinator_update()

    def _get_latest_data(self, key: str):  # noqa: ANN202
        """Get Coordinator Latest Data."""
        station_data = self._coordinator.data.get(self._station_id)
        if not station_data:
            return None
        latest_station_data = station_data.get(LATEST_KEY)
        if not latest_station_data:
            return None
        return getattr(latest_station_data, key, None)

    @property
    def unique_id(self):  # noqa: ANN201
        """Return a unique_id for this entity."""
        return self._unique_id

    @property
    def native_temperature(self):  # noqa: ANN201
        """Return the temperature."""
        return self._get_latest_data("td")

    @property
    def humidity(self):  # noqa: ANN201
        """Return the humidity."""
        return self._get_latest_data("rh")

    @property
    def native_wind_speed(self):  # noqa: ANN201
        """Return the wind speed."""
        return self._get_latest_data("ws")

    @property
    def native_pressure(self):  # noqa: ANN201
        """Return the wind speed."""
        return self._get_latest_data("bp")

    @property
    def wind_bearing(self):  # noqa: ANN201
        """Return the wind bearing."""
        return self._get_latest_data("wd")

    @property
    def condition(self):  # noqa: ANN201
        """Return the weather condition."""
        monitored_datetime = self._get_latest_data("datetime")
        is_night = False
        if monitored_datetime and (
            monitored_datetime.hour > 20 or monitored_datetime.hour < 7
        ):
            is_night = True

        rain = self._get_latest_data("rain")
        is_clear = rain < 1.0
        if is_clear:
            return ATTR_CONDITION_CLEAR_NIGHT if is_night else ATTR_CONDITION_SUNNY

        return ATTR_CONDITION_POURING if rain > 5.0 else ATTR_CONDITION_RAINY

    async def async_added_to_hass(self) -> None:
        """Connect to dispatcher listening for entity data notifications."""
        self.async_on_remove(
            self._coordinator.async_add_listener(self.async_write_ha_state)
        )
