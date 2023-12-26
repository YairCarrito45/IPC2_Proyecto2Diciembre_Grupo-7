from django.db import models

# Create your models here.
#aca se va a crear la base de datos y se va pedir datos a cliente
class Cliente(models.Model):
    nit = models.CharField(max_length=200, unique=True, null=True, blank=True)
    nombre = models.CharField(max_length=200, null=True, blank=False)
    telefono = models.CharField(max_length=200, null=True, blank=False) 
    direccion = models.TextField(null=True, blank=False)  # Campo para la dirección domiciliar
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='clientes'
        verbose_name_plural = 'clientes'

    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    nombre = models.CharField(max_length=255, unique=True, null=True, blank= False)
    descripcion = models.CharField(max_length=255, null=True, blank=True)
    imagen = models.ImageField(upload_to='productos', null=True, blank=True)
    precio = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    stock = models.IntegerField(blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta: 
        verbose_name='producto'
        verbose_name_plural = 'productos'
        order_with_respect_to = 'descripcion'

    def __str__(self):
        return self.descripcion

