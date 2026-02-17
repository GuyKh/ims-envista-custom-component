"""The IMS Envista integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.const import CONF_API_TOKEN, Platform
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.loader import async_get_loaded_integration

from ims_envista import IMSEnvista

from .const import (
    CONF_STATION_CONDITIONS,
    CONF_STATION_ID,
    DOMAIN,
    LOGGER,
    SERVICE_DEBUG_GET_COORDINATOR_DATA,
)
from .coordinator import ImsEnvistaUpdateCoordinator
from .data import ImsEnvistaData

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant, ServiceCall

    from .data import ImsEnvistaConfigEntry

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.WEATHER,
]


# https://developers.home-assistant.io/docs/config_entries_index/#setting-up-an-entry
async def async_setup_entry(
    hass: HomeAssistant,
    entry: ImsEnvistaConfigEntry,
) -> bool:
    """Set up this integration using UI."""
    coordinator = ImsEnvistaUpdateCoordinator(hass=hass, config_entry=entry)

    entry.runtime_data = ImsEnvistaData(
        client=IMSEnvista(
            token=entry.data[CONF_API_TOKEN],
            session=async_get_clientsession(hass),
        ),
        integration=async_get_loaded_integration(hass, entry.domain),
        coordinator=coordinator,
        station_id=entry.data[CONF_STATION_ID],
        conditions=entry.data[CONF_STATION_CONDITIONS],
    )
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = entry.runtime_data

    await coordinator.add_station(entry.data[CONF_STATION_ID])

    # https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    if not hass.services.has_service(DOMAIN, SERVICE_DEBUG_GET_COORDINATOR_DATA):

        async def handle_debug_get_coordinator_data(call: ServiceCall) -> None:  # noqa: ARG001
            """Log coordinator data for all loaded IMS Envista entries."""
            data = {
                config_entry.entry_id: config_entry.runtime_data.coordinator.data
                for config_entry in hass.config_entries.async_entries(DOMAIN)
                if config_entry.runtime_data is not None
            }
            LOGGER.info("Coordinator data: %s", data)
            hass.bus.async_fire("custom_component_debug_event", {"data": data})

        hass.services.async_register(
            DOMAIN,
            SERVICE_DEBUG_GET_COORDINATOR_DATA,
            handle_debug_get_coordinator_data,
        )

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ImsEnvistaConfigEntry,
) -> bool:
    """Handle removal of an entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)
        if not hass.config_entries.async_entries(DOMAIN) and hass.services.has_service(
            DOMAIN, SERVICE_DEBUG_GET_COORDINATOR_DATA
        ):
            hass.services.async_remove(DOMAIN, SERVICE_DEBUG_GET_COORDINATOR_DATA)
    return unload_ok


async def async_reload_entry(
    hass: HomeAssistant,
    entry: ImsEnvistaConfigEntry,
) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
