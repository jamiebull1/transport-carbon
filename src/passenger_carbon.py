'''
Created on 15 Jan 2014

@author: Jamie
'''
import sqlite3 as lite
from geopy import geocoders

import travel_distance


MAX_SHORT_HAUL_KM = 3700

class FreightTable:
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

def air(origin, destination, ghg_units="kgCO2e", travel_class="Average", radiative_forcing=True):
    flights = BusinessAir()
    haul = flights.get_haul(origin, destination)
    return flights.get_factor(ghg_units, haul, travel_class, radiative_forcing)

def sea(ghg_units="kgCO2e", passenger_type="Average"):
    ferries = BusinessSea()
    passenger_type = passenger_type
    ghg_units = ghg_units
    return ferries.get_factor(ghg_units, passenger_type)

def rail(ghg_units="kgCO2e", rail_type="NationalRail"):
    trains = BusinessRail()
    rail_type = rail_type
    ghg_units = ghg_units
    return trains.get_factor(ghg_units, rail_type)

def car(ghg_units="kgCO2e", select_by="Size",
               size="Average", market_segment="UpperMedium",
               fuel="Unknown", unit='km'):
    if select_by == "Size":
        cars = BusinessCarBySize()
        return cars.get_factor(ghg_units, size, fuel, unit)
    elif select_by == "MarketSegment":
        cars = BusinessCarByMarketSegment()
        return cars.get_factor(ghg_units, market_segment, fuel, unit)
    else:
        raise Exception("%s is not a valid criterion for car selection" % select_by)

class BusinessRail(FreightTable):
    
    def __init__(self):
        self.table_name = "BusinessRail"
        
    def get_factor(self, ghg_units="kgCO2e", rail_type="NationalRail"):
        con = lite.connect("defra_carbon.db")
        with con:
            cur = con.cursor()    
            cur.execute("SELECT %s FROM %s WHERE RailType=:RailType" % (ghg_units, self.table_name), 
                        {"RailType": rail_type})
            con.commit()
            row = cur.fetchone()
            if row:
                return row[0]
            else:
                raise Exception("%s is not a valid rail type" % (rail_type))

class BusinessSea(FreightTable):
    
    def __init__(self):
        self.table_name = "BusinessSea"
        
    def get_factor(self, ghg_units="kgCO2e", passenger_type="Car"):
        con = lite.connect("defra_carbon.db")
        with con:
            cur = con.cursor()    
            cur.execute("SELECT %s FROM %s WHERE PassengerType=:PassengerType" % (ghg_units, self.table_name), 
                        {"PassengerType": passenger_type})
            con.commit()
            row = cur.fetchone()
            if row:
                return row[0]
            else:
                raise Exception("%s is not a valid ferry type" % (passenger_type))

class BusinessAir(FreightTable):
    
    def __init__(self):
        self.table_name = "BusinessAir"

    def get_factor(self, ghg_units="kgCO2e", haul="ShortHaul", travel_class="Average", radiative_forcing=True):
        con = lite.connect("defra_carbon.db")
        with con:
            cur = con.cursor()    
            cur.execute("SELECT %s FROM %s WHERE Haul=:Haul AND PassengerClass=:PassengerClass AND IncludeRF" % (ghg_units, self.table_name),
                        {"Haul": haul,
                         "PassengerClass": travel_class,
                         "IncludeRF": radiative_forcing})
            con.commit()
            row = cur.fetchone()
            if row:
                return row[0]
            else:
                raise Exception("%s %s is not a valid flight type" % (travel_class, haul))
        
    def get_haul(self, origin, destination):
        if get_country(origin) == "UK" and get_country(destination) == "UK":
            return "Domestic"
        elif travel_distance.air_distance(origin, destination, 'km') < MAX_SHORT_HAUL_KM:
            return "ShortHaul"
        else:
            return "LongHaul"

class BusinessCarBySize(FreightTable):
    
    def __init__(self):
        self.table_name = "BusinessCarsBySize"

    def get_factor(self, ghg_units="kgCO2e", size="Average", fuel="Unknown", unit='km'):
        con = lite.connect("defra_carbon.db")
        with con:
            cur = con.cursor()    
            cur.execute("SELECT %s FROM %s WHERE Size=:Size AND Fuel=:Fuel AND Unit=:Unit" % (ghg_units, self.table_name),
                        {"Size": size,
                         "Fuel": fuel,
                         "Unit": unit})
            con.commit()
            row = cur.fetchone()
            if row:
                return row[0]
            else:
                raise Exception("%s %s %s is not a valid car type" % (size, fuel, unit))
        
class BusinessCarByMarketSegment(FreightTable):
    
    def __init__(self):
        self.table_name = "BusinessCarsByMarketSegment"

    def get_factor(self, ghg_units="kgCO2e", market_segment="UpperMedium", fuel="Unknown", unit='km'):
        con = lite.connect("defra_carbon.db")
        with con:
            cur = con.cursor()    
            cur.execute("SELECT %s FROM %s WHERE MarketSegment=:MarketSegment AND Fuel=:Fuel AND Unit=:Unit" % (ghg_units, self.table_name),
                        {"MarketSegment": market_segment,
                         "Fuel": fuel,
                         "Unit": unit})
            con.commit()
            row = cur.fetchone()
            if row:
                return row[0]
            else:
                raise Exception("%s %s %s is not a valid car type" % (market_segment, fuel, unit))
        
def get_country(location):
    g = geocoders.GoogleV3()
    place, _geoid = g.geocode(location)
    country = place.split(',')[-1]
    return country
        
         
def main():
    pass

if __name__ == "__main__":
    main()