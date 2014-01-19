transport-carbon
================

This is a start at creating an open source Python package for calculating the carbon footprint of transport (UK-focused to begin with).

##Distances
The first step is calculating travel distances. Planned modes are:

###Air
[x] Working prototype completed as `travel_distance.air_distance()`

[x] End to end unit test

[x] Passes end to end unit test

###Road
[x] Working prototype completed as `travel_distance.road_distance()`

[x] End to end unit test

[x] Passes end to end unit test

###Rail
[ ] Working prototype completed as `travel_distance.rail_distance()`

[x] End to end unit test

[ ] Passes end to end unit test (fails on many options and so far no obvious pattern)

###Sea
[ ] Working prototype completed as `travel_distance.sea_distance()` (a very sketchy prototype is under development based on waypoints and Dijkstra's shortest path algorithm)

[ ] Create a grid over the seas and oceans and including all known ports

[ ] Find a non-directional graphing package which implements a fast version of Dijkstra's shortest path algorithm

[ ] End to end unit test

[ ] Passes end to end unit test

##Carbon Intensity
The second task is fetching carbon intensity. No API exists to serve carbon intensity data from Defra so we have created a database ourselves.

The tables are:

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

All business transport and freight transport options have been added for 2013.

Available functions are:

[x] `passenger_carbon.air([origin[, destination[, ghg_units[, haul[, travel_class[, radiative_forcing]]]]]]`
[x] `passenger_carbon.bus([ghg_units[, bus_type]])`
[x] `passenger_carbon.car([ghg_units[, select_by[, size[, market_segment[, fuel[, unit]]]]]])`
[x] `passenger_carbon.motorbike([ghg_units[, size])`
[x] `passenger_carbon.rail([ghg_units[, ghg_units[, rail_type]])`
[x] `passenger_carbon.sea([ghg_units[, passenger_type]])`
[x] `passenger_carbon.taxi([ghg_units[, taxi_type[, unit]]])`

[x] `freight_carbon.air()([origin[, destination[, ghg_units[, haul[, radiative_forcing]]]]]]`
[x] `freight_carbon.cargo_ship()`
[x] `freight_carbon.hgv()`
[x] `freight_carbon.rail()`
[x] `freight_carbon.sea_tanker()`
[x] `freight_carbon.van()`


##Contributing
Please contact Jamie Bull at jamie.bull@oco-carbon.com if you would like to assist in developing this package