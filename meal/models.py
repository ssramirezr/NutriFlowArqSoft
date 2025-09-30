from django.db import models
from django.contrib.auth.models import User
from preferences.models import Preferences

# Create your models here.
class Meal(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    calories = models.FloatField()
    protein = models.FloatField()
    carbs = models.FloatField()
    fat = models.FloatField()
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name

class MealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    plan_json = models.JSONField()

    def __str__(self):
        return f"Plan de {self.user.username} - {self.created_at.strftime('%Y-%m-%d')}"