from django.db import models
from django.contrib.auth.models import User

class Preferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="account_preferences")  # 👈 Diferencia este modelo
    genero = models.CharField(max_length=10)
    objetivo = models.CharField(max_length=50)
    edad = models.IntegerField()
    peso = models.FloatField()
    altura = models.FloatField()
    nivel_actividad = models.CharField(max_length=20)
    presupuesto = models.FloatField()
    alergias = models.TextField(blank=True, null=True)  # Puede estar vacío

    def __str__(self):
        return f"Preferencias de {self.user.username}"
    
class DailyLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    calorias = models.IntegerField(default=0)
    proteinas = models.IntegerField(default=0)
    carbohidratos = models.IntegerField(default=0)
    grasas = models.IntegerField(default=0)

