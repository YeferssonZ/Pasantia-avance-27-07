from django.conf import settings
from django.db import models

class Roles(models.Model):
    ADMIN = 'admin'
    CLIENTE = 'cliente'
    ROL_CHOICES = [
        (ADMIN, 'Admin'),
        (CLIENTE, 'Cliente')
    ]
    nombre = models.CharField(max_length=100, choices=ROL_CHOICES)

    def __str__(self):
        return self.nombre.capitalize()

class Cuenta(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    
    rol = models.ForeignKey(Roles, on_delete=models.CASCADE)
    def __str__(self):
        return self.username

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Subcategoria(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    stock = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    especificaciones_tecnicas = models.TextField(blank=True, null=True)
    subcategoria = models.ForeignKey(Subcategoria, on_delete=models.CASCADE, blank=True, null=True)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)

    def save(self, *args, **kwargs):
        # Verificar si el objeto ya tiene un ID asignado
        if not self.id:
            # Obtener el máximo ID existente y agregar 1
            max_id = Producto.objects.aggregate(models.Max('id'))['id__max']
            self.id = max_id + 1 if max_id else 1

        super().save(*args, **kwargs)

    def obtener_especificaciones(self):
        if self.especificaciones_tecnicas:
            return self.especificaciones_tecnicas.split(',')
        else:
            return []

    def __str__(self):
        return self.nombre

class Tutorial(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    contenido = models.TextField()
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

class Comentario(models.Model):
    texto = models.TextField()
    fecha_hora = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.usuario.username} - {self.producto.nombre}'

class Carrito(models.Model):
    usuario = models.ForeignKey(Cuenta, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Carrito de {self.usuario.username}'

class MetodoPago(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre