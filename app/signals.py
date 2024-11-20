from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import User

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
