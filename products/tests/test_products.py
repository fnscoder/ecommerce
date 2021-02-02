from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from accounts.models import User
from products.models import Product
from products.views import ProductModelViewSet


class ProductsModelViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='john@card.com', first_name='John', last_name='Lennon')
        self.product = Product.objects.create(
            name='guitar',
            description='Guitar Les Paul',
            price=1500,
            quantity=2,
            owner=self.user
        )
        self.list_url = reverse('product-list')
        self.detail_url = reverse('product-detail', kwargs={'pk': self.product.pk})
        self.data = {
            'description': 'New product description',
            'name': 'New product name',
            'price': 199,
            'quantity': 10
        }
        self.factory = APIRequestFactory()

    def test_create_product(self):
        request = self.factory.post(self.list_url, self.data, format='json')
        view = ProductModelViewSet.as_view({'post': 'create'})
        force_authenticate(request, self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['owner']['id'], str(self.user.id))
        self.assertEqual(response.data['name'], 'New product name')
        self.assertEqual(response.data['description'], 'New product description')

    def test_list_products(self):
        request = self.factory.post(self.list_url, self.data, format='json')
        view = ProductModelViewSet.as_view({'post': 'create'})
        force_authenticate(request, self.user)
        response = view(request)

        request = self.factory.get(self.list_url)
        view = ProductModelViewSet.as_view({'get': 'list'})
        force_authenticate(request, self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(Product.objects.all().count(), 2)

    def test_update_product(self):
        request = self.factory.patch(self.detail_url, self.data, format='json')
        view = ProductModelViewSet.as_view({'patch': 'partial_update'})
        force_authenticate(request, self.user)
        response = view(request, pk=self.product.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.product.id)
        self.assertEqual(response.data['name'], self.data['name'])

    def test_delete_product(self):
        self.assertEqual(Product.objects.all().count(), 1)
        request = self.factory.delete(self.detail_url, format='json')
        view = ProductModelViewSet.as_view({'delete': 'destroy'})
        force_authenticate(request, self.user)
        response = view(request, pk=self.product.pk)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.all().count(), 0)
