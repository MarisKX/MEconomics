"""
Tests for recipe APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from citizens.models import (
    Citizen,
)

from citizens.serializers import (
    CitizenSerializer,
    CitizenDetailSerializer,
)


CITIZENS_URL = reverse('citizens:citizen-list')


def detail_url(citizen_id):
    """Create and return a citizen detail URL"""
    return reverse('citizens:citizen-detail', args=[citizen_id])


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


def create_citizen(**params):
    """Create and return a sample ciztizen"""
    defaults = {
        'first_name': 'Jānis',
        'last_name': 'Bērziņš',
        'street_adress_1': 25,
        'street_adress_2': 'Erasplaats',
        'city': 'Riverside',
        'post_code': '1001AA',
        'country': 'Minecraft Kingdom',
    }
    defaults.update(params)

    citizen = Citizen.objects.create(**defaults)
    return citizen


class PublicRecipeAPITests(TestCase):
    """Test unauthenticated API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API"""
        res = self.client.get(CITIZENS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    """Test authenticated API requests"""
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='pass123')
        self.client.force_authenticate(self.user)

    def test_retrieve_citizens(self):
        """Test retrieving a list of citizens"""
        create_citizen()
        create_citizen()

        res = self.client.get(CITIZENS_URL)

        citizens = Citizen.objects.all().order_by('id')
        serializer = CitizenSerializer(citizens, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_citizen_detail(self):
        """Test get citizen detail"""
        citizen = create_citizen()

        url = detail_url(citizen.id)
        res = self.client.get(url)

        serializer = CitizenDetailSerializer(citizen)
        self.assertEqual(res.data, serializer.data)

    def test_create_citizen(self):
        """Test creating a citizen"""
        payload = {
            'first_name': 'Jānis',
            'last_name': 'Bērziņš',
            'street_adress_1': 25,
            'street_adress_2': 'Erasplaats',
            'city': 'Riverside',
            'post_code': '1001AA',
            'country': 'Minecraft Kingdom',
        }
        res = self.client.post(CITIZENS_URL, payload)

        citizen = Citizen.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(citizen, k), v)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
