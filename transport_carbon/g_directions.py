"""
    g_directions.py Google Directions API wrapper,
    based on https://pypi.python.org/pypi/google.directions by D9T GmbH, Daniel Kraft.
"""
import urllib, urllib2
import json

class GoogleDirections(object):
    url="http://maps.googleapis.com/maps/api/directions/json?origin=%s&destination=%s&sensor=false&"
    
    def __init__(self):
        self.result = None
        self.origin = None
        self.destination = None

    def query(self, origin, destination, options=None, headers=None,):
        if self.result and self.origin==origin and self.destination==destination:
            return self
        self.origin = origin
        self.destination = destination
        url = self.url % (
            urllib.quote(origin),
            urllib.quote(destination),
        )
        if not headers:
            headers = {}
        if options:
            url += urllib.urlencode(options)
        req = urllib2.Request(url, None, headers)
        res = urllib2.urlopen(req).read()
        self.result = json.loads(res)
        return self

    @property
    def status(self):
        """
            Returns the status of the query. Check if this is == "OK".
        """
        return self.result["status"]

    @property
    def distance(self):
        """
            Returns the travel distance in meters.
        """
        return sum([leg["distance"]["value"]
                    for leg in self.result['routes'][0]['legs']])

    @property
    def duration(self):
        """
            Returns the travel time in seconds.
        """
        return sum([leg["duration"]["value"]
                    for leg in self.result["routes"][0]["legs"]])

    @property
    def start_address(self):
        """
            Returns an address line
        """
        return self.result["routes"][0]["legs"][0]['start_address']

    @property
    def end_address(self):
        """
            Returns an address line
        """
        return self.result["routes"][0]["legs"][-1]['end_address']

