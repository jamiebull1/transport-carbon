transport-carbon
================

This is a start at creating an open source Python package for calculating the carbon footprint of transport (UK-focused to begin with).

##Distances
The first step is calculating travel distances. Planned modes are:

###Air
Working

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

`carbon.air([origin[, destination[, ghg_units[, haul[, travel_class[, radiative_forcing]]]]]]`

Requires either `origin` and `destination`, or `haul` to be passed. `ghg_units` defaults to kgCO2e and `radiative_forcing` defaults to True.

`carbon.bus([ghg_units[, bus_type]])`
`carbon.car([ghg_units[, select_by[, size[, market_segment[, fuel[, unit]]]]]])`
`carbon.motorbike([ghg_units[, size])`
`carbon.rail([ghg_units[, ghg_units[, rail_type]])`
`carbon.sea([ghg_units[, passenger_type]])`
`carbon.taxi([ghg_units[, taxi_type[, unit]]])`

`carbon.air_freight()([origin[, destination[, ghg_units[, haul[, radiative_forcing]]]]]]`

Requires either `origin` and `destination`, or `haul` to be passed. `ghg_units` defaults to kgCO2e and `radiative_forcing` defaults to True.

`carbon.cargo_ship()`
`carbon.hgv()`
`carbon.rail()`
`carbon.sea_tanker()`
`carbon.van()`


##Contributing
Please contact Jamie Bull at jamie.bull@oco-carbon.com if you would like to assist in developing this package