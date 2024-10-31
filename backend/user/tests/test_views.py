from django.urls import reverse

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from user.models import (User,
                         Profile,
                         OTP)


class TestRegister(APITestCase):
    def setUp(self) -> None:
        self.credentials = {
            "phone":"09123456789",
            "email":"test321@gmail.com",
            "username":"test_user",
            "password":"mnbvcxz#09876543210",
            "first_name":"ben",
            "last_name":"web",
        }
        self.register = reverse("user:register")
        self.client = APIClient()
    
    def test_registerUser(self):
        response = self.client.post(self.register, data=self.credentials)
        self.assertEqual(response.status_code, 201)


class TestProfile(APITestCase):
    def setUp(self) -> None:
        self.credentials = {
            "phone":"09123456789",
            "email":"test321@gmail.com",
            "username":"test_user",
            "password":"mnbvcxz#09876543210",
            "first_name":"ben",
            "last_name":"web",
        }
        
        self.client = APIClient()
        
        self.user = User.objects.create_user(**self.credentials)
        
        self.access_token = reverse("user:access")
        self.profile = reverse("user:profile")
    
    def login(self):
        response = self.client.post(self.access_token, data={
            "email": self.credentials["email"],
            "password": self.credentials["password"],
            })
        
        access_token = response.data["access"]
        # Set the token in the header
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    
    def test_get_profile(self):
        self.login()

        profile_response = self.client.get(self.profile)

        self.assertEqual(profile_response.status_code, 200)
    
    # TODO: You can add more scenarios
    def test_update_profile(self):
        self.login()
    
    # TODO: You can add more scenarios
    def test_delete_profile(self):
        self.login()


class TestPasswordReset(APITestCase):
    def setUp(self) -> None:
        self.credentials = {
            "phone":"09123456789",
            "email":"test321@gmail.com",
            "username":"test_user",
            "password":"mnbvcxz#09876543210",
            "first_name":"ben",
            "last_name":"web",
        }
        
        self.client = APIClient()
        
        self.user = User.objects.create_user(**self.credentials).save()

        self.otp = reverse("user:otp")
        self.reset = reverse("user:reset")
