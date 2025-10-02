import os
import json
import re
import openai
from dotenv import load_dotenv
from preferences.models import Preferences
from supermarket.models import Supermarket
from meal.models import MealPlan

class MealPlanFacade:
    """
    Proporciona una interfaz simple para el subsistema de generación de planes de comidas con IA.
    Encapsula toda la lógica de preparación de datos, construcción de prompts, 
    llamadas a la API y procesamiento de respuestas.
    """

    def __init__(self, user):
        self.user = user
        self.prefs = Preferences.objects.filter(user=user).first()

    def _load_api_key(self):
        """Carga la clave API de OpenAI desde un archivo .env."""
        load_dotenv() # Busca el archivo .env en el directorio del proyecto
        api_key = os.getenv("openai_apikey")
        if not api_key:
            raise ValueError("La clave API de OpenAI no está configurada en el archivo .env.")
        openai.api_key = api_key

    def _get_products_as_text(self):
        """Obtiene todos los productos del supermercado y los formatea como texto."""
        productos_disponibles = Supermarket.objects.all()
        productos_lista = ""
        for prod in productos_disponibles:
            productos_lista += (
                f"- {prod.nombre_producto} ({prod.marca_producto}): "
                f"{prod.calorias} kcal, {prod.proteinas}g proteínas, "
                f"{prod.carbohidratos}g carbohidratos, {prod.grasas}g grasas, "
                f"Precio: {prod.precio_producto}€, Supermercado: {prod.nombre_supermercado}\n"
            )
        return productos_lista

    def _build_prompt(self, productos_lista):
        """Construye el prompt completo para la API de OpenAI."""
        # (Aquí se pega toda la lógica de construcción de prompt_intro y prompt_json)
        prompt_intro = f"""...""" # El f-string gigante va aquí
        prompt_json = """...""" # El bloque de estructura JSON va aquí
        return prompt_intro + prompt_json

    def generate_plan(self):
        """
        Orquesta el proceso completo de generación de un plan de comidas.
        Retorna el plan de comidas o un diccionario de error.
        """
        if not self.prefs:
            return {'error': 'No has configurado tus preferencias nutricionales.'}

        try:
            self._load_api_key()
            productos_lista = self._get_products_as_text()
            
            # La lógica de construcción del prompt es compleja y se mantiene aquí
            # (Omitido por brevedad, pero es el mismo prompt gigante de la vista original)
            full_prompt = self._build_full_prompt(productos_lista)

            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Eres un nutricionista que crea planes alimenticios solo con productos reales y económicos."},
                    {"role": "user", "content": full_prompt}
                ],
                temperature=0.5,
                max_tokens=2000
            )

            json_text = self._parse_and_clean_response(response)
            meal_plan_data = json.loads(json_text)

            if not meal_plan_data.get("meals") or not meal_plan_data.get("shopping_list"):
                return {'error': "El plan generado no contiene datos completos. Intenta nuevamente."}

            MealPlan.objects.create(user=self.user, plan_json=meal_plan_data)
            
            alerta_presupuesto = self._calculate_budget_alert(meal_plan_data)

            return {'meal_plan_data': meal_plan_data, 'alerta_presupuesto': alerta_presupuesto}

        except Exception as e:
            return {'error': str(e)}

    def _build_full_prompt(self, productos_lista):
        # Esta es la lógica completa para construir el prompt, extraída de la vista.
        prompt_intro = f"""
Eres un nutricionista experto en planes de alimentación económica y saludable.

Crea un plan de comidas para un día (desayuno, snack 1, almuerzo, snack 2, cena) usando únicamente los productos de la siguiente lista:

{productos_lista}

Cada comida debe:
- Elegir productos con mejor relación costo/nutrición
- No superar el presupuesto disponible: {self.prefs.presupuesto} €
- Indicar cantidad, preparación y macronutrientes

El formato de salida debe ser estrictamente JSON...
""" # (El resto del prompt sigue aquí)
        prompt_json = """ 
{
  "meals": [...], ... 
}
""" # (El resto de la estructura JSON sigue aquí)
        return prompt_intro + prompt_json

    def _parse_and_clean_response(self, response):
        json_text = response['choices'][0]['message']['content'].strip()
        if not json_text:
            raise ValueError('La respuesta de OpenAI está vacía.')

        match = re.search(r'({.*})', json_text, re.DOTALL)
        if match:
            json_text = match.group(1)
        else:
            raise ValueError(f"La respuesta no contiene JSON reconocible: {json_text}")
        
        return json_text.replace('\"', '"').replace("\n", "").strip()

    def _calculate_budget_alert(self, meal_plan_data):
        total_usado = meal_plan_data["presupuesto"]["total_usado"]
        total_usuario = float(meal_plan_data["presupuesto"]["total_usuario"])
        porcentaje_usado = (total_usado / total_usuario) * 100

        if porcentaje_usado >= 80:
            color = "danger"
            mensaje = f"¡Cuidado! Estás usando el {porcentaje_usado:.2f}% de tu presupuesto."
        elif porcentaje_usado >= 50:
            color = "warning"
            mensaje = f"Atención: llevas usado el {porcentaje_usado:.2f}% de tu presupuesto."
        else:
            color = "success"
            mensaje = f"Presupuesto bajo control: solo has usado el {porcentaje_usado:.2f}%."

        return {
            "porcentaje": round(porcentaje_usado, 2),
            "color": color,
            "mensaje": mensaje
        }