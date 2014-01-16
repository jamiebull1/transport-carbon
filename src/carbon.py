'''
Created on 15 Jan 2014

@author: Jamie
'''
import sqlite3 as lite
import sys

import distance


MAX_SHORT_HAUL_KM = 3700

def air_carbon(origin, destination, travel_class, radiative_forcing=False):
    activity = "Flights"
    haul = get_haul(origin, destination)
    travel_class = travel_class
    if radiative_forcing:
        units = "kgCO2ePerPassengerKmRF"
    else:
        units = "kgCO2ePerPassengerKmNoRF"
    return get_factor(activity, units, haul, travel_class)

def get_factor(activity, units, haul, travel_class):
    con = lite.connect("defra_carbon.db")
    with con:
        cur = con.cursor()    
        cur.execute("SELECT %s FROM %s WHERE Haul=:Haul AND TravelClass=:TravelClass" % (units, activity),  
                    {"Haul": haul,
                     "TravelClass": travel_class})
        con.commit()
        row = cur.fetchone()
        if row:
            return row[0]
        else:
            raise Exception("%s %s is not a valid flight type" % (travel_class, haul))
        
def get_haul(origin, destination):
    if get_country(origin) == "UK" and get_country(destination) == "UK":
        return "Domestic"
    elif distance.air_distance(origin, destination, 'km') < MAX_SHORT_HAUL_KM:
        return "ShortHaul"
    else:
        return "LongHaul"

def get_country(location):
    raise Exception("get_country() not yet implemented")

def add_table():
    flights = (
        (1,'Domestic','Average',0.035618,0.035618),
        (2,'ShortHaul','Average',0.020995,0.020995),
        (3,'ShortHaul','Economy',0.020012,0.020012),
        (4,'ShortHaul','Business',0.030013,0.030013),
        (5,'LongHaul','Average',0.02471,0.02471),
        (6,'LongHaul','Economy',0.018047,0.018047),
        (7,'LongHaul','PremiumEconomy',0.028868,0.028868),
        (8,'LongHaul','Business',0.052326,0.052326),
        (9,'LongHaul','First',0.072166,0.072166)
    )
    con = None
    try:
        con = lite.connect("defra_carbon.db")
        with con:
            cur = con.cursor()    
            cur.execute("DROP TABLE IF EXISTS Activities")
            cur.execute("CREATE TABLE Activities(Id INT, Name TEXT)")
            cur.execute("INSERT INTO Activities VALUES(1,'Flights')")
            cur.execute("DROP TABLE IF EXISTS Flights")
            cur.execute("CREATE TABLE Flights(Id INT, Haul TEXT, TravelClass TEXT, kgCO2ePerPassengerKm_RF REAL, kgCO2ePerPassengerKm_NoRF REAL)")
            cur.executemany("INSERT INTO Flights VALUES(?, ?, ?, ?, ?)", flights)
         
    except lite.Error, e:
        print "Error %s:" % e.args[0]
        sys.exit(1)


def test():
    pass

def main():
#    add_table()
    test()
    

if __name__ == "__main__":
    main()