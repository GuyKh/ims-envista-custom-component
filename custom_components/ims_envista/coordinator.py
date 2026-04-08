"""DataUpdateCoordinator for ims_envista."""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING, Any, cast

from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from ims_envista import ImsEnvistaApiClientAuthenticationError, ImsEnvistaApiClientError

from .const import DOMAIN, LATEST_KEY, LOGGER

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant

    from ims_envista.station_data import StationInfo

    from .data import ImsEnvistaConfigEntry, ImsEnvistaData


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class ImsEnvistaUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: ImsEnvistaConfigEntry

    async def _verify_station(self, station_id: int) -> bool:
        """Verify station exists."""
        if station_id in self._stations:
            LOGGER.error(
                "Coordinator already fetches data for station: %s", str(station_id)
            )
            return False
        try:
            entry_data = cast(
                "ImsEnvistaData", self.hass.data[DOMAIN][self.config_entry.entry_id]
            )
            station_info = await entry_data.client.get_station_info(station_id)
            self._stations_static_data[station_id] = station_info
        except ImsEnvistaApiClientError as exception:
            LOGGER.error("Error getting station info: %s", exception)
            raise UpdateFailed(exception) from exception
        return True

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize."""
        self._stations: list[int] = []
        self._stations_static_data: dict[int, StationInfo] = {}

        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=10),
        )
        self.config_entry = config_entry

    async def add_station(self, station_id: int) -> None:
        """Add station."""
        if await self._verify_station(station_id):
            LOGGER.debug("Adding station %d to coordinator", station_id)
            self._stations.append(station_id)
        else:
            LOGGER.error("Station %s does not exist", station_id)

    async def remove_station(self, station_id: int) -> None:
        """Add station."""
        if station_id in self._stations:
            LOGGER.debug("Removing station %d from coordinator", station_id)
            self._stations_static_data.pop(station_id)
            self._stations.remove(station_id)
        else:
            LOGGER.error("Station %s does not exist in the coordinator", station_id)

    def get_station_info(self, station_id: int) -> StationInfo | None:
        """Get station info by station id."""
        station_info = self._stations_static_data.get(station_id)
        if not station_info:
            LOGGER.error("Missing station %s data in coordinator", station_id)
        return station_info

    async def _async_update_data(self) -> dict[int, dict[str, Any]]:
        """Update data via library."""
        station_data: dict[int, dict[str, Any]] = {}
        try:
            for station in self._stations:
                LOGGER.debug("Updating Station %d", station)
                station_data[station] = station_data.get(station, {})

                entry_data = cast(
                    "ImsEnvistaData", self.hass.data[DOMAIN][self.config_entry.entry_id]
                )
                station_latest_res = await entry_data.client.get_latest_station_data(
                    station
                )

                station_latest = station_latest_res.data[0]
                LOGGER.debug("Station %d latest data: %s", station, station_latest)
                station_data[station][LATEST_KEY] = station_latest

                # station_daily = (
                #     await self.config_entry.runtime_data.client.get_daily_station_data
                #     (
                #         station
                #     )
                # )
                # station_data[station][DAILY_KEY] = station_daily.data

        except ImsEnvistaApiClientAuthenticationError as exception:
            raise ConfigEntryAuthFailed(exception) from exception
        except ImsEnvistaApiClientError as exception:
            raise UpdateFailed(exception) from exception
        else:
            return station_data
