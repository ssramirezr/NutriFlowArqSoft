from django.urls import path
from . import views
from accounts.views import profile_view

urlpatterns = [
    path('', views.preferences_view, name='preferences'),
    path('save-preferences/', views.save_preferences, name='save_preferences'),
    path('perfil/', profile_view, name='profile')

]
