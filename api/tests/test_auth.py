from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse

class APITestsWithoutLogin(TestCase):
    def setUp(self):
        self.client = APIClient(enforce_csrf_checks=True)
        self.measurement_url = reverse('aqimeasurement-list') 
        self.standard_url = reverse('aqistandard-list')
        self.point_url = reverse('aqipoint-list') 

    def test_post_measurement_without_login(self):
        data = {
            'lon': 10,
            'lat': 10,
            'pollution': 50,
            'noise': 40
        }
        response = self.client.post(self.measurement_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_standard_without_login(self):
        data = {
            'lower_limit': 0,
            'upper_limit': 50,
            'description': 'Medium'
        }
        response = self.client.post(self.standard_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_point_without_login(self):
        data = {
            'coordinates': 'POINT(10 10)'
        }
        response = self.client.post(self.point_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)