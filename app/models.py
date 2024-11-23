from django.db import models


class Producto(models.Model):
    nombre = models.CharField(max_length=100) 
    descripcion = models.CharField(max_length=100)
    imagen = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField()           
    categoria = models.CharField(max_length=100)
