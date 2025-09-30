from django.db import models

# Crear tus modelos aquí.
class Supermarket(models.Model):
    nombre_supermercado = models.CharField(max_length=100)
    nombre_producto = models.CharField(max_length=100)
    marca_producto = models.CharField(max_length=100)
    precio_producto = models.FloatField()
    calorias = models.FloatField()
    proteinas = models.FloatField()
    carbohidratos = models.FloatField()
    grasas = models.FloatField()
    imagen = models.ImageField(upload_to='images/', default='images/default_image.jpg')

    def __str__(self):
        return f"{self.nombre_producto} ({self.marca_producto}) - {self.nombre_supermercado}"
