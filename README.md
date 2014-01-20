# Introduction

This library is intended to provide an open source Python package for calculating the carbon footprint of transport (UK-focused to begin with).

##Distance functions
The distances are provided from a range of sources at present, some of which need more work, and some of which need replacing.

All distance functions are in the format `distance.[mode]_distance(origin, destination, units)`, and the units default to "km".

The available functions are:

`air_distance(origin, destination[, units])`

This function is complete. It calculates the great circle distance between two points. The emissions factors already include an uplift to account for non-optimal routing and stacking at airports.

`rail_distance(origin, destination[, units])`

This function has a working prototype. It is quite successful when used on journeys that are on a single train line (as they should be), however in trying to calculate more complicated journeys it often fails to find a route.

`road_distance(origin, destination[, mode[, units])`

This function is based on the Google Directions API as implemented in the `g_directions` module. `mode` defaults to "driving" and `units` defaults to "km".

`sea_distance(origin, destination[, units])`

## Carbon functions
The carbon factors are based on the data provided by Defra in their [2013 Government GHG Conversion Factors for Company Reporting](http://www.ukconversionfactorscarbonsmart.co.uk/) now provided in a web service from Ricardo-AEA.

For all functions, `ghg_units` defaults to kgCO2e. Well to tank (upstream) emissions are available using kgCO2eWTT.

### Business travel
`carbon.air([origin[, destination[, ghg_units[, haul[, travel_class[, radiative_forcing]]]]]]`

Requires either origin and destination, or haul to be passed. If unspecified, `ghg_units` defaults to "kgCO2e" and radiative_forcing defaults to `True`.

`carbon.bus([ghg_units[, bus_type]])`  

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

If unspecified, `ship_type` defaults to "BulkCarrier". `capacity` and `capacity_units` default to `None`. The capacity units are looked up from the ship type, and the formula returns the average emissions factor for the ship type.

`carbon.hgv([ghg_units[, refrigerated[, percent_laden[, hgv_type[, tonnage[, unit]]]]]])`

If unspecified, `refrigerated` defaults to `False`, `percent_laden` defaults to "Average", `hgv_type` defaults to "All", `tonnage` defaults to `None` and the formula returns the average emissions factor for the HGV type, and `unit` deafults to 'km'.

`carbon.rail_freight([ghg_units[, rail_type]])`

If unspecified, `rail_type` defaults to "FreightTrain.

`carbon.sea_tanker([ghg_units[, ship_type[, capacity[, capacity_unit]]]])`

If unspecified, `ship_type` defaults to "ProductsTanker". `capacity` and `capacity_units` default to `None`. The capacity units are looked up from the ship type, and the formula returns the average emissions factor for the tanker type.

`carbon.van([ghg_units[, van_class[, tonnage[, fuel[, unit]]]]])`

If unspecified, `van_class` defaults to "Average", `tonnage` defaults to `None` and the formula returns the average emissions factor, `fuel` defaults to "Unknown", and `unit` defaults to "km".

####Carbon Intensity database
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

##Contributing
Please contact Jamie Bull at jamie.bull@oco-carbon.com if you would like to assist in developing this package

####ToDo list
1. Add other years to the database. Data for 2012 is available in the same format and so should be easy to add. Other years may be more difficult.
2. Create public functions which link distance and carbon calculations. The intended syntax is `travel_carbon.travel_carbon(origin, destination, mode, **kwargs)`
3. Create the `sea_distance()` function. Some thought has gone into this so please contact if you would like to contribute.
4. Improve the `rail_distance()` function. A new data source, choosing the start and end station appropriately.
5. Improve test coverage.
