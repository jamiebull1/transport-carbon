'''
Created on 9 Jan 2014

@author: Jamie
'''
import unittest

import distance
import stations
import carbon

class Test(unittest.TestCase):


    def testRoadDistance(self):
        london_to_leeds = distance.road_distance('London', 'Leeds')
        self.assertAlmostEqual(london_to_leeds, 313, delta=1,
                               msg="Road distance failed on London to Leeds")
        london_to_leeds = distance.road_distance('London', 'Leeds', 'km')
        self.assertAlmostEqual(london_to_leeds, 313, delta=1,
                               msg="Road distance (km) failed on London to Leeds")
        london_to_leeds = distance.road_distance('London', 'Leeds', units='miles')
        self.assertAlmostEqual(london_to_leeds, 195, delta=1,
                               msg="Road distance (miles) failed on London to Leeds")

    def testRailDistance(self):
        london_to_leeds = distance.rail_distance('London Euston', 'Leeds')
        self.assertAlmostEqual(london_to_leeds, 303, delta=1,
                               msg="Rail distance failed on London to Leeds")
        london_to_leeds = distance.rail_distance('London Euston', 'Leeds', 'km')
        self.assertAlmostEqual(london_to_leeds, 303, delta=1,
                               msg="Rail distance (km) failed on London to Leeds")
        london_to_leeds = distance.rail_distance('London Euston', 'Leeds', units='miles')
        self.assertAlmostEqual(london_to_leeds, 188, delta=1,
                               msg="Rail distance (miles) failed on London to Leeds")
        print london_to_leeds

    def testAirDistance(self):
        london_to_leeds = distance.air_distance('London Euston', 'Leeds')
        self.assertAlmostEqual(london_to_leeds, 292, delta=1,
                               msg="Air distance failed on London to Leeds")
        london_to_leeds = distance.air_distance('London Euston', 'Leeds', 'km')
        self.assertAlmostEqual(london_to_leeds, 292, delta=1,
                               msg="Air distance (km) failed on London to Leeds")
        london_to_leeds = distance.air_distance('London Euston', 'Leeds', units='miles')
        self.assertAlmostEqual(london_to_leeds, 181, delta=1,
                               msg="Air distance (miles) failed on London to Leeds")
    
    def testRailClosest(self):
        closest = stations.closest('SW9')
        self.assertEquals(closest, 'Stockwell', "Closest stations fails on SW9")
        closest = stations.closest('Napton')
        self.assertEquals(closest, 'Leamington Spa', "Closest stations fails on Napton")

    def testAirCarbonFactor(self):
        factor =  carbon.get_factor("Flights", "kgCO2ePerPassengerKm_NoRF", "Domestic", "Average")
        self.assertEquals(factor, 0.035618)

    def testAirCarbonEndToEnd(self):
        factor = carbon.air_carbon("London", "Madrid", "Economy", True)
        self.assertIsInstance(factor, float)
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()