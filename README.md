# Israel Meteorological Service (IMS) Envista Custom Component

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

![Project Maintenance][maintenance-shield]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]


_Integration to integrate with [IMS Envista API][ims-envista-api]._

**This integration could set up the following conditions.**

![Example Image][exampleimg]

Read more here at [Observation Data API Documentation][observation-data-api]

IMS also has a [map of stations][map-of-stations]

For deeper understanding in what every condition means, please read [IMS Documentation][ims-documentation]

Condition | Description
-- | --
`station_name` | Station Name
`last_update` | Last Date/Time where the station data was updated
`rh` | Relative Humidity (%)
`rain` | Amount of rain (mm)
`rain_1_min` | Rainfall  (mm)
`wd` | Wind Direction (deg)
`wd_max` | Top Gust Wind Direction (deg)
`std_wd` | Standard Deviation of Wind Direction (deg)
`ws` | Wind Speed (m/sec)
`ws_1mm` | Maximal 1min Wind Speed (m/sec)
`ws_10mm` | Maximal 10min Wind Speed (m/sec)
`ws_max` | Top Gust Wind Speed (m/sec)
`td` | Dry Temperature (Celsius deg)
`td_max` | Maximal Temperature (Celsius deg)
`td_min` | Minimal Temperature (Celsius deg)
`tg` | Grass Minimum Temperature (Celsius deg)
`bp` | Barometric Pressure (hPa)
`diff` | Diffused Radiation ($\frac{w}{m^2}$)
`grad` | Global Radiation ($\frac{w}{m^2}$)
`nip` | Direct Radiation ($\frac{w}{m^2}$)


## Installation

Automatic (HACS):
1. Add this path to HACS: `https://github.com/GuyKh/ims-envista-custom-component`
2. Install through HACS

Manual:
1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
1. If you do not have a `custom_components` directory (folder) there, you need to create it.
1. In the `custom_components` directory (folder) create a new folder called `ims_envista`.
1. Download _all_ the files from the `custom_components/ims_envista/` directory (folder) in this repository.
1. Place the files you downloaded in the new directory (folder) you created.
1. Restart Home Assistant
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "IMS Envista"

## Configuration is done in the UI

## Logs
To view logs in debug add this to `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    ...
    custom_components.ims_envista: debug
    ims_envista: debug
```

<!---->

## Frequently Asked Questions

#### How to get an IMS Envista API Token?
Contact IMS by sending a mail to [this address](mailto:ims@ims.gov.il)

#### Can I use this custom component without an API key
**No**

<!---->

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[ims-envista-api]: https://ims.gov.il/sites/default/files/2021-09/API%20explanation.pdf
[buymecoffee]: https://www.buymeacoffee.com/guykh
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/guykh/ims-envista-custom-component.svg?style=for-the-badge
[commits]: https://github.com/guykh/ims-envista-custom-component/commits/main
[exampleimg]: example.png
[license-shield]: https://img.shields.io/github/license/guykh/ims-envista-custom-component.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Guy%20Khmelnitsky%20%40GuyKh-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/guykh/ims-envista-custom-component.svg?style=for-the-badge
[releases]: https://github.com/guykh/ims-envista-custom-component/releases
[observation-data-api]: https://ims.gov.il/he/ObservationDataAPI
[map-of-stations]: https://ims.gov.il/en/stations
[ims-documentation]: https://ims.gov.il/sites/default/files/2022-09/%E2%80%8E%D7%9E%D7%93%D7%A8%D7%99%D7%9A%20%D7%9C%D7%9E%D7%A9%D7%AA%D7%9E%D7%A9%20%D7%91%D7%A0%D7%AA%D7%95%D7%A0%D7%99%20%D7%94%D7%A9%D7%9E%D7%98%20%D7%A2%D7%93%D7%9B%D7%95%D7%9F%2003.2022.pdf
