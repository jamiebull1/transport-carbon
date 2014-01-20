**Introduction**

This library provides an open source Python package for calculating the carbon footprint of transport (UK-focused to begin with). The final version will include transport by land, sea or air, whether freight or business travel, by any mode covered in the *Defra GHG Emissions Factors for Company Reporting*.

It is currently in pre-alpha stage as several of the distance functions are incomplete (see *Contributing* and *To-do List* section).

**distance:** provide the distance between two locations using a given transport mode
These functions are provided from a range of sources at present, some of which need more work, and some of which need replacing.

All distance functions are in the format ``distance.[mode]_distance(origin, destination, units)``, and the units default to "km".

    >>> from transport_carbon import *
    >>> road_distance('London', 'Leeds')
    313.473    
    
The available functions are:

``air_distance(origin, destination[, units])``

This function is complete. It calculates the great circle distance between two points. The emissions factors already include an uplift to account for non-optimal routing and stacking at airports.

``rail_distance(origin, destination[, units])``

This function has a working prototype. It is quite successful when used on journeys that are on a single train line (as they should be), however in trying to calculate more complicated journeys it often fails to find a route.

``road_distance(origin, destination[, mode[, units])``

This function is complete. It is based on the Google Directions API as implemented in the ``g_directions`` module. ``mode`` defaults to "driving" and ``units`` defaults to "km".

``sea_distance(origin, destination[, units])``

**carbon:** provide the GHG emissions associated with a form of freight pr business transport
The GHG emissions factors are based on the data provided by Defra in their [2013 Government GHG Conversion Factors for Company Reporting](http://www.ukconversionfactorscarbonsmart.co.uk/) now provided in a web service from Ricardo-AEA.

For all functions, ``ghg_units`` defaults to "kgCO2e". Well to tank (upstream) emissions are available using "kgCO2eWTT". Other emissions factors available are "kgCO2", "kgCH4" and "kgN2O".

    >>> from transport_carbon import *
    >>> motorbike_ghg(size="Small")
    0.11890999999999999 
    
*Business travel*

``air_ghg([origin[, destination[, ghg_units[, haul[, travel_class[, radiative_forcing]]]]]]``

Requires either origin and destination, or haul to be passed. If unspecified radiative_forcing defaults to ``True``.

``bus_ghg([ghg_units[, bus_type]])``  

If unspecified, ``bus_type`` defaults to "AverageLocalBus".

``car_ghg([ghg_units[, select_by[, size[, market_segment[, fuel[, unit]]]]]])``

If unspecified, ``select_by`` defaults to "Size", ``size`` defaults to "Average", ``market_segment`` defaults to "UpperMedium", ``fuel`` defaults to "Unknown", and ``unit`` defaults to "km".

``motorbike_ghg([ghg_units[, size])``

If unspecified, ``size`` defaults to "Average".

``rail_ghg([ghg_units[, ghg_units[, rail_type]])``

If unspecified, ``rail_type`` defaults to "NationalRail".

``ferry_ghg([ghg_units[, passenger_type]])``

If unspecified, ``passenger_type`` defaults to "Average".

``taxi_ghg([ghg_units[, taxi_type[, unit]]])``

If unspecified, ``taxi_type`` defaults to "RegularTaxi", and ``units`` defaults to "PassengerKm".

*Freight transport*

``air_freight_ghg()([origin[, destination[, ghg_units[, haul[, radiative_forcing]]]]]]``

Requires either origin and destination, or haul to be passed. ghg_units defaults to kgCO2e and radiative_forcing defaults to True.

``cargo_ship_ghg([ghg_units[, ship_type[, capacity[, capacity_unit]]]])``

If unspecified, ``ship_type`` defaults to "BulkCarrier". ``capacity`` and ``capacity_units`` default to ``None``. The capacity units are looked up from the ship type, and the formula returns the average emissions factor for the ship type.

``hgv_ghg([ghg_units[, refrigerated[, percent_laden[, hgv_type[, tonnage[, unit]]]]]])``

If unspecified, ``refrigerated`` defaults to ``False``, ``percent_laden`` defaults to "Average", ``hgv_type`` defaults to "All", ``tonnage`` defaults to ``None`` and the formula returns the average emissions factor for the HGV type, and ``unit`` deafults to 'km'.

``rail_freight_ghg([ghg_units[, rail_type]])``

If unspecified, ``rail_type`` defaults to "FreightTrain".

``sea_tanker_ghg([ghg_units[, ship_type[, capacity[, capacity_unit]]]])``

If unspecified, ``ship_type`` defaults to "ProductsTanker". ``capacity`` and ``capacity_units`` default to ``None``. The capacity units are looked up from the ship type, and the formula returns the average emissions factor for the tanker type.

``van_ghg([ghg_units[, van_class[, tonnage[, fuel[, unit]]]]])``

If unspecified, ``van_class`` defaults to "Average", ``tonnage`` defaults to ``None`` and the formula returns the average emissions factor, ``fuel`` defaults to "Unknown", and ``unit`` defaults to "km".

**Carbon Intensity database**

No API exists to serve GHG intensity data from Defra so we have created a database ourselves, ``defra_carbon.py``. All business transport and freight transport options have been added for 2013.

The tables are:

* Activities
* BusinessBus
* BusinessCarsByMarketSegment
* BusinessCarsBySize
* BusinessFlights
* BusinessFerries
* BusinessMotorbike
* BusinessRail
* BusinessTaxi
* FreightCargoShip
* FreightFlights
* FreightHGV
* FreightRail
* FreightSeaTanker
* FreightVan

**Contributing**

Please contact Jamie Bull at jamie.bull@oco-carbon.com if you would like to assist in developing this package

**To-do list**

1. Add other years to the database. Data for 2012 is available in the same format and so should be easy to add. Other years may be more difficult.

2. Create public functions which link distance and carbon calculations. The intended syntax is ``travel_carbon.travel_carbon(origin, destination, mode, **kwargs)``

3. Create the ``sea_distance()`` function. Some thought has gone into this so please contact if you would like to contribute.

4. Improve the ``rail_distance()`` function. A new data source, choosing the start and end station appropriately.

5. Improve test coverage.
