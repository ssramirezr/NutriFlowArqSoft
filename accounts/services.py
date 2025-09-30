from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest
from django.contrib.auth.models import User


class AuthService:
    """
    Singleton para manejar la autenticación y cierre de sesión de usuarios.
    Evita instancias duplicadas y centraliza la lógica de autenticación.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AuthService, cls).__new__(cls)
        return cls._instance

    def login_user(self, request: HttpRequest, username: str, password: str) -> User | None:
        """
        Autentica y registra la sesión de un usuario existente.

        Args:
            request: Objeto HttpRequest actual.
            username: Nombre de usuario.
            password: Contraseña.

        Returns:
            El objeto User si la autenticación fue exitosa, None si falló.
        """
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return user
        return None

    def logout_user(self, request: HttpRequest) -> None:
        """
        Cierra la sesión del usuario actual.

        Args:
            request: Objeto HttpRequest actual.
        """
        logout(request)
