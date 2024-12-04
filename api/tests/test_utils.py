from django.test import TestCase
from math import isclose
from api.utils import calculate_length

class UtilsTests(TestCase):
    
    def test_calculate_length(self):
        
        long_start = -74.005974  
        lat_start = 40.712776    
        long_end = -118.243683   
        lat_end = 34.052235      
        
        expected_distance = 3936.536
        
        calculated_distance = calculate_length(long_start, lat_start, long_end, lat_end)
        
        self.assertTrue(isclose(calculated_distance, expected_distance, rel_tol=0.01), 
                        f"Expected {expected_distance}, got {calculated_distance}")
