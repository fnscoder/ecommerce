from django.urls import path, include
from rest_framework.routers import SimpleRouter

from products.views import CategoryModelViewSet, ProductModelViewSet

router = SimpleRouter()

router.register('products', ProductModelViewSet, 'product')
router.register('categories', CategoryModelViewSet, 'category')

urlpatterns = [
    path('', include(router.urls)),
]
