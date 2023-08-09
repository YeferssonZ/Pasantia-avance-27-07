from django.shortcuts import render, get_object_or_404
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import redirect
from .models import *
import random
from django.http import JsonResponse
from random import sample
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in

# Create your views here.
def index(request):
    # Obtén todas las categorías y subcategorías de la base de datos
    categorias = Categoria.objects.all()
    subcategorias = Subcategoria.objects.all()

    # Obtén todos los productos de la base de datos
    todos_los_productos = Producto.objects.all()

    # Obtener el carrito actual del usuario o crear uno nuevo
    carrito_id = request.session.get('carrito_id')
    if carrito_id:
        try:
            carrito = Carrito.objects.get(id=carrito_id)
        except Carrito.DoesNotExist:
            carrito = None
    else:
        carrito = None

    # Seleccionar una muestra aleatoria de productos destacados
    productos_destacados = random.sample(list(todos_los_productos), min(6, len(todos_los_productos)))

    return render(request, 'index.html', {'categorias': categorias, 'subcategorias': subcategorias, 'carrito': carrito, 'productos_destacados': productos_destacados})



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


def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    # Obtener el carrito del usuario autenticado si está logueado
    carrito_autenticado = None
    if request.user.is_authenticated:
        carrito_autenticado, _ = Carrito.objects.get_or_create(usuario=request.user)

    # Obtener el carrito de la sesión actual del usuario o crear uno nuevo
    carrito_id = request.session.get('carrito_id')
    if carrito_id:
        try:
            carrito = Carrito.objects.get(id=carrito_id)
        except Carrito.DoesNotExist:
            carrito = None
    else:
        carrito = None

    if not carrito:
        carrito = Carrito.objects.create(usuario=None)  # No se asocia con un usuario
        request.session['carrito_id'] = carrito.id

    if producto.stock > 0:
        # Verificar si el usuario está autenticado
        if request.user.is_authenticated:
            # Transferir productos del carrito no autenticado al carrito del usuario autenticado
            if carrito.itemcarrito_set.exists():
                for item in carrito.itemcarrito_set.all():
                    item.carrito = carrito_autenticado
                    item.save()
            carrito.delete()  # Eliminar el carrito no autenticado

            # Obtener el carrito actual del usuario autenticado
            carrito = carrito_autenticado

        item_carrito, created = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto)

        # Restricción de cantidad máxima basada en el stock
        max_cantidad_permitida = min(producto.stock, 30)
        if not created:
            if item_carrito.cantidad < max_cantidad_permitida:
                item_carrito.cantidad += 1
                item_carrito.save()
        else:
            item_carrito.cantidad = 1
            item_carrito.save()

        return JsonResponse({'cantidad': item_carrito.cantidad})

    return JsonResponse({})

def transferir_carrito(sender, user, request, **kwargs):
    carrito_no_autenticado = None
    carrito_autenticado = None

    # Obtener el carrito no autenticado si existe
    carrito_id = request.session.get('carrito_id')
    if carrito_id:
        try:
            carrito_no_autenticado = Carrito.objects.get(id=carrito_id)
        except Carrito.DoesNotExist:
            carrito_no_autenticado = None

    # Obtener el carrito del usuario autenticado
    carrito_autenticado, _ = Carrito.objects.get_or_create(usuario=user)

    # Transferir productos del carrito no autenticado al carrito del usuario autenticado
    if carrito_no_autenticado and carrito_no_autenticado.itemcarrito_set.exists():
        for item in carrito_no_autenticado.itemcarrito_set.all():
            item.carrito = carrito_autenticado
            item.save()

        carrito_no_autenticado.delete()  # Eliminar el carrito no autenticado

user_logged_in.connect(transferir_carrito)


def ver_carrito(request):
    usuario = request.user

    if usuario.is_authenticated:  # Verificar si el usuario está autenticado
        carrito_autenticado, _ = Carrito.objects.get_or_create(usuario=usuario)
    else:
        carrito_autenticado = None

    carrito_no_autenticado = None

    # Obtener el carrito no autenticado si existe
    carrito_id = request.session.get('carrito_id')
    if carrito_id:
        try:
            carrito_no_autenticado = Carrito.objects.get(id=carrito_id)
        except Carrito.DoesNotExist:
            carrito_no_autenticado = None

    if carrito_no_autenticado and carrito_no_autenticado.itemcarrito_set.exists():
        for item in carrito_no_autenticado.itemcarrito_set.all():
            item.carrito = carrito_autenticado
            item.save()

        carrito_no_autenticado.delete()  # Eliminar el carrito no autenticado

    subtotal_items = []
    total = 0

    if carrito_autenticado:
        for item in carrito_autenticado.itemcarrito_set.all():
            subtotal = item.cantidad * item.producto.precio
            subtotal_items.append((item, subtotal))
            total += subtotal

    return render(request, 'carrito.html', {'carrito': carrito_autenticado, 'carrito_no_autenticado': carrito_no_autenticado, 'subtotal_items': subtotal_items, 'total': total})


def cambiar_cantidad(request, item_id, action):
    if request.method == 'GET' and request.is_ajax():
        item_carrito = ItemCarrito.objects.get(id=item_id)
        if action == 'sumar':
            if item_carrito.cantidad < item_carrito.producto.stock:
                item_carrito.cantidad += 1
                item_carrito.save()
                return JsonResponse({'success': True})
        elif action == 'restar':
            if item_carrito.cantidad > 1:
                item_carrito.cantidad -= 1
                item_carrito.save()
                return JsonResponse({'success': True})
    return JsonResponse({'success': False})
