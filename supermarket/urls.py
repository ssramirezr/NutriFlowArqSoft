from django.urls import path
from . import views

urlpatterns = [
    path('', views.vista_supermercado, name='supermarket'),
    path('buscar_productos/', views.buscar_productos, name='buscar_productos'),
]