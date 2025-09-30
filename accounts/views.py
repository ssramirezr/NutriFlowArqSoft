from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from preferences.models import Preferences
from .factories import UserFactory
from .services import AuthService


def signupaccount(request):
    """
    Vista para registrar un nuevo usuario usando el Factory Method y validaciones de Django.
    """
    if request.method == 'GET':
        form = UserCreationForm()
        return render(request, 'signupaccount.html', {'form': form})

    # POST
    form = UserCreationForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')

        try:
            # Crea y autentica el usuario con el Factory
            UserFactory.create_user(request, username=username, password=password)
            return redirect('home')
        except IntegrityError:
            form.add_error('username', 'El nombre de usuario ya está en uso.')
        except ValueError as e:
            form.add_error(None, str(e))

    # Si el formulario no es válido, Django mostrará automáticamente los errores de contraseña
    return render(request, 'signupaccount.html', {'form': form})


def loginaccount(request):
    """
    Vista para iniciar sesión. Usa AuthService (Singleton) para centralizar autenticación.
    """
    if request.method == 'GET':
        return render(request, 'loginaccount.html', {'form': AuthenticationForm()})

    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        auth_service = AuthService()
        user = auth_service.login_user(request, username, password)

        if user:
            return redirect('home')

    # Si falla la autenticación, muestra mensaje de error
    return render(request, 'loginaccount.html', {
        'form': form,
        'error': 'El usuario o la contraseña no coinciden.'
    })


@login_required
def logoutaccount(request):
    """
    Cierra la sesión del usuario actual.
    """
    auth_service = AuthService()
    auth_service.logout_user(request)
    return redirect('home')


@login_required
def profile_view(request):
    """
    Muestra el perfil del usuario y sus preferencias nutricionales.
    """
    preferences = Preferences.objects.filter(user=request.user).first()

    if not preferences:
        return render(request, 'account.html', {'no_preferences': True})

    # 🔹 Datos de ejemplo (temporal)
    calorias_consumidas = 400
    proteinas_consumidas = 50
    carbohidratos_consumidos = 90
    grasas_consumidas = 17

    def porcentaje(actual, objetivo):
        return min(round((actual / objetivo) * 100, 2), 100) if objetivo > 0 else 0

    context = {
        'no_preferences': False,
        'preferences': preferences,
        'calorias_consumidas': calorias_consumidas,
        'proteinas_consumidas': proteinas_consumidas,
        'carbohidratos_consumidos': carbohidratos_consumidos,
        'grasas_consumidas': grasas_consumidas,
        'porcentaje_calorias': porcentaje(calorias_consumidas, preferences.calorias),
        'porcentaje_proteinas': porcentaje(proteinas_consumidas, preferences.proteinas),
        'porcentaje_carbohidratos': porcentaje(carbohidratos_consumidos, preferences.carbohidratos),
        'porcentaje_grasas': porcentaje(grasas_consumidas, preferences.grasas),
    }

    return render(request, 'account.html', context)
