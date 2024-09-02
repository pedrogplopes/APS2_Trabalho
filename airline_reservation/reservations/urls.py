from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.search_flights, name='search_flights'),
    path('reserve/<int:flight_id>/', views.make_reservation, name='make_reservation'),
    path('payment/', views.payment, name='payment'),
    path('my_reservations/', views.my_reservations, name='my_reservations'),
    path('cancel_reservation/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),
]