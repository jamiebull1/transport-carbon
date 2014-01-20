'''
    stations.py written to extract and use data in uk_stations.db
'''
import sqlite3 as lite
import os

from geopy import geocoders, distance

DIR = os.path.dirname(__file__)

def closest(location):
    '''Finds the nearest station (by great circle dist) to
        a given location and returns the station name '''
    g = geocoders.GoogleV3()
    try:
        _address, latlng_a = g.geocode('%s, %s' % (location, 'uk'))
    except TypeError:
        raise TypeError('Location not found')

    with lite.connect(os.path.join(DIR, "db/uk_stations.db")) as con:
        cur = con.cursor()
        cur.execute("SELECT Latitude, Longitude FROM Stations")
        latlngs = cur.fetchall()
        cur.execute("SELECT Station FROM Stations")      
        stations = cur.fetchall()
        
        closest_distance = float('inf')
        for latlng_b, station in zip(latlngs, stations):
#            dist = travel_distance.great_circle_distance(latlng_a, latlng_b)
            dist = distance.distance(latlng_a, latlng_b)
            if closest_distance > dist:
                closest_distance = dist
                closest_station = station[0]
        return closest_station
