from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase

from accounts.views import RegisterAPIView


class RegisterTestCase(APITestCase):
    def test_register_user(self):
        data = {
            "first_name": "User",
            "last_name": "Test",
            "email": "user@test.com",
            "password": "secret",
        }
        url = reverse('register')
        factory = APIRequestFactory()
        request = factory.post(url, data=data, format='json')
        view = RegisterAPIView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data['auth_token'])
        self.assertEqual(response.data['first_name'], data['first_name'])

    def test_register_user_without_password(self):
        data = {"email": "my@email.com"}
        url = reverse('register')
        factory = APIRequestFactory()
        request = factory.post(url, data=data, format='json')
        view = RegisterAPIView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_invalid_email(self):
        data = {"email": "email"}
        url = reverse('register')
        factory = APIRequestFactory()
        request = factory.post(url, data=data, format='json')
        view = RegisterAPIView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_without_email(self):
        data = {"name": "name"}
        url = reverse('register')
        factory = APIRequestFactory()
        request = factory.post(url, data=data, format='json')
        view = RegisterAPIView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
