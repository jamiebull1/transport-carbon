'''
Created on 15 Jan 2014

@author: Jamie
'''
import bisect

import sqlite3 as lite
from geopy import geocoders

import distance


MAX_SHORT_HAUL_KM = 3700

''' Freight functions '''
def air_freight(origin, destination, ghg_units="kgCO2e", haul=None, radiative_forcing=True, ):
    flights = FreightAir()
    if origin and destination and haul:
        raise Exception("Specify either haul or origin and destination, not both.")
    if not haul:
        haul = get_haul(origin, destination)
    criteria = {"GHGUnits": ghg_units, "Haul": haul, "IncludeRF": radiative_forcing}
    return flights.get_factor(criteria)

def cargo_ship(ghg_units="kgCO2e", ship_type="BulkCarrier", capacity=None,
               capacity_unit=None):
    min_capacity = get_min_capacity(ship_type, "FreightCargoShip", capacity)
    if not capacity_unit:
        capacity_unit = capacity_units[ship_type]
    if capacity_unit == capacity_units["GeneralCargo"]:
        raise Exception("For GeneralCargo you must specify a capacity unit (DWT or DWTandTEU)")
    cargo_ship = FreightCargoShip()
    criteria = {"GHGUnits": ghg_units, "ShipType": ship_type,
                "MinCapacity": min_capacity, "CapacityUnit": capacity_unit}
    return cargo_ship.get_factor(criteria)

def hgv(ghg_units="kgCO2e", refrigerated=False, percent_laden="Average",
        hgv_type="All", tonnage=None, unit='km'):
    if not tonnage is None:
        if hgv_type == "Articulated":
            if tonnage > 33:
                min_weight = 33
            elif tonnage > 3.5:
                min_weight = 3.5
            else:
                raise Exception("HGV must be heavier than 3.5 tonnes")                
        elif hgv_type == "Rigid":
            if tonnage > 17:
                min_weight = 17
            elif tonnage > 7.5:
                min_weight = 7.5
            elif tonnage > 3.5:
                min_weight = 3.5
            else:
                raise Exception("HGV must be heavier than 3.5 tonnes")
    else:
        min_weight = -1
    if hgv_type == "All":
        min_weight = -1
    hgv = FreightHGV()
    criteria = {"GHGUnits": ghg_units, "Refrigerated": refrigerated,
                "PercentLaden": percent_laden, "HGVType": hgv_type,
                "MinWeight": min_weight, "Unit": unit}
    return hgv.get_factor(criteria)

def rail_freight(ghg_units="kgCO2e", rail_type="FreightTrain"):
    trains = FreightRail()
    criteria = {"GHGUnits": ghg_units, "RailType": rail_type}
    return trains.get_factor(criteria)

def sea_tanker(ghg_units="kgCO2e", ship_type="ProductsTanker", capacity=None,
               capacity_unit=None):
    min_capacity = get_min_capacity(ship_type, "FreightSeaTanker", capacity)
    if ship_type in ["LNGTanker", "LPGTanker"]:
        capacity_unit = "M3"
    else:
        capacity_unit = "DWT"
    sea_tanker = FreightSeaTanker()
    criteria = {"GHGUnits": ghg_units, "ShipType": ship_type,
                "MinCapacity": min_capacity, "CapacityUnit": capacity_unit}
    return sea_tanker.get_factor(criteria)

def van(ghg_units="kgCO2e", van_class="Average",
        tonnage=None, fuel="Unknown", unit='km'):
    if not tonnage is None:
        if tonnage < 1.305:
            van_class = "ClassOne"
        elif tonnage < 1.74:
            van_class = "ClassTwo"
        elif tonnage < 3.5:
            van_class = "ClassThree"
        else:
            raise Exception("Vans must weigh less than 3.5 tonnes")
    van = FreightVan()
    criteria = {"GHGUnits": ghg_units, "Fuel": fuel, "VanClass": van_class}
    return van.get_factor(criteria)

capacity_units = {"BulkCarrier": "DWT",
                  "GeneralCargo": ("DWT or DWT and 100+ TEU"),
                  "ContainerShip": "TEU",
                  "VehicleTransport": "CEU",
                  "RoRoFerry": "LM",
                  "LargeRoPaxFerry": None,
                  "RefrigeratedCargo": None}

def get_min_capacity(ship_type, activity, capacity):
    if capacity is None:
        return -1
    with lite.connect("defra_carbon.db") as con:
        cur = con.cursor()
        cur.execute("SELECT MinCapacity FROM %s WHERE ShipType=:ShipType" % activity,
                    {'ShipType': ship_type})
        capacities = sorted([c[0] for c in cur.fetchall()])
        i = bisect.bisect_left(capacities, capacity)
        min_capacity = capacities[i-1]
    return min_capacity

class ActivityTable:
    
    def get_factor(self, criteria):
        query, error_message = self.select_from_criteria(criteria)
        with lite.connect("defra_carbon.db") as con:
            cur = con.cursor()
            cur.execute(query)
            row = cur.fetchone()
            if row:
                return row[0]
            else:
                raise Exception(error_message)
    
    def select_from_criteria(self, criteria):
        ghg_units = criteria.pop('GHGUnits')
        # extract any booleans
        true_bools = [i for i in criteria if criteria[i] is True]
        false_bools = [i for i in criteria if criteria[i] is False]
        # extract any booleans and numbers (booleans first as booleans can be mistaken for ints)
        for b in true_bools:
            criteria.pop(b)
        for b in false_bools:
            criteria.pop(b)
        numbers = {i: criteria[i] for i in criteria
                   if isinstance(criteria[i], int) or isinstance(criteria[i], float)}
        for n in numbers:
            criteria.pop(n)
            
        str_params = ["%s=\"%s\"" % (k, criteria[k]) for k in criteria]
        num_params = ["%s=\"%s\"" % (k, numbers[k]) for k in numbers]
        query = "SELECT %s FROM %s" % (ghg_units, self.table_name)
        if str_params or num_params or true_bools:
            query += " WHERE "
            if str_params:
                query += " AND ".join(str_params)
            if num_params:
                query += " AND " + " AND ".join(num_params)        
            if true_bools:
                query += " AND " + " AND ".join(true_bools)
        error_message = 'Error selecting from database'
        return query, error_message

    @property
    def columns(self):
        with lite.connect("defra_carbon.db") as con:
            cur = con.cursor()    
            cur.execute("SELECT * FROM %s" % self.table_name)
            names = list(map(lambda x: x[0], cur.description))
            return names

    @property
    def ghg_units(self):
        with lite.connect("defra_carbon.db") as con:
            cur = con.cursor()    
            cur.execute("SELECT * FROM %s" % self.table_name)
            names = list(map(lambda x: x[0], cur.description))
            return [nm for nm in names if 'kg' in nm]

    @property
    def options(self):
        with lite.connect("defra_carbon.db") as con:
            cur = con.cursor()    
            cur.execute("SELECT * FROM %s" % self.table_name)
            names = list(map(lambda x: x[0], cur.description))
            return [nm for nm in names if 'kg' not in nm]

class FreightAir(ActivityTable):
    
    def __init__(self):
        self.table_name = "FreightAir"

class FreightCargoShip(ActivityTable):
    
    def __init__(self):
        self.table_name = "FreightCargoShip"
        
class FreightHGV(ActivityTable):
    
    def __init__(self):
        self.table_name = "FreightHGV"
        
class FreightRail(ActivityTable):
    
    def __init__(self):
        self.table_name = "FreightRail"
        
class FreightSeaTanker(ActivityTable):
    
    def __init__(self):
        self.table_name = "FreightSeaTanker"
        
class FreightVan(ActivityTable):
    
    def __init__(self):
        self.table_name = "FreightVan"

''' Business travel functions '''
def air(origin=None, destination=None, ghg_units="kgCO2e", haul=None,
        passenger_class="Average", radiative_forcing=True):
    flights = BusinessAir()
    if not haul:
        if not origin and not destination:
            raise Exception("Cannot determine haul of flight. Either specify haul, or origin and destination.")
        else:
            haul = get_haul(origin, destination)
    criteria = {"GHGUnits": ghg_units, "Haul": haul,
                "PassengerClass": passenger_class, "IncludeRF": radiative_forcing}
    return flights.get_factor(criteria)

def bus(ghg_units="kgCO2e", bus_type="AverageLocalBus"):
    bus = BusinessBus()
    criteria = {"GHGUnits": ghg_units, "BusType": bus_type}
    return bus.get_factor(criteria)

def car(ghg_units="kgCO2e", select_by="Size",
               size="Average", market_segment="UpperMedium",
               fuel="Unknown", unit='km'):
    if select_by == "Size":
        cars = BusinessCarBySize()
        criteria = {"GHGUnits": ghg_units, "Size": size, "Unit": unit}
        return cars.get_factor(criteria)
    elif select_by == "MarketSegment":
        cars = BusinessCarByMarketSegment()
        criteria = {"GHGUnits": ghg_units, "MarketSegment": market_segment, "Unit": unit}
        return cars.get_factor(criteria)
    else:
        raise Exception("%s is not a valid criterion for car selection" % select_by)

def motorbike(ghg_units="kgCO2e", size="Average"):
    motorbikes = BusinessMotorbike()
    criteria = {"GHGUnits": ghg_units, "Size": size}
    return motorbikes.get_factor(criteria)

def rail(ghg_units="kgCO2e", rail_type="NationalRail"):
    trains = BusinessRail()
    criteria = {"GHGUnits": "kgCO2e", "RailType": rail_type}
    return trains.get_factor(criteria)

def sea(ghg_units="kgCO2e", passenger_type="Average"):
    ferries = BusinessSea()
    return ferries.get_factor({"GHGUnits": ghg_units, "PassengerType": passenger_type})

def taxi(ghg_units="kgCO2e", taxi_type="RegularTaxi", units="PassengerKm"):
    taxi = BusinessTaxi()
    return taxi.get_factor({"GHGUnits": ghg_units, "TaxiType": taxi_type})

class BusinessRail(ActivityTable):
    
    def __init__(self):
        self.table_name = "BusinessRail"
        
class BusinessBus(ActivityTable):
    
    def __init__(self):
        self.table_name = "BusinessBus"
        
class BusinessTaxi(ActivityTable):
    
    def __init__(self):
        self.table_name = "BusinessTaxi"

class BusinessMotorbike(ActivityTable):
    
    def __init__(self):
        self.table_name = "BusinessMotorbike"
        
class BusinessSea(ActivityTable):
    
    def __init__(self):
        self.table_name = "BusinessSea"
        
class BusinessAir(ActivityTable):
    
    def __init__(self):
        self.table_name = "BusinessAir"

    def get_haul(self, origin, destination):
        if get_country(origin) == "UK" and get_country(destination) == "UK":
            return "Domestic"
        elif distance.air_distance(origin, destination, 'km') < MAX_SHORT_HAUL_KM:
            return "ShortHaul"
        else:
            return "LongHaul"

class BusinessCarBySize(ActivityTable):
    
    def __init__(self):
        self.table_name = "BusinessCarsBySize"

class BusinessCarByMarketSegment(ActivityTable):
    
    def __init__(self):
        self.table_name = "BusinessCarsByMarketSegment"

def get_country(location):
    g = geocoders.GoogleV3()
    place, _geoid = g.geocode(location)
    country = place.split(',')[-1]
    return country
        
def get_haul(origin, destination):
    if get_country(origin) == "UK" and get_country(destination) == "UK":
        return "Domestic"
    elif distance.air_distance(origin, destination, 'km') < MAX_SHORT_HAUL_KM:
        return "ShortHaul"
    else:
        return "LongHaul"

         
def main():
    pass

if __name__ == "__main__":
    main()