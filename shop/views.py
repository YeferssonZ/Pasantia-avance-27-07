from django.shortcuts import render
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


