'''
Created on 9 Jan 2014

@author: Jamie
'''
import math
import requests
import re

from pygeocoder import Geocoder

import stations
from g_directions import GoogleDirections

''' Distance conversion constants '''
CHAINS_PER_MILE = 0.0125
KM_PER_MILE = 1.6093
EARTH_RADIUS = 6378137 # earth radius in meters
''' GCD_UPLIFT (Great Circle Distance) is an uplift to account for
    non-optimal routing and stacking (now included in GHG factors
    so set to zero) '''
GCD_UPLIFT = 0.00 # This may be different in years before 2013


def air_distance(origin, destination, units='km'):
    ''' Uses great circle distance and an uplift factor of 9% following
    Defra's guidance '''
    latlng_a = Geocoder.geocode(origin).coordinates
    latlng_b = Geocoder.geocode(destination).coordinates
    
    dist = great_circle_distance(latlng_a, latlng_b)

    if units == 'km':
        dist = dist / 1000.0
    elif units == 'miles':
        dist = dist / 1000.0 / KM_PER_MILE
    else:
        raise Exception('%s is not a valid unit system. Use "km" or "miles"' % units)

    return dist * (1 + GCD_UPLIFT)

def road_distance(origin, destination, mode='driving', units='km'):
    ''' Uses the Google Directions API '''
    gd = GoogleDirections()
    options = {'mode': mode}
    dist = gd.query(origin, destination, options).distance
    if units == 'km':
        dist = dist / 1000.0
    elif units == 'miles':
        dist = dist / 1000.0 / KM_PER_MILE
    else:
        raise Exception('%s is not a valid unit system. Use "km" or "miles"' % units)
    
    return dist
    
def rail_distance(origin, destination, units='km'):
    ''' Uses the site railmiles.org as an unofficial API. It's very shaky so would
    like to find a better source to use '''
    origin = stations.closest(origin)
    destination = stations.closest(destination)

    query = {'origin': origin,
             'destination': destination,
             'type': 'text',
             'shortestroutes': 'on'}
    page = requests.post('http://mileage.railmiles.org/rmv2a.php/', data=query)

    if "Error: " in page.text:
        raise Exception('railmiles.org returned an error')

    miles_pattern = re.compile('>Distance: (.*)mi \d')
    miles = int(re.findall(miles_pattern, page.text)[0])
    chains_pattern = re.compile('>Distance: \S* (.*)ch -')
    chains = int(re.findall(chains_pattern, page.text)[0])
    
    dist = miles + chains * CHAINS_PER_MILE
    
    if units == 'km':
        dist = dist * KM_PER_MILE
    elif units == 'miles':
        pass
    else:
        raise Exception('%s is not a valid unit system. Use "km" or "miles"' % units)
    
    return dist

def sea_distance(origin, destination, units='km'):
    raise NotImplementedError("sea_distance is not yet implemented")

def great_circle_distance(latlng_a, latlng_b):
    ''' From Gist https://gist.github.com/gabesmed/1826175 '''
    lat1, lon1 = latlng_a
    lat2, lon2 = latlng_b
 
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = (math.sin(dLat / 2) * math.sin(dLat / 2) +
            math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
            math.sin(dLon / 2) * math.sin(dLon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = EARTH_RADIUS * c
    
    return d    

def main():
    pass

if __name__ == "__main__":
    main()