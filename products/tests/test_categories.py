from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from accounts.models import User
from products.models import Category, Product
from products.views import CategoryModelViewSet


class CategoriesModelViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='john@card.com', first_name='John', last_name='Lennon')
        self.category = Category.objects.create(name='music')
        self.product = Product.objects.create(
            category=self.category,
            name='guitar',
            description='Guitar Les Paul',
            price=1500,
            quantity=2,
            owner=self.user
        )
        self.list_url = reverse('category-list')
        self.detail_url = reverse('category-detail', kwargs={'pk': self.category.pk})
        self.data = {'name': 'New category'}
        self.factory = APIRequestFactory()

    def test_create_category(self):
        request = self.factory.post(self.list_url, self.data, format='json')
        view = CategoryModelViewSet.as_view({'post': 'create'})
        force_authenticate(request, self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New category')

    def test_list_categories(self):
        request = self.factory.post(self.list_url, self.data, format='json')
        view = CategoryModelViewSet.as_view({'post': 'create'})
        force_authenticate(request, self.user)
        response = view(request)

        request = self.factory.get(self.list_url)
        view = CategoryModelViewSet.as_view({'get': 'list'})
        force_authenticate(request, self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(Category.objects.all().count(), 2)

    def test_update_category(self):
        request = self.factory.patch(self.detail_url, self.data, format='json')
        view = CategoryModelViewSet.as_view({'patch': 'partial_update'})
        force_authenticate(request, self.user)
        response = view(request, pk=self.category.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.category.id)
        self.assertEqual(response.data['name'], self.data['name'])

    def test_delete_category(self):
        self.assertEqual(Category.objects.all().count(), 1)
        request = self.factory.delete(self.detail_url, format='json')
        view = CategoryModelViewSet.as_view({'delete': 'destroy'})
        force_authenticate(request, self.user)
        response = view(request, pk=self.category.pk)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.all().count(), 0)
