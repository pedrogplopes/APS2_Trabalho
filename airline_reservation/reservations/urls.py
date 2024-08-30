from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_flights, name='search_flights'),
    path('reserve/<int:flight_id>/', views.make_reservation, name='make_reservation'),
]
