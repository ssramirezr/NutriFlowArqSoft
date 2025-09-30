from django.shortcuts import render, redirect
from preferences.models import Preferences
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


# Create your views here.

def home(request):

    return render(request, 'home.html') 

def signupaccount(request):

    return render(request, 'signupaccount.html')

def loginaccount(request):
    return render(request, 'loginaccount.html')

def logoutaccount(request):
    return render(request, 'logoutaccount.html')


@login_required
def user_preferences(request):
    if request.method == "POST":
        genero = request.POST.get("genero")
        objetivo = request.POST.get("objetivo")
        edad = request.POST.get("edad")
        peso = request.POST.get("peso")
        altura = request.POST.get("altura")
        nivel_actividad = request.POST.get("nivel_actividad")
        presupuesto = request.POST.get("presupuesto")
        alergias = request.POST.get("alergias")

        # Intentamos obtener las preferencias del usuario, si no existen, las creamos
        preferences, created = preferences.objects.get_or_create(user=request.user)
        preferences.genero = genero
        preferences.objetivo = objetivo
        preferences.edad = edad
        preferences.peso = peso
        preferences.altura = altura
        preferences.nivel_actividad = nivel_actividad
        preferences.presupuesto = presupuesto
        preferences.alergias = alergias
        preferences.save()

        return redirect("home")  # Redirige a la página principal o donde quieras

    return render(request, "meal/preferences.html")
