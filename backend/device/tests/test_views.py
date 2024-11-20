import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from device.models import Device, DeviceGroup, DeviceData, DeviceAuditLog, Notification

from user.models import User


class DeviceAPITestCase(APITestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            email="test@gmail.com",
            phone="09123456789",
            username='testuser',
            first_name="abcd",
            last_name="efgh",
            password='testpass',
        )
        self.client = APIClient()
        self.login = reverse("user:access")

    def test_create_device(self):
        # Log in to get the access token
        login_response = self.client.post(self.login, {'email': 'test@gmail.com', 'password': 'testpass'}, format='json')
        
        # Check if login was successful and extract the token
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        json_login = json.loads(login_response.content)
        token = json_login["access"]
        
        # Prepare to create a device
        url = reverse('device:device-list-create')
        data = {'name': 'New Device', 'type': 1, 'status': True}
        
        # Correctly pass the authorization header without extra spaces
        response = self.client.post(url, data, HTTP_AUTHORIZATION=f"Bearer {token}", format='json')
        
        # Check if device creation was successful
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
