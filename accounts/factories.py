from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpRequest


class UserFactory:
    """
    Factory Method para manejar la creación y autenticación de usuarios.
    Separa la lógica del modelo User de las vistas, favoreciendo la reutilización y testeo.
    """

    @staticmethod
    def create_user(request: HttpRequest, username: str, password: str) -> User:
        """
        Crea un nuevo usuario y lo autentica inmediatamente.

        Args:
            request: Objeto HttpRequest actual.
            username: Nombre de usuario deseado.
            password: Contraseña del usuario.

        Returns:
            El objeto User recién creado y autenticado.

        Raises:
            ValueError: Si los campos son inválidos.
            IntegrityError: Si el nombre de usuario ya existe.
        """
        if not username or not password:
            raise ValueError("El nombre de usuario y la contraseña son obligatorios.")

        try:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return user
        except IntegrityError:
            raise IntegrityError("El nombre de usuario ya está en uso.")

    @staticmethod
    def authenticate_user(request: HttpRequest, username: str, password: str) -> User | None:
        """
        Autentica un usuario existente.

        Args:
            request: Objeto HttpRequest actual.
            username: Nombre de usuario.
            password: Contraseña.

        Returns:
            El objeto User si la autenticación es exitosa, None en caso contrario.
        """
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return user
        return None

    @staticmethod
    def logout_user(request: HttpRequest) -> None:
        """
        Cierra la sesión del usuario actual.
        """
        logout(request)
