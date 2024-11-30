"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from app import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('register/',views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('vistaProducto/', views.vistaProducto, name='vistaProducto'),
    path('buscar/', views.buscar_productos, name='buscar_productos'),
    path('pasarelaPago/',views.pasarela_pago,name='pasarelaPago'),
    path('agregar-a-cesta/<str:producto_nombre>/', views.agregar_a_cesta, name='agregar_a_cesta'),
    path('cesta/', views.ver_cesta, name='cesta'),    path('cesta/', views.ver_cesta, name='cesta'),
    path('eliminar-producto/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('eliminar-producto-no-autenticado/<int:producto_id>/', views.eliminar_producto_no_autenticado, name='eliminar_producto_no_autenticado'),
    path('pedidos/',views.pedidos,name='pedidos'),



]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])