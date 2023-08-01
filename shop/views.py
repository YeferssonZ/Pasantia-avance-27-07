from django.shortcuts import render, get_object_or_404
from .models import *

# Create your views here.
def index(request):
    # Obtén todas las categorías y subcategorías de la base de datos
    categorias = Categoria.objects.all()
    subcategorias = Subcategoria.objects.all()

    # Pasa los datos a la plantilla 'index.html'
    return render(request, 'index.html', {'categorias': categorias, 'subcategorias': subcategorias})


def login(request):
    return render(request, 'login.html')

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
    # Obtener el producto seleccionado desde la base de datos
    producto = get_object_or_404(Producto, id=producto_id)

    # Pasa los datos a la plantilla 'producto.html'
    return render(request, 'producto.html', {'producto': producto})