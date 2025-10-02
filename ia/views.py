from django.shortcuts import render, redirect
from django.urls import reverse
from .services import MealPlanFacade

def generate_meal_plan(request):
    """
    Gestiona la solicitud para generar un nuevo plan de comidas.
    Utiliza MealPlanFacade para orquestar la lógica de negocio.
    """
    if request.method == 'POST':
        # Limpiar datos de sesión anteriores
        if 'meal_plan_data' in request.session:
            del request.session['meal_plan_data']
        if 'alerta_presupuesto' in request.session:
            del request.session['alerta_presupuesto']

        # Instanciar y usar la fachada para encapsular la complejidad
        facade = MealPlanFacade(request.user)
        result = facade.generate_plan()

        # Comprobar el resultado de la fachada
        if 'error' in result:
            return render(request, 'meal_plan_result.html', {'error': result['error']})
        
        # Si todo fue exitoso, guardar los datos en la sesión
        request.session['meal_plan_data'] = result['meal_plan_data']
        request.session['alerta_presupuesto'] = result['alerta_presupuesto']

        # Redirigir a la vista que muestra los resultados
        return redirect(reverse('mostrar_plan_generado'))

    # Para peticiones GET, simplemente renderiza la página inicial
    return render(request, 'meal_plan_result.html')

def mostrar_plan_generado(request):
    """
    Muestra el plan de comidas que fue previamente generado y guardado en la sesión.
    """
    meal_plan_data = request.session.get('meal_plan_data')
    alerta_presupuesto = request.session.get('alerta_presupuesto')

    if not meal_plan_data:
        return render(request, 'meal_plan_result.html', {
            'error': 'No hay un plan para mostrar. Por favor, genera uno primero.'
        })

    return render(request, 'meal_plan_result.html', {
        'meal_plan_json': meal_plan_data,
        'alerta_presupuesto': alerta_presupuesto
    })

