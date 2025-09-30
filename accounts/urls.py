from django.urls import path
from . import views
from meal import views as mealViews
from django.conf import settings
from django.conf.urls.static import static
from .views import profile_view

urlpatterns = [
    path('signupaccount/', views.signupaccount, name='signupaccount'),
    path('home/', mealViews.home, name='home'),
    path('loginaccount/', views.loginaccount, name='loginaccount'),
    path('logout/', views.logoutaccount, name='logoutaccount'),
    path('perfil/', profile_view, name='perfil'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)