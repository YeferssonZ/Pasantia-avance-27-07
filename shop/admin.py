from django.contrib import admin
from .models import *

# Registramos todos los modelos en el panel de administración
admin.site.register(Roles)
admin.site.register(Cuenta)
admin.site.register(Categoria)
admin.site.register(Subcategoria)
admin.site.register(Producto)
admin.site.register(Tutorial)
admin.site.register(Comentario)
admin.site.register(Carrito)
admin.site.register(MetodoPago)
