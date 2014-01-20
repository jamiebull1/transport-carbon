'''
Created on 9 Jan 2014

@author: Jamie
'''
import unittest

from transport_carbon import *

class Test(unittest.TestCase):


    def testRoadtravel_distance(self):
        london_to_leeds = distance.road_distance('London', 'Leeds')
        self.assertAlmostEqual(london_to_leeds, 313, delta=1,
                               msg="Road distance failed on London to Leeds")
        london_to_leeds = distance.road_distance('London', 'Leeds', 'km')
        self.assertAlmostEqual(london_to_leeds, 313, delta=1,
                               msg="Road distance (km) failed on London to Leeds")
        london_to_leeds = distance.road_distance('London', 'Leeds', units='miles')
        self.assertAlmostEqual(london_to_leeds, 195, delta=1,
                               msg="Road distance (miles) failed on London to Leeds")

    def testRailtravel_distance(self):
        london_to_leeds = distance.rail_distance('London Euston', 'Leeds')
        self.assertAlmostEqual(london_to_leeds, 303, delta=1,
                               msg="Rail distance failed on London to Leeds")
        london_to_leeds = distance.rail_distance('London Euston', 'Leeds', 'km')
        self.assertAlmostEqual(london_to_leeds, 303, delta=1,
                               msg="Rail distance (km) failed on London to Leeds")
        london_to_leeds = distance.rail_distance('London Euston', 'Leeds', units='miles')
        self.assertAlmostEqual(london_to_leeds, 188, delta=1,
                               msg="Rail distance (miles) failed on London to Leeds")

    def testAirtravel_distance(self):
        london_to_leeds = distance.air_distance('London Euston', 'Leeds')
        self.assertAlmostEqual(london_to_leeds, 270, delta=1,
                               msg="Air distance failed on London to Leeds")
        london_to_leeds = distance.air_distance('London Euston', 'Leeds', 'km')
        self.assertAlmostEqual(london_to_leeds, 270, delta=1,
                               msg="Air distance (km) failed on London to Leeds")
        london_to_leeds = distance.air_distance('London Euston', 'Leeds', units='miles')
        self.assertAlmostEqual(london_to_leeds, 168, delta=1,
                               msg="Air distance (miles) failed on London to Leeds")
    
    def testAirCarbonEndToEnd(self):
        factor = carbon.air_ghg("London", "Glasgow", "kgCO2e",
                                      passenger_class="Economy", radiative_forcing=True)
        self.assertIsInstance(factor, float)
        factor = carbon.air_ghg("kgCO2e", haul="ShortHaul",
                                      passenger_class="Economy", radiative_forcing=True)
        self.assertIsInstance(factor, float)
        
    def testAirCarbonFactor(self):
        factor =  carbon.BusinessFlights().get_factor({"GHGUnits": "kgCO2e", "Haul": "Domestic",
                                                   "PassengerClass": "Average", "IncludeRF": True})
        self.assertAlmostEqual(factor, 0.326615, 8)

    def testBusCarbonEndToEnd(self):
        factor = carbon.bus_ghg("kgCO2e", "Coach")
        self.assertIsInstance(factor, float)
        
    def testBusCarbonFactor(self):
        factor = carbon.BusinessBus().get_factor({"GHGUnits": "kgCO2e", "BusType": "Coach"})
        self.assertAlmostEqual(factor, 0.02932, 8)

    def testCarCarbonEndToEnd(self):
        factor =  carbon.car_ghg()
        self.assertIsInstance(factor, float)

    def testCarByMarketSegmentCarbonFactor(self):
        factor =  carbon.BusinessCarByMarketSegment().get_factor({"GHGUnits": "kgCO2e",
                                                                  "MarketSegment": "UpperMedium"})
        self.assertAlmostEqual(factor, 0.17224, 8)

    def testCarByMarketSegmentCarbonEndToEnd(self):
        factor = carbon.car_ghg(select_by="MarketSegment")
        self.assertIsInstance(factor, float)
        
    def testFerryCarbonFactor(self):
        factor =  carbon.BusinessFerries().get_factor({"GHGUnits": "kgCO2e", "PassengerType": "Foot"})
        self.assertAlmostEqual(factor, 0.01928, 8)

    def testFerryCarbonEndToEnd(self):
        factor = carbon.ferry_ghg("kgCO2e", "Car")
        self.assertEquals(factor, 0.13321)

    def testRailClosest(self):
        closest = stations.closest('SW9')
        self.assertEquals(closest, 'Stockwell', "Closest stations fails on SW9")
        closest = stations.closest('Napton')
        self.assertEquals(closest, 'Leamington Spa', "Closest stations fails on Napton")

    def testMotorbikeCarbonEndToEnd(self):
        factor = carbon.motorbike_ghg(ghg_units="kgCO2e", size="Large")
        self.assertIsInstance(factor, float)
        
    def testMotorbikeCarbonFactor(self):
        factor =  carbon.BusinessMotorbike().get_factor({"GHGUnits": "kgCO2e", "Size": "Small"})
        self.assertAlmostEqual(factor, 0.08774, 8)

    def testRailCarbonEndToEnd(self):
        factor = carbon.rail_ghg({"GHGUnits": "kgCO2e", "RailType": "Tram"})
        self.assertIsInstance(factor, float)
        
    def testRailCarbonFactor(self):
        factor =  carbon.BusinessRail().get_factor({"GHGUnits": "kgCO2e", "RailType": "NationalRail"})
        self.assertAlmostEqual(factor, 0.04904, 8)

    def testTaxiCarbonEndToEnd(self):
        factor = carbon.taxi_ghg(ghg_units="kgCO2e", taxi_type="BlackCab")
        self.assertIsInstance(factor, float)
        
    def testTaxiCarbonFactor(self):
        factor = carbon.BusinessTaxi().get_factor({"GHGUnits": "kgCO2e", "TaxiType": "RegularTaxi"})
        self.assertAlmostEqual(factor, 0.144342857, 8)

    def testVanCarbonFactor(self):
        factor = carbon.FreightVans().get_factor({"GHGUnits": "kgCO2e",
                                                 "Fuel": "Diesel",
                                                 "VanClass": "ClassOne"})
        self.assertAlmostEqual(factor, 0.650217502, 8)

    def testVanCarbonEndToEnd(self):
        factor = carbon.van_ghg("kgCO2e", fuel="Petrol", tonnage=1.7)
        self.assertAlmostEqual(factor, 0.80545922, 8)
        factor = carbon.van_ghg("kgCO2e")

    def testHGVCarbonFactor(self):
        factor = carbon.FreightHGV().get_factor({"GHGUnits": "kgCO2e",
                                                 "PercentLaden": 50,
                                                 "HGVType": "Articulated",
                                                 "MinWeight": 3.5,
                                                 "Refrigerated": True})
        self.assertAlmostEqual(factor, 0.174482, 8)

    def testHGVCarbonEndToEnd(self):
        factor = carbon.hgv_ghg(ghg_units="kgCO2e", tonnage=25)
        self.assertAlmostEqual(factor, 0.90765, 8)
        factor = carbon.hgv_ghg("kgCO2e")

    def testAirFreightCarbonEndToEnd(self):
        factor = carbon.air_freight_ghg(origin="London", destination="Glasgow",
                                    ghg_units="kgCO2e", radiative_forcing=True)
        self.assertIsInstance(factor, float)
        
    def testAirFreightCarbonFactor(self):
        criteria = {"GHGUnits":"kgCO2e", "Haul": "Domestic", "IncludeRF": False}
        factor = carbon.FreightFlights().get_factor(criteria)
        self.assertAlmostEqual(factor, 4.136955, 8)

    def testRailFreightCarbonEndToEnd(self):
        factor = carbon.rail_ghg(ghg_units="kgCO2e")
        self.assertIsInstance(factor, float)
        
    def testRailFreightCarbonFactor(self):
        factor = carbon.FreightRail().get_factor({"GHGUnits": "kgCO2e"})
        self.assertAlmostEqual(factor, 0.02721, 8)

    def testSeaTankerFreightCarbonEndToEnd(self):
        factor = carbon.sea_tanker_ghg(ghg_units="kgCO2e",
                                   ship_type="ChemicalTanker",
                                   capacity=40000)
        self.assertIsInstance(factor, float)
        
    def testSeaTankerFreightCarbonFactor(self):
        factor = carbon.FreightSeaTanker().get_factor({"GHGUnits": "kgCO2e"})
        self.assertAlmostEqual(factor, 0.00292, 8)
    
    def testCargoShipFreightCarbonEndToEnd(self):
        factor = carbon.cargo_ship_ghg(ghg_units="kgCO2e", ship_type="BulkCarrier", capacity=40000)
        self.assertIsInstance(factor, float)
        
    def testCargoShipFreightCarbonFactor(self):
        factor = carbon.FreightCargoShip().get_factor({"GHGUnits": "kgCO2e", "ShipType": "BulkCarrier",
                                                       "MinCapacity": 0, "CapacityUnit": "DWT"})
        self.assertAlmostEqual(factor, 0.02943, 8)
    
    def testMinCapacity(self):
        min_capacity = carbon.get_min_capacity("ChemicalTanker", "FreightSeaTanker", 206474)
        self.assertEqual(min_capacity, 20000, "Fails with largest size")
        min_capacity = carbon.get_min_capacity("ChemicalTanker", "FreightSeaTanker", 18457)
        self.assertEqual(min_capacity, 10000, "Fails with intermediate size")
        min_capacity = carbon.get_min_capacity("ChemicalTanker", "FreightSeaTanker", 300)
        self.assertEqual(min_capacity, 0, "Fails with smallest size")
        min_capacity = carbon.get_min_capacity("ChemicalTanker", "FreightSeaTanker", None)
        self.assertEqual(min_capacity, -1, "Fails with None")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()