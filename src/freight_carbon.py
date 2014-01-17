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
    raise NotImplementedError("Not yet implemented")

def sea(ghg_units="kgCO2e", passenger_type="Average"):
    raise NotImplementedError("Not yet implemented")

def rail(ghg_units="kgCO2e", rail_type="NationalRail"):
    raise NotImplementedError("Not yet implemented")

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
    return van.get_factor(ghg_units, fuel, van_class)

def hgv(ghg_units="kgCO2e", refrigerated=False, percent_laden="Average",
        hgv_type="AllHGV", tonnage=None, unit='km'):
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
            min_weight = 0
    else:
        min_weight = 0
    hgv = FreightHGV()
    return hgv.get_factor(ghg_units, refrigerated,
                          percent_laden, hgv_type,
                          min_weight, unit)

class FreightHGV(FreightTable):
    
    def __init__(self):
        self.table_name = "FreightHGV"
        
    def get_factor(self, ghg_units="kgCO2e", refrigerated=False,
                   percent_laden="Average", hgv_type="AllHGV",
                   min_weight=None, unit="km"):
        con = lite.connect("defra_carbon.db")
        with con:
            cur = con.cursor()
            cur.execute("SELECT %s FROM %s WHERE Refrigerated AND PercentLaden=:PercentLaden AND HGVType=:HGVType AND MinWeight=:MinWeight AND Unit=:Unit" % (ghg_units, self.table_name), 
                        {"PercentLaden": percent_laden,
                         "HGVType": hgv_type,
                         "MinWeight": min_weight,
                         "Unit": unit})
            con.commit()
            row = cur.fetchone()
            if row:
                if row[0] is None:
                    raise Exception('No factor available %s%% laden %ss over %s tonnes' % (percent_laden, hgv_type, min_weight))
                return row[0]
            else:
                raise Exception("Error selecting an HGV record")


class FreightVan(FreightTable):
    
    def __init__(self):
        self.table_name = "FreightVan"
        
    def get_factor(self, ghg_units="kgCO2e", fuel="Unknown", van_class="Average", unit="km"):
        con = lite.connect("defra_carbon.db")
        with con:
            cur = con.cursor()
            cur.execute("SELECT %s FROM %s WHERE Fuel=:Fuel AND VanClass=:VanClass AND Unit=:Unit" % (ghg_units, self.table_name), 
                        {"Fuel": fuel,
                         "VanClass": van_class,
                         "Unit": unit})
            con.commit()
            row = cur.fetchone()
            if row:
                if row[0] is None:
                    raise Exception('No factor available for %s fuelled %s vans' % (fuel, van_class))
                return row[0]
            else:
                raise Exception("%s is not a valid van class" % (van_class))

class FreightRail(FreightTable):
    
    def __init__(self):
        self.table_name = "FreightRail"
        
    def get_factor(self, ghg_units="kgCO2e", rail_type="NationalRail"):
        raise NotImplementedError("Not yet implemented")

class FreightSea(FreightTable):
    
    def __init__(self):
        self.table_name = "FreightSea"
        
    def get_factor(self, ghg_units="kgCO2e", passenger_type="Car"):
        raise NotImplementedError("Not yet implemented")

class FreightAir(FreightTable):
    
    def __init__(self):
        self.table_name = "FreightAir"

    def get_factor(self, ghg_units="kgCO2e", haul="ShortHaul", travel_class="Average", radiative_forcing=True):
        raise NotImplementedError("Not yet implemented")
        con = lite.connect("defra_carbon.db")
        with con:
            cur = con.cursor()    
            cur.execute("SELECT %s FROM %s WHERE Haul=:Haul AND PassengerClass=:PassengerClass" % (ghg_units, self.table_name),
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

        
def get_country(location):
    g = geocoders.GoogleV3()
    place, _geoid = g.geocode(location)
    country = place.split(',')[-1]
    return country
        
         
def main():
    pass

if __name__ == "__main__":
    main()