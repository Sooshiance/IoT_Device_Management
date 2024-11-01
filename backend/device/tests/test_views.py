from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from device.models import Device, DeviceGroup, DeviceData, DeviceAuditLog, Notification

from user.models import User


class DeviceAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@gmail.com",
                                             phone="09123456789",
                                             username="username",
                                             first_name="abcde",
                                             last_name="fgh",
                                             password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.device = Device.objects.create(user=self.user, name='Test Device', type='sensor')

    def test_create_device(self):
        url = reverse('device-list-create')
        data = {'name': 'New Device', 'type': 'sensor', 'status': True}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_device_list(self):
        url = reverse('device-list-create')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_device_detail(self):
        url = reverse('device-detail', args=[self.device.did])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_device(self):
        url = reverse('device-detail', args=[self.device.did])
        data = {'name': 'Updated Device'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.device.refresh_from_db()
        self.assertEqual(self.device.name, 'Updated Device')

    def test_delete_device(self):
        url = reverse('device-detail', args=[self.device.did])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class DeviceGroupAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@gmail.com",
                                             phone="09123456789",
                                             username="username2",
                                             first_name="abcde",
                                             last_name="fghij",
                                             password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.device_group = DeviceGroup.objects.create(user=self.user, name='Test Group')

    def test_create_device_group(self):
        url = reverse('device-group-list-create')
        data = {'name': 'New Group'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_device_group_list(self):
        url = reverse('device-group-list-create')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_device_group_detail(self):
        url = reverse('device-group-detail', args=[self.device_group.gid])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_device_group(self):
        url = reverse('device-group-detail', args=[self.device_group.gid])
        data = {'name': 'Updated Group'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.device_group.refresh_from_db()
        self.assertEqual(self.device_group.name, 'Updated Group')

    def test_delete_device_group(self):
        url = reverse('device-group-detail', args=[self.device_group.gid])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class NotificationAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@gmail.com",
                                             phone="09123456789",
                                             username="username3",
                                             first_name="abcde",
                                             last_name="fghij",
                                             password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.notification = Notification.objects.create(user=self.user, message='Test Notification')

    def test_create_notification(self):
        url = reverse('notification-list-create')
        data = {'message': 'New Notification'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_notifications(self):
        url = reverse('notification-list-create')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_mark_notification_as_read(self):
        url = reverse('notification-mark-as-read', args=[self.notification.nid])
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.is_read)
