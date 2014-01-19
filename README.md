# Introduction

This library is intended to provide an open source Python package for calculating the carbon footprint of transport (UK-focused to begin with).

The carbon factors are based on the data provided by Defra in their [2013 Government GHG Conversion Factors for Company Reporting] now provided in a web service from Ricardo-AEA[1].

[1] http://www.ukconversionfactorscarbonsmart.co.uk/

The distances are provided from a range of sources at present, some of which need more work, and some of which need replacing.

##Carbon Intensity database
No API exists to serve carbon intensity data from Defra so we have created a database ourselves, `defra_carbon.py`. All business transport and freight transport options have been added for 2013.

The tables are:

- Activities
- BusinessBus
- BusinessCarsByMarketSegment
- BusinessCarsBySize
- BusinessFlights
- BusinessFerries
- BusinessMotorbike
- BusinessRail
- BusinessTaxi
- FreightCargoShip
- FreightFlights
- FreightHGV
- FreightRail
- FreightSeaTanker
- FreightVan

## Functions
For all functions, `ghg_units` defaults to kgCO2e. Well to tank (upstream) emissions are available using kgCO2eWTT.

### Business travel
`carbon.air([origin[, destination[, ghg_units[, haul[, travel_class[, radiative_forcing]]]]]]`

Requires either origin and destination, or haul to be passed. If unspecified, `ghg_units` defaults to "kgCO2e" and radiative_forcing defaults to `True`.

`carbon.bus([ghg_units[, bus_type]])

If unspecified, `bus_type` defaults to "AverageLocalBus".

`carbon.car([ghg_units[, select_by[, size[, market_segment[, fuel[, unit]]]]]])`

If unspecified, `select_by` defaults to "Size", `size` defaults to "Average", `market_segment` defaults to "UpperMedium", `fuel` defaults to "Unknown", and `unit` defaults to "km".

`carbon.motorbike([ghg_units[, size])`

If unspecified, `size` defaults to "Average".

`carbon.rail([ghg_units[, ghg_units[, rail_type]])`

If unspecified, `rail_type` defaults to "NationalRail".

`carbon.sea([ghg_units[, passenger_type]])`

If unspecified, `passenger_type` defaults to "Average".

`carbon.taxi([ghg_units[, taxi_type[, unit]]])`

If unspecified, `taxi_type` defaults to "RegularTaxi", and `units` defaults to "PassengerKm".

### Freight transport
`carbon.air_freight()([origin[, destination[, ghg_units[, haul[, radiative_forcing]]]]]]`

Requires either origin and destination, or haul to be passed. ghg_units defaults to kgCO2e and radiative_forcing defaults to True.

`carbon.cargo_ship([ghg_units[, ship_type[, capacity[, capacity_unit]]]])`

`carbon.hgv([ghg_units[, refrigerated[, percent_laden[, hgv_type[, tonnage[, unit]]]]]])`

`carbon.rail_freight([ghg_units[, rail_type]])`

`carbon.sea_tanker([ghg_units[, ship_type[, capacity[, capacity_unit]]]])`

`carbon.van([ghg_units[, van_class[, tonnage[, fuel[, unit]]]]])`

##Contributing
Please contact Jamie Bull at jamie.bull@oco-carbon.com if you would like to assist in developing this package

