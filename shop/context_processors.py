# context_processors.py

from .models import *

def categorias_subcategorias(request):
    categorias = Categoria.objects.all()
    subcategorias = Subcategoria.objects.all()
    return {'categorias': categorias, 'subcategorias': subcategorias}
