from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Producto

@receiver(post_migrate)
def create_initial_users(sender, **kwargs):
    """
    Crea el superusuario y usuarios básicos al ejecutar las migraciones.
    Se ejecuta después de que las migraciones se hayan completado.
    """
    # Crear Superusuario
    if not User.objects.filter(username='admin').exists():
        superuser = User.objects.create_superuser(
            username='admin',
            password='admin'
        )
        superuser.save()

    # Crear usuarios básicos
    if not User.objects.filter(username='usuario1').exists():
        user1 = User.objects.create_user(
            username='usuario1',
            email='usuario1@ejemplo.com',
            password='usuario123'
        )
        user1.save()

    if not User.objects.filter(username='usuario2').exists():
        user2 = User.objects.create_user(
            username='usuario2',
            email='usuario2@ejemplo.com',
            password='usuario123'
        )
        user2.save()

    if not User.objects.filter(username='usuario3').exists():
        user3 = User.objects.create_user(
            username='usuario3',
            email='usuario3@ejemplo.com',
            password='usuario123'
        )
        user3.save()
@receiver(post_migrate)
def agregar_productos(sender, **kwargs):
    if not Producto.objects.exists():  # Evitar duplicar productos
        Producto.objects.create(nombre="Amuleto de la Suerte", descripcion="Amuleto protector.", imagen='piedras.jpg', precio=14.99, cantidad=10, categoria="Cristales y Amuletos")
        Producto.objects.create(nombre="Collar de Cuarzo", descripcion="Collar con cuarzo rosa para la energía positiva.", imagen='cuarzo.jpg', precio=19.99, cantidad=15, categoria="Cristales y Amuletos")
        Producto.objects.create(nombre="Velón Mágico", descripcion="Velón especial para rituales.", imagen='vela.jpg', precio=9.99, cantidad=10, categoria="Velas e Inciensos")
        Producto.objects.create(nombre="Incienso de Sándalo", descripcion="Incienso para meditación y relajación.", imagen='incienso.jpg', precio=4.99, cantidad=20, categoria="Velas e Inciensos")
        Producto.objects.create(nombre="Tarot", descripcion="Baraja de cartas de tarot.", imagen='tarot.jpg', precio=29.99, cantidad=10, categoria="Tarot y Herramientas Espirituales")
        Producto.objects.create(nombre="Péndulo de Cuarzo", descripcion="Péndulo para lecturas espirituales.", imagen='pendulo.jpg', precio=24.99, cantidad=8, categoria="Tarot y Herramientas Espirituales")
        Producto.objects.create(nombre="Aceite de Lavanda", descripcion="Aceite esencial para relajación.", imagen='lavanda.jpg', precio=12.99, cantidad=25, categoria="Aceites y Esencias")
        Producto.objects.create(nombre="Esencia de Mirra", descripcion="Esencia para rituales y limpieza energética.", imagen='mirra.jpg', precio=14.49, cantidad=12, categoria="Aceites y Esencias")
        Producto.objects.create(nombre="Taza con Símbolos", descripcion="Taza decorada con símbolos espirituales.", imagen='taza.jpg', precio=9.99, cantidad=18, categoria="Decoración Espiritual")
        Producto.objects.create(nombre="Tapiz de Mandala", descripcion="Tapiz con diseño de mandala para meditación.", imagen='mandala.jpg', precio=39.99, cantidad=5, categoria="Decoración Espiritual")