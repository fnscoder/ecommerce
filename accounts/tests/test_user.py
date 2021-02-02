from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate

from accounts.models import User
from accounts.views import UserModelViewSet


class UserTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(is_active=True, is_staff=True)
        self.other_user = User.objects.create(is_active=True, is_staff=False)
        self.factory = APIRequestFactory()
        self.url = reverse('user-list')
        self.data = {
            'first_name': 'New First Name',
            'last_name': 'New Last Name'
        }

    def test_list_users(self):
        request = self.factory.get(self.url, format='json')
        view = UserModelViewSet.as_view({'get': 'list'})
        force_authenticate(request, self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['id'], str(self.user.pk))

    def test_retrieve_user(self):
        url = reverse('user-detail', kwargs={'pk': self.user.pk})
        request = self.factory.get(url, format='json')
        view = UserModelViewSet.as_view({'get': 'retrieve'})
        force_authenticate(request, self.user)
        response = view(request, pk=self.user.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.user.pk))

    def test_retrieve_user_not_logged(self):
        url = reverse('user-detail', kwargs={'pk': self.user.pk})
        request = self.factory.get(url, format='json')
        view = UserModelViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=self.user.pk)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_user(self):
        request = self.factory.patch(self.url, self.data, format='json')
        view = UserModelViewSet.as_view({'patch': 'partial_update'})
        force_authenticate(request, self.user)
        response = view(request, pk=self.user.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.user.pk))
        self.assertEqual(response.data['first_name'], self.data['first_name'])
        self.assertEqual(response.data['last_name'], self.data['last_name'])

    def test_delete_user(self):
        url = reverse('user-detail', kwargs={'pk': self.user.pk})
        request = self.factory.delete(url, format='json')
        view = UserModelViewSet.as_view({'delete': 'destroy'})
        force_authenticate(request, self.user)
        response = view(request, pk=self.user.pk)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 1)
