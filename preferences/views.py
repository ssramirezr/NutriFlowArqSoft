from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Preferences  # Asegúrate de que tienes este modelo

def preferences_view(request):
    preferences = None
    calorias = None

    if request.user.is_authenticated:
        preferences = Preferences.objects.filter(user=request.user).first()

        if preferences:
            # Obtener valores
            peso = float(preferences.peso) if preferences.peso else 0
            altura = float(preferences.altura) if preferences.altura else 0
            edad = int(preferences.edad) if preferences.edad else 0
            genero = preferences.genero
            nivel_actividad = preferences.nivel_actividad

            # Calcular TMB
            if genero == 'M':
                tmb = 88.36 + (13.4 * peso) + (4.8 * altura) - (5.7 * edad)
            else:  # Femenino
                tmb = 447.6 + (9.2 * peso) + (3.1 * altura) - (4.3 * edad)

            # Aplicar factor de actividad
            factores_actividad = {
                "sedentario": 1.2,
                "ligero": 1.375,
                "moderado": 1.55,
                "activo": 1.725,
                "muy_activo": 1.9
            }
            calorias = tmb * factores_actividad.get(nivel_actividad, 1.2)

    return render(request, 'preferences.html', {
        'preferences': preferences,
        'calorias': round(calorias, 2) if calorias else None
    })


def save_preferences(request):
    if request.method == "POST":
        peso = float(request.POST.get("peso"))
        altura = float(request.POST.get("altura"))
        edad = int(request.POST.get("edad"))
        genero = request.POST.get("genero")
        nivel_actividad = request.POST.get("nivel_actividad")
        objetivo = request.POST.get("objetivo")
        presupuesto = float(request.POST.get("presupuesto", 0))
        alergias = request.POST.get("alergias", "")


        # Calcular requerimientos
        requerimientos = calcular_requerimientos(peso, altura, edad, genero, nivel_actividad, objetivo)

        # Buscar las preferencias existentes o crear nuevas
        preferences, created = Preferences.objects.get_or_create(
            user=request.user,  # Si tienes autenticación
            defaults={
                "peso": peso,
                "altura": altura,
                "edad": edad,
                "genero": genero,
                "nivel_actividad": nivel_actividad,
                "objetivo": objetivo,
                "presupuesto": presupuesto,
                "alergias": ",".join(alergias),  # Guarda alergias como texto separado por comas
                **requerimientos,  # Guarda calorías, proteínas, carbohidratos y grasas
            }
        )

        # Si ya existía, actualiza los valores
        if not created:
            preferences.peso = peso
            preferences.altura = altura
            preferences.edad = edad
            preferences.genero = genero
            preferences.nivel_actividad = nivel_actividad
            preferences.objetivo = objetivo
            preferences.presupuesto = presupuesto
            preferences.alergias = ",".join(alergias)
            preferences.calorias = requerimientos["calorias"]
            preferences.proteinas = requerimientos["proteinas"]
            preferences.carbohidratos = requerimientos["carbohidratos"]
            preferences.grasas = requerimientos["grasas"]
            preferences.save()

        return JsonResponse({
            "success": True,
            "message": "Preferencias guardadas correctamente",
            **requerimientos  # Devuelve calorías, proteínas, carbohidratos y grasas
        })

    return JsonResponse({"success": False, "error": "Método no permitido"}, status=400)

def calcular_requerimientos(peso, altura, edad, genero, nivel_actividad, objetivo):
    if genero == "male":
        tmb = 88.36 + (13.4 * peso) + (4.8 * altura) - (5.7 * edad)
    else:
        tmb = 447.6 + (9.2 * peso) + (3.1 * altura) - (4.3 * edad)

    actividad_factor = {
        "sedentario": 1.2,
        "ligero": 1.375,
        "moderado": 1.55,
        "activo": 1.725,
        "muy_activo": 1.9
    }

    calorias_mantenimiento = tmb * actividad_factor.get(nivel_actividad, 1.2)

    if objetivo == "lose_weight":
        calorias = calorias_mantenimiento - 500
    elif objetivo == "gain_weight":
        calorias = calorias_mantenimiento + 500
    else:
        calorias = calorias_mantenimiento

    proteinas = (0.3 * calorias) / 4
    carbohidratos = (0.5 * calorias) / 4
    grasas = (0.2 * calorias) / 9

    return {
        "calorias": round(calorias, 2),
        "proteinas": round(proteinas, 2),
        "carbohidratos": round(carbohidratos, 2),
        "grasas": round(grasas, 2)
    }
