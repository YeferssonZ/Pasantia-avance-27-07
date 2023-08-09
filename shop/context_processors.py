# context_processors.py

from .models import *

def categorias_subcategorias(request):
    categorias = Categoria.objects.all()
    subcategorias = Subcategoria.objects.all()
    return {'categorias': categorias, 'subcategorias': subcategorias}

def carrito_cantidad(request):
    cantidad_productos = 0
    if request.user.is_authenticated:
        # Obtener la cantidad desde la base de datos si el usuario está logueado
        try:
            carrito = Carrito.objects.get(usuario=request.user)
            cantidad_productos = carrito.itemcarrito_set.aggregate(total_cantidad=models.Sum('cantidad'))['total_cantidad']
        except Carrito.DoesNotExist:
            pass
    else:
        # Obtener la cantidad de la sesión si el usuario no está logueado
        session_carrito = request.session.get('carrito', {})
        cantidad_productos = sum(session_carrito.values())
        
    return {'carrito_cantidad': cantidad_productos}
