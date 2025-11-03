from django.urls import path
from .views import stats_view, home_view, moissonner_view, borealis_view

urlpatterns = [
    path('', home_view, name='home'),
    path('stats/', stats_view, name='stats'),  # si déjà défini
    path('moissonner/', moissonner_view, name='moissonner'),
    path('borealis/', borealis_view, name='borealis'),

]
