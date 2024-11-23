from django.shortcuts import redirect, render

from django.contrib import messages
from app.forms import RegistrationForm
from django.contrib.auth import authenticate, login
from .models import Producto


def home(request):
    return render(request, 'home.html') 

def login_user(request):
    print(request)
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/")  
        else:
            messages.error(request, "Nombre de usuario o contraseña incorrectos")

    return render(request, "login.html")

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "¡Cuenta creada exitosamente!")
            return redirect('login')  # Redirige al login después del registro
        else:
            messages.error(request, "Corrige los errores en el formulario.")
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})

def cesta(request):
    return render(request, 'cesta.html')

def editarUsuario(request):
    return render(request, 'editarUsuario.html')
    
def editarProductos(request):
    return render(request, 'editarProductos.html')

def vistaProducto(request):
    query = request.GET.get('search', '')  # Obtenemos el término de búsqueda desde la URL
    productos = Producto.objects.all()

    # Si hay una consulta de búsqueda, filtrar los productos
    if query:
        productos = productos.filter(
            nombre__icontains=query) | productos.filter(descripcion__icontains=query)
    
    return render(request, 'vistaProducto.html', {'productos': productos, 'query': query})

def buscar_productos(request):
    query = request.GET.get('search', '')  # Obtiene la búsqueda desde la URL
    productos = Producto.objects.filter(nombre__icontains=query)  # Filtra los productos por nombre (case-insensitive)
    return render(request, 'productos/buscar.html', {'productos': productos, 'query': query})