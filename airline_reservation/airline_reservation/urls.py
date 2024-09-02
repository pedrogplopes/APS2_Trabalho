from django.contrib import admin
from django.urls import path, include
from reservations import views  # Certifique-se de que este import está correto

urlpatterns = [
    path('admin/', admin.site.urls),
    path('reservations/', include('reservations.urls')),
    path('', views.home, name='home'),  # Redireciona a URL raiz para a view home
]
