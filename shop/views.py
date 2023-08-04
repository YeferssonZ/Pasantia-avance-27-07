from django.shortcuts import render, get_object_or_404
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import redirect
from .models import *
import random

# Create your views here.
def index(request):
    # Obtén todas las categorías y subcategorías de la base de datos
    categorias = Categoria.objects.all()
    subcategorias = Subcategoria.objects.all()

    # Pasa los datos a la plantilla 'index.html'
    return render(request, 'index.html', {'categorias': categorias, 'subcategorias': subcategorias})

def logout_view(request):
    logout(request)
    return redirect('shop:index')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('shop:index')
        else:
            # Aquí puedes agregar algún mensaje de error en caso de inicio de sesión fallido
            pass

    return render(request, 'registrar/login.html')


def mostrar_categoria(request, categoria_id):
    # Obtener la categoría seleccionada desde la base de datos
    categoria = get_object_or_404(Categoria, id=categoria_id)
    # Obtener todas las subcategorías asociadas a la categoría seleccionada
    subcategorias = categoria.subcategoria_set.all()

    # Pasa los datos a la plantilla 'categoria.html'
    return render(request, 'categoria.html', {'categoria': categoria, 'subcategorias': subcategorias})

def mostrar_subcategoria(request, subcategoria_id):
    # Obtener la subcategoría seleccionada desde la base de datos
    subcategoria = get_object_or_404(Subcategoria, id=subcategoria_id)
    # Obtener todos los productos asociados a la subcategoría seleccionada
    productos = subcategoria.producto_set.all()

    # Pasa los datos a la plantilla 'categoria.html'
    return render(request, 'categoria.html', {'categoria': subcategoria.categoria, 'subcategorias': subcategoria.categoria.subcategoria_set.all(), 'productos': productos})

def mostrar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    subcategoria_productos = Producto.objects.filter(subcategoria=producto.subcategoria).order_by('id')

    # Obtener el índice del producto actual en la lista
    current_index = list(subcategoria_productos).index(producto)

    # Obtener el producto anterior y siguiente si existen
    producto_anterior = subcategoria_productos[current_index - 1] if current_index > 0 else None
    producto_siguiente = subcategoria_productos[current_index + 1] if current_index < len(subcategoria_productos) - 1 else None

    # Obtener productos relacionados al azar (excepto el producto actual) y elegir hasta 3
    productos_relacionados = random.sample(list(subcategoria_productos.exclude(id=producto.id)), min(5, subcategoria_productos.count() - 1))

    context = {
        'producto': producto,
        'producto_anterior': producto_anterior,
        'producto_siguiente': producto_siguiente,
        'productos_relacionados': productos_relacionados,
    }

    return render(request, 'producto.html', context)

def buscar_productos(request):
    query = request.GET.get('q')

    if query:
        # Realiza la búsqueda de productos que coincidan con la consulta
        productos = Producto.objects.filter(nombre__icontains=query)
    else:
        productos = []

    return render(request, 'buscar_producto.html', {'query': query, 'productos': productos})
