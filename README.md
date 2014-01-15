transport-carbon
================

This is a start at creating an open source Python package for calculating the carbon footprint of transport (UK-focused to begin with).

##Distances
The first step is calculating travel distances. Planned modes are:

###Air
[x] Working prototype completed as distance.air_distance()
[x] End to end unit test
[x] Passes end to end unit test

###Road
[x] Working prototype completed as `distance.road_distance()`
[x] End to end unit test
[x] Passes end to end unit test

###Rail
[ ] Working prototype completed as `distance.rail_distance()`
[x] End to end unit test
[ ] Passes end to end unit test (fails on many options and so far no obvious pattern)

###Sea
[ ] Working prototype completed as `distance.sea_distance()` (a very sketchy prototype is under development based on waypoints and Dijkstra's shortest path algorithm)
[ ] Create a grid over the seas and oceans and including all known ports
[ ] Find a non-directional graphing package which implements a fast version of Dijkstra's shortest path algorithm
[ ] End to end unit test
[ ] Passes end to end unit test

##Carbon Intensity
The second task will be fetching carbon intensity. The plan is to find an API to serve carbon intensity data from Defra or to create one ourselves.

##Contributing
Please contact Jamie Bull at jamie.bull@oco-carbon.com if you would like to assist in developing this package