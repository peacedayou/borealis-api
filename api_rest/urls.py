from django.urls import path, include
from harvest.urls import urlpatterns as harvest_urls

urlpatterns = [
    path('', include(harvest_urls)),
]
