from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from api.models import AQIPoint, AQIMeasurement, AQIStandard
from django.urls import reverse
from django.contrib.auth.models import User

import os


class StandardTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(os.environ.get('DJANGO_SUPERUSER_USERNAME'), os.environ.get('DJANGO_SUPERUSER_PASSWORD'))
        self.client = APIClient(enforce_csrf_checks=True)
        self.client.force_authenticate(self.user)
        self.url = reverse('aqistandard-list')
        data = {
            'lower_limit': 151,
            'upper_limit': 500,
            'description': 'High'
        }
        response = self.client.post(self.url, data, format='json')
        self.standard = AQIStandard.objects.get(id=response.data['id'])
        

    def test_create_standard(self):
        data = {
            'lower_limit': 0,
            'upper_limit': 20,
            'description': 'Low'
        }
        response = self.client.post(self.url, data, format='json')
        self.standard = AQIStandard.objects.get(id=response.data['id'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AQIStandard.objects.count(), 2)

    def test_get_standard_by_id(self):
        url_id = reverse('aqistandard-detail', kwargs={'pk': self.standard.id})
        response = self.client.get(url_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], self.standard.description)

    def test_get_standard_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_standard(self):
        data = {
            'lower_limit': 20,
            'upper_limit': 50,
            'description': 'Medium'
        }
        url_id = reverse('aqistandard-detail', kwargs={'pk': self.standard.id})
        response = self.client.put(url_id, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.standard.refresh_from_db()
        self.assertEqual(self.standard.description, 'Medium')
        self.assertEqual(self.standard.lower_limit, 20)
        self.assertEqual(self.standard.upper_limit, 50)

    def test_patch_standard(self):
        url_id = reverse('aqistandard-detail', kwargs={'pk': self.standard.id})

        response = self.client.patch(url_id, {
            'description': 'Medium Patch'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.standard.refresh_from_db()
        self.assertEqual(self.standard.description, 'Medium Patch')

        response = self.client.patch(url_id, {
            'lower_limit': 10
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.standard.refresh_from_db()
        self.assertEqual(self.standard.lower_limit, 10)

        response = self.client.patch(url_id, {
            'upper_limit': 60
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.standard.refresh_from_db()
        self.assertEqual(self.standard.upper_limit, 60)

    def test_delete_standard(self):
        url_id = reverse('aqistandard-detail', kwargs={'pk': self.standard.id})
        response = self.client.delete(url_id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(AQIStandard.objects.count(), 0)

class MeasurementTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(os.environ.get('DJANGO_SUPERUSER_USERNAME'), os.environ.get('DJANGO_SUPERUSER_PASSWORD'))
        self.client = APIClient(enforce_csrf_checks=True)
        self.client.force_authenticate(self.user)
        self.url = reverse('aqimeasurement-list')
        data = {
            'lon': 10,
            'lat': 10,
            'pollution': 50,
            'noise': 20
        }
        response = self.client.post(self.url, data, format='json')
        self.measurement = AQIMeasurement.objects.get(id=response.data['data']['id'])
        

    def test_create_measurement(self):

        data = {
            'lon': 15,
            'lat': 15,
            'pollution': 25, 
            'noise': 25
        }
        response = self.client.post(self.url, data, format='json')
        self.measurement = AQIMeasurement.objects.get(id=response.data['data']['id'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AQIMeasurement.objects.count(), 2)
        self.assertEqual(AQIMeasurement.objects.get(id=self.measurement.id).pollution, 25)

    def test_get_measurement_by_id(self):
        url_id = reverse('aqimeasurement-detail', kwargs={'pk': self.measurement.id})
        response = self.client.get(url_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['pollution'], self.measurement.pollution)

    def test_get_measurement_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_measurement(self):
        data = {
            'lon': 15,
            'lat': 15,
            'pollution': 80,
            'noise': 70
        }
        url_id = reverse('aqimeasurement-detail', kwargs={'pk': self.measurement.id})
        response = self.client.put(url_id, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.measurement.refresh_from_db()
        self.assertEqual(self.measurement.pollution, 80)

    def test_patch_measurement(self):
        url_id = reverse('aqimeasurement-detail', kwargs={'pk': self.measurement.id})
        data = {
            'pollution': 85
        }
        response = self.client.patch(url_id, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.measurement.refresh_from_db()
        self.assertEqual(self.measurement.pollution, 85)

    def test_delete_measurement(self):
        url_id = reverse('aqimeasurement-detail', kwargs={'pk': self.measurement.id})
        response = self.client.delete(url_id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(AQIMeasurement.objects.count(), 0)



class PointTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(os.environ.get('DJANGO_SUPERUSER_USERNAME'), os.environ.get('DJANGO_SUPERUSER_PASSWORD'))
        self.client = APIClient(enforce_csrf_checks=True)
        self.client.force_authenticate(self.user)
        self.url = reverse('aqipoint-list')
        data = {
            'coordinates': 'SRID=4326;POINT(30 40)'
        }
        response = self.client.post(self.url, data, format='json')
        self.point = AQIPoint.objects.get(id=response.data['id'])

    def test_create_point(self):
        data = {
            'coordinates': 'SRID=4326;POINT(30 40)'
        }
        response = self.client.post(self.url, data)
        self.point = AQIPoint.objects.get(id=response.data['id'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AQIPoint.objects.count(), 2)

    def test_get_point_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_point_by_id(self):
        url_id = reverse('aqipoint-detail', kwargs={'pk': self.point.id})
        response = self.client.get(url_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.point.id)

    def test_update_point(self):
        data = {
            'coordinates': 'SRID=4326;POINT(40 50)'
        }
        url_id = reverse('aqipoint-detail', kwargs={'pk': self.point.id})
        response = self.client.put(url_id, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.point.refresh_from_db()
        self.assertEqual(self.point.coordinates, 'SRID=4326;POINT(40 50)')

    def test_patch_point(self):
        data = {
            'coordinates': 'SRID=4326;POINT(400 500)'
        }
        url_id = reverse('aqipoint-detail', kwargs={'pk': self.point.id})
        response = self.client.patch(url_id, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.point.refresh_from_db()
        self.assertEqual(self.point.coordinates, 'SRID=4326;POINT(400 500)')

    def test_delete_point(self):
        url_id = reverse('aqipoint-detail', kwargs={'pk': self.point.id})
        response = self.client.delete(url_id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(AQIPoint.objects.count(), 0)


