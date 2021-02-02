from django.urls import path, include
from rest_framework.routers import SimpleRouter

from products.views import ProductModelViewSet

router = SimpleRouter()

router.register('products', ProductModelViewSet, 'product')

urlpatterns = [
    path('', include(router.urls)),
]
