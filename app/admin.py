from django.contrib import admin
from .models import Producto
from .models import ProductoCesta

admin.site.register(Producto)
admin.site.register(ProductoCesta)