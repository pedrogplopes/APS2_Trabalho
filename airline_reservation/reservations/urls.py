from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # URL para a home
    path('search_flights/', views.search_flights, name='search_flights'),
    path('make_reservation/', views.make_reservation, name='make_reservation'),
]
