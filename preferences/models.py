from django.db import models
from django.contrib.auth.models import User

class Preferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    genero = models.CharField(max_length=10, choices=[("male", "Hombre"), ("female", "Mujer")])
    objetivo = models.CharField(max_length=20, choices=[("lose_weight", "Bajar de peso"), ("improve_health", "Mejorar salud"), ("gain_weight", "Subir de peso")])
    edad = models.IntegerField()
    peso = models.FloatField()
    altura = models.FloatField()
    nivel_actividad = models.CharField(max_length=20, choices=[("sedentario", "Sedentario"), ("ligero", "Ligero"), ("moderado", "Moderado"), ("activo", "Activo"), ("muy_activo", "Muy Activo")])
    presupuesto = models.FloatField()
    alergias = models.TextField(blank=True, null=True)

    # Nuevos campos para los requerimientos nutricionales
    calorias = models.FloatField(default=0)
    proteinas = models.FloatField(default=0)
    carbohidratos = models.FloatField(default=0)
    grasas = models.FloatField(default=0)

    def __str__(self):
        return f'Preferencias de {self.user.username}'