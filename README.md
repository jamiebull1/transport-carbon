# Introduction

This library is intended to provide an open source Python package for calculating the carbon footprint of transport (UK-focused to begin with).

The carbon factors are based on the data provided by Defra in their [2013 Government GHG Conversion Factors for Company Reporting] now provided in a web service from Ricardo-AEA[1].

[1] http://www.ukconversionfactorscarbonsmart.co.uk/

The distances are provided from a range of sources at present, some of which need more work and some of which need replacing.

##Carbon Intensity database
No API exists to serve carbon intensity data from Defra so we have created a database ourselves, `defra_carbon.py`. All business transport and freight transport options have been added for 2013.

The tables are:

- Activities
- BusinessBus
- BusinessCarsByMarketSegment
- BusinessCarsBySize
- BusinessFlights
- BusinessFerries
- BusinessRail
- BusinessMotorbike
- BusinessTaxi
- FreightCargoShip
- FreightFlights
- FreightHGV
- FreightRail
- FreightSeaTanker
- FreightVan


## Functions
For all functions, ghg_units defaults to kgCO2e. Well to tank (upstream) emissions are available using kgCO2eWTT.

The available options for a function can be found by 

### Business travel
`carbon.air([origin[, destination[, ghg_units[, haul[, travel_class[, radiative_forcing]]]]]]`
Requires either origin and destination, or haul to be passed. ghg_units defaults to kgCO2e and radiative_forcing defaults to True.

`carbon.bus([ghg_units[, bus_type]])
`carbon.car([ghg_units[, select_by[, size[, market_segment[, fuel[, unit]]]]]])`
`carbon.motorbike([ghg_units[, size])`
`carbon.rail([ghg_units[, ghg_units[, rail_type]])`
`carbon.sea([ghg_units[, passenger_type]])`
`carbon.taxi([ghg_units[, taxi_type[, unit]]])`

### Freight transport
`carbon.air_freight()([origin[, destination[, ghg_units[, haul[, radiative_forcing]]]]]]`
Requires either origin and destination, or haul to be passed. ghg_units defaults to kgCO2e and radiative_forcing defaults to True.
`carbon.cargo_ship()`
`carbon.hgv()`
`carbon.rail()`
`carbon.sea_tanker()`
`carbon.van()`


##Contributing
Please contact Jamie Bull at jamie.bull@oco-carbon.com if you would like to assist in developing this package

