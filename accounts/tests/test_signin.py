from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory

from accounts.models import User
from accounts.views import SignInAPIView


class SignInTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="user@test.com")
        self.user.set_password('secret')
        self.user.save()
        self.url = reverse('login')
        self.factory = APIRequestFactory()

    def test_sign_in_user(self):
        data = {
            "email": "user@test.com",
            "password": "secret"
        }
        request = self.factory.post(self.url, data=data, format='json')
        view = SignInAPIView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)

    def test_sign_in_empty_password(self):
        data = {
            "email": "user@test.com",
            "password": ""
        }
        request = self.factory.post(self.url, data=data, format='json')
        view = SignInAPIView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['password'][0], 'This field may not be blank.')

    def test_sign_in_empty_email(self):
        data = {
            "email": "",
            "password": "secret"
        }
        request = self.factory.post(self.url, data=data, format='json')
        view = SignInAPIView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'][0], 'This field may not be blank.')

    def test_sign_in_wrong_password(self):
        data = {
            "email": "user@test.com",
            "password": "wrong_password"
        }
        request = self.factory.post(self.url, data=data, format='json')
        view = SignInAPIView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0], 'Unable to log in with provided credentials.')
