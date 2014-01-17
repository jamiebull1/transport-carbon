'''
Created on 9 Jan 2014

@author: Jamie
'''
import unittest

import travel_distance
import stations
import passenger_carbon
import freight_carbon

class Test(unittest.TestCase):


    def testRoadtravel_distance(self):
        london_to_leeds = travel_distance.road_distance('London', 'Leeds')
        self.assertAlmostEqual(london_to_leeds, 313, delta=1,
                               msg="Road travel_distance failed on London to Leeds")
        london_to_leeds = travel_distance.road_distance('London', 'Leeds', 'km')
        self.assertAlmostEqual(london_to_leeds, 313, delta=1,
                               msg="Road travel_distance (km) failed on London to Leeds")
        london_to_leeds = travel_distance.road_distance('London', 'Leeds', units='miles')
        self.assertAlmostEqual(london_to_leeds, 195, delta=1,
                               msg="Road travel_distance (miles) failed on London to Leeds")

    def testRailtravel_distance(self):
        london_to_leeds = travel_distance.rail_distance('London Euston', 'Leeds')
        self.assertAlmostEqual(london_to_leeds, 303, delta=1,
                               msg="Rail travel_distance failed on London to Leeds")
        london_to_leeds = travel_distance.rail_distance('London Euston', 'Leeds', 'km')
        self.assertAlmostEqual(london_to_leeds, 303, delta=1,
                               msg="Rail travel_distance (km) failed on London to Leeds")
        london_to_leeds = travel_distance.rail_distance('London Euston', 'Leeds', units='miles')
        self.assertAlmostEqual(london_to_leeds, 188, delta=1,
                               msg="Rail travel_distance (miles) failed on London to Leeds")

    def testAirtravel_distance(self):
        london_to_leeds = travel_distance.air_distance('London Euston', 'Leeds')
        self.assertAlmostEqual(london_to_leeds, 270, delta=1,
                               msg="Air travel_distance failed on London to Leeds")
        london_to_leeds = travel_distance.air_distance('London Euston', 'Leeds', 'km')
        self.assertAlmostEqual(london_to_leeds, 270, delta=1,
                               msg="Air travel_distance (km) failed on London to Leeds")
        london_to_leeds = travel_distance.air_distance('London Euston', 'Leeds', units='miles')
        self.assertAlmostEqual(london_to_leeds, 168, delta=1,
                               msg="Air travel_distance (miles) failed on London to Leeds")
    
    def testRailClosest(self):
        closest = stations.closest('SW9')
        self.assertEquals(closest, 'Stockwell', "Closest stations fails on SW9")
        closest = stations.closest('Napton')
        self.assertEquals(closest, 'Leamington Spa', "Closest stations fails on Napton")

    def testAirCarbonFactor(self):
        factor =  passenger_carbon.BusinessAir().get_factor("kgCO2e", "Domestic", "Average", True)
        self.assertAlmostEqual(factor, 0.326615, 8)

    def testRailCarbonEndToEnd(self):
        factor = passenger_carbon.rail("kgCO2e", "Tram")
        self.assertIsInstance(factor, float)
        
    def testRailCarbonFactor(self):
        factor =  passenger_carbon.BusinessRail().get_factor("kgCO2e", "NationalRail")
        self.assertAlmostEqual(factor, 0.04904, 8)

    def testAirCarbonEndToEnd(self):
        factor = passenger_carbon.air("London", "Glasgow", "kgCO2e", "Economy", True)
        self.assertIsInstance(factor, float)
        
    def testCarCarbonEndToEnd(self):
        factor =  passenger_carbon.car()
        self.assertIsInstance(factor, float)

    def testCarByMarketSegmentCarbonFactor(self):
        factor =  passenger_carbon.BusinessCarByMarketSegment().get_factor("kgCO2e", "UpperMedium")
        self.assertAlmostEqual(factor, 0.19315, 8)

    def testCarByMarketSegmentCarbonEndToEnd(self):
        factor = passenger_carbon.car(select_by="MarketSegment")
        self.assertIsInstance(factor, float)
        
    def testFerryCarbonFactor(self):
        factor =  passenger_carbon.BusinessSea().get_factor("kgCO2e", "Foot")
        self.assertAlmostEqual(factor, 0.01928, 8)

    def testFerryCarbonEndToEnd(self):
        factor = passenger_carbon.sea("kgCO2e", "Car")
        self.assertEquals(factor, 0.13321)

    def testVanCarbonFactor(self):
        factor = freight_carbon.FreightVan().get_factor(ghg_units="kgCO2e", fuel="Diesel", van_class="ClassOne")
        self.assertAlmostEqual(factor, 0.15346443, 8)

    def testVanCarbonEndToEnd(self):
        factor = freight_carbon.van("kgCO2e", fuel="Petrol", tonnage=1.7)
        self.assertAlmostEqual(factor, 0.212229316, 8)
        factor = freight_carbon.van("kgCO2e")

    def testHGVCarbonFactor(self):
        factor = freight_carbon.FreightHGV().get_factor(ghg_units="kgCO2e", percent_laden=50,
                                                                      hgv_type="Articulated", min_weight=3.5,
                                                                      refrigerated=True)
        self.assertAlmostEqual(factor, 1.092565762, 8)

    def testHGVCarbonEndToEnd(self):
        factor = freight_carbon.hgv("kgCO2e", tonnage=25)
        self.assertAlmostEqual(factor, 1.087226, 8)
        factor = freight_carbon.hgv("kgCO2e")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()