from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Supermarket
from django.db.models import Q

# Vista para mostrar los productos con filtros y paginación
def vista_supermercado(request):
    productos = Supermarket.objects.all()  # Obtener todos los productos inicialmente

    # Filtrado por supermercado
    filtro_supermercado = request.GET.get('supermarket', '')
    if filtro_supermercado:
        productos = productos.filter(nombre_supermercado__icontains=filtro_supermercado)

    # Filtrado por nombre de producto
    filtro_nombre_producto = request.GET.get('product_name', '')
    if filtro_nombre_producto:
        productos = productos.filter(nombre_producto__icontains=filtro_nombre_producto)

    # Filtrado por marca de producto
    filtro_marca = request.GET.get('product_brand', '')
    if filtro_marca:
        productos = productos.filter(marca_producto__icontains=filtro_marca)

    # Filtrado por precio de producto
    filtro_precio = request.GET.get('price', '')
    if filtro_precio:
        try:
            precio = float(filtro_precio)
            productos = productos.filter(precio_producto__lte=precio)
        except ValueError:
            pass

    # Paginación
    paginador = Paginator(productos, 16)  # Mostrar 16 productos por página
    numero_pagina = request.GET.get('page')
    page_obj = paginador.get_page(numero_pagina)

    return render(request, 'supermarket.html', {'page_obj': page_obj})

# Vista para manejar la búsqueda (reutilizada en la vista principal)
def buscar_productos(request):
    return vista_supermercado(request)

