from django.shortcuts import redirect, render

from django.contrib import messages
from app.forms import RegistrationForm
from django.contrib.auth import authenticate, login
from .models import Producto
from .models import ProductoCesta

def home(request):
    productos = Producto.objects.all()
    return render(request, 'home.html',{'productos': productos}) 

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
    productos=None
    if request.user.is_authenticated:
        productos = ProductoCesta.objects.filter(usuario=request.user)
    else:
        productos = []
    precio=sum(producto.precio*producto.cantidad for producto in productos)
    
    return render(request, 'cesta.html',{'productos': productos,'precio': precio})

def editarUsuario(request):
    return render(request, 'editarUsuario.html')
    
def editarProductos(request):
    return render(request, 'editarProductos.html')

def vistaProducto(request):
    query = request.GET.get('search', '')
    query_type = request.GET.get('search_type', 'nombre')  # Default search type is 'nombre'
    
    if query:
        if query_type == 'nombre':
            # Buscar por nombre del producto
            productos = Producto.objects.filter(nombre__icontains=query)
            print(productos)
        elif query_type == 'precio':
            # Buscar por precio
            try:
                precio = float(query)
                productos = Producto.objects.filter(precio=precio)
                print(productos)
            except ValueError:
                productos = Producto.objects.none()  # Si el valor no es un número, no hay productos
        elif query_type == 'categoria':
            # Buscar por categoría
            print(query)
            productos = Producto.objects.filter(categoria__icontains=query)
            print(productos)
            print(Producto.objects.filter(categoria__icontains=query))
            print(Producto.objects)
        else:
            productos = Producto.objects.none()  # Si no se reconoce el tipo de búsqueda, no hay resultados
    else:
        productos = Producto.objects.all()  # Si no hay búsqueda, mostrar todos los productos
    
    return render(request, 'vistaProducto.html', {'productos': productos, 'query': query, 'query_type': query_type})

def buscar_productos(request):
    query = request.GET.get('search', '') 
    productos = Producto.objects.filter(nombre__icontains=query)  
    return render(request, 'productos/buscar.html', {'productos': productos, 'query': query})
