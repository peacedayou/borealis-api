from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BorealisDatasetViewSet

router = DefaultRouter()
router.register(r'borealis', BorealisDatasetViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
