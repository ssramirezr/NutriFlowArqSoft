from django.contrib import admin

from meal.models import Meal, MealPlan

# Register your models here.
admin.site.register(Meal)
admin.site.register(MealPlan)

