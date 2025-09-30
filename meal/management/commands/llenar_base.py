import json
from django.core.management.base import BaseCommand
from meal.models import Meal

class Command(BaseCommand):
    help = "Llena la base de datos con alimentos desde un archivo JSON."

    def handle(self, *args, **kwargs):
        try:
            with open("meal/management/commands/meals.json", "r", encoding="utf-8") as file:
                data = json.load(file)
            
            alimentos = data.get("alimentos", [])
            
            for item in alimentos:
                Meal.objects.get_or_create(
                    name=item["name"],
                    description=item["description"],
                    calories=item["calories"],
                    protein=item["protein"],
                    carbs=item["carbs"],
                    fat=item["fat"],
                    image=None  # Dejamos la imagen vacía
                )

            self.stdout.write(self.style.SUCCESS("Base de datos poblada con éxito."))
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error al llenar la base de datos: {e}"))
