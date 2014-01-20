'''
Created on 16 Jan 2014

@author: Jamie
'''
import sqlite3 as lite

import pandas
import pandas.io.sql as pd_lite

''' Create the stations database '''
with lite.connect("./db/uk_stations.db") as con:
    cur = con.cursor()    
    cur.execute("DROP TABLE IF EXISTS Stations")
    stations = pandas.read_csv('./tables/uk_stations.csv', encoding="utf-8")
    pd_lite.write_frame(stations, "Stations", con)

''' Create the emissions factors database '''
with lite.connect("./db/defra_carbon.db") as con:
    cur = con.cursor()    
    cur.execute("DROP TABLE IF EXISTS Activities")
    
    activities = ["BusinessBus", "BusinessCarsByMarketSegment","BusinessCarsBySize", 
                  "BusinessFlights", "BusinessFerries", "BusinessRail",
                  "BusinessMotorbike", "BusinessTaxi",
                  "FreightCargoShip","FreightFlights", "FreightHGV", "FreightRail",
                  "FreightSeaTanker", "FreightVans"]
    
    for activity in activities:    
        cur.execute("DROP TABLE IF EXISTS %s" % activity)

    cur.execute("CREATE TABLE Activities(Id INTEGER PRIMARY KEY, Activity TEXT)")
    
    for activity in activities:
        cur.execute("INSERT INTO Activities(Activity) VALUES(?)", (activity,))
        activity_data = pandas.read_csv('./tables/%s.csv' % activity)   
        pd_lite.write_frame(activity_data, activity, con)
        
    cur.execute("SELECT Activity FROM Activities")
    rows = cur.fetchall()
    for row in rows:
        print row[0]

