transport-carbon
================

This is a start at creating an open source Python package for calculating the carbon footprint of transport (UK-focused to begin with).

##Distances
The first step is calculating travel distances. Planned modes are:

###Air
[x] Working prototype completed as travel_distance.air_distance()

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
The second task is fetching carbon intensity. No API exists to serve carbon intensity data from Defra so we will create one ourselves.

At this point we have focused on business transport (cars, flights, ferries, rail) and have created a database which hold 2013 data for these modes.

Van and HGV freight transport are also almost complete for 2013. They are missing data for Well To Tank (upstream emissions).

##Contributing
Please contact Jamie Bull at jamie.bull@oco-carbon.com if you would like to assist in developing this package