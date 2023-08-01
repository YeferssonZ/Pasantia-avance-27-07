from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('categorias/<int:categoria_id>/', views.mostrar_categoria, name='mostrar_categoria'),
    path('subcategorias/<int:subcategoria_id>/', views.mostrar_subcategoria, name='mostrar_subcategoria'),
    path('productos/<int:producto_id>/', views.mostrar_producto, name='mostrar_producto'),
    path('login/', views.login, name='login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)