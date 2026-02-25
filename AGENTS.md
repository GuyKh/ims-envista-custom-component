# AI Agent Instructions - IMS Envista Custom Component

This document provides guidance for AI coding agents working on this Home Assistant custom integration project.

## Project Overview

This is a Home Assistant custom component for the Israeli Meteorological Service (IMS) Envista API. It provides weather and sensor entities for station observations.

Integration details:
- Domain: `ims_envista`
- Title: `IMS Envista`
- Repository: `GuyKh/ims-envista-custom-component`

Key directories:
- `custom_components/ims_envista/` - Main integration code
- `config/` - Home Assistant config for local development
- `scripts/` - Local development and validation scripts

## Tech Stack

- Python: 3.12+
- Home Assistant: custom integration architecture (ConfigEntry + DataUpdateCoordinator)
- API library: `ims-envista` (see `manifest.json`)
- Linting/formatting: Ruff

## Code Structure

`custom_components/ims_envista/` includes:
- `__init__.py` - integration setup/unload, service registration
- `const.py` - constants and channel names
- `config_flow.py` - user setup flow
- `coordinator.py` - API polling and station data coordination
- `entity.py` - base coordinator entity
- `sensor.py` - station condition sensors
- `weather.py` - weather entity
- `services.yaml` - service definitions
- `translations/*.json` - localization strings

## Local Development

Always use project scripts:

Setup dependencies:
```bash
./scripts/setup
```

Run Home Assistant:
```bash
./scripts/develop
```

Lint and format:
```bash
./scripts/lint
```

## Working Rules

- Prefer surgical changes; avoid unrelated refactors.
- Follow existing Home Assistant patterns:
  - Config flow owns user setup and validation.
  - Entities read from coordinator data; no direct API calls from entities.
  - Use `ConfigEntryAuthFailed` for auth failures and `UpdateFailed` for transient update failures.
- Keep translations in sync when adding/changing config flow errors, abort reasons, entities, or services.
- Preserve backward compatibility for entity IDs/unique IDs unless explicitly requested.
- If a change can break existing user automations/dashboards, call it out clearly before proceeding.

## Validation

Before finishing work, run:
```bash
./scripts/lint
```

If linting fails, fix issues and rerun until it passes.
