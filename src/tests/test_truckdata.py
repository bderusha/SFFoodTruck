import unittest
from unittest.mock import patch
from truckdata import TruckData


class TestTruckData(unittest.TestCase):
    def test_expected_columns(self):
        self.assertListEqual(list(TruckData().data.columns), [
                TruckData.APPLICANT,
                TruckData.ADDRESS, 
                TruckData.STATUS, 
                TruckData.FOOD_ITEMS, 
                TruckData.LATITUDE, 
                TruckData.LONGITUDE,
                TruckData.DISTANCE
            ])

if __name__ == '__main__':
    unittest.main()