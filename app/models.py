from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError

def validate_min_value(value):
    if value < 0:
        raise ValidationError("El valor no puede ser negativo.")

class Producto(models.Model):
    nombre = models.CharField(max_length=100) 
    descripcion = models.CharField(max_length=100)
    imagen = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2,validators=[validate_min_value])
    cantidad = models.PositiveIntegerField()          
    categoria = models.CharField(max_length=100)  

class ProductoCesta(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad} en cesta"
    
class Pedido(models.Model):
    class EstadoPedido(models.TextChoices):
        PENDIENTE = 'PENDIENTE', 'Pendiente'
        EN_PROCESO = 'EN_PROCESO', 'En Proceso'
        COMPLETADO = 'COMPLETADO', 'Completado'

    email = models.EmailField(null=False)  
    fecha = models.DateTimeField(auto_now_add=True)
    direccion = models.TextField()
    codigo_postal = models.CharField(max_length=10)
    total = models.DecimalField(max_digits=10, decimal_places=2,validators=[validate_min_value])
    estado =  models.CharField(
        max_length=10,
        choices=EstadoPedido.choices,
        default=EstadoPedido.PENDIENTE,  
    )


class ProductoPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='productos')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
