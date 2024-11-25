from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.contrib import messages
from app.forms import RegistrationForm
from django.contrib.auth import authenticate, login
from .models import Producto
from .models import ProductoCesta
from django.core.mail import send_mail

def home(request):
    productos = Producto.objects.all()
    return render(request, 'home.html',{'productos': productos}) 

def login_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Buscar usuario por correo electrónico
        try:
            user = User.objects.get(email=email)  # Buscar al usuario por su email
            username = user.username  # Obtener el nombre de usuario asociado
        except User.DoesNotExist:
            messages.error(request, "El correo electrónico no está registrado.")
            return render(request, "login.html")  # Devolver la misma plantilla con el mensaje de error

        # Autenticar usando el nombre de usuario asociado
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/")  # Redirigir a la página principal
        else:
            messages.error(request, "Correo o contraseña incorrectos.")
            return render(request, "login.html")  # Devolver la misma plantilla con el mensaje de error

    # En el caso de solicitudes GET, siempre devolver el formulario de inicio de sesión
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

def pasarela_pago(request):
    if request.method == 'POST':
        user_name = request.POST.get('userName')
        user_email = request.POST.get('userEmail')
        address = request.POST.get('address')
        postal_code = request.POST.get('postalCode')
        card_number = request.POST.get('cardNumber')  
        productos = ProductoCesta.objects.filter(usuario=request.user)
        amount = sum(producto.precio * producto.cantidad for producto in productos)
        payment_successful = True

        if payment_successful:
            subject = "Confirmación de Pago"
            message = f"¡Gracias por tu compra!\n\nProducto(s):\n"
            for producto in productos:
                message += f"{producto.nombre} x{producto.cantidad} - ${producto.precio * producto.cantidad}\n"
            message += f"\nTotal a Pagar: ${amount}\nDirección de Envío: {address}, {postal_code}"
            send_mail(subject, message, 'no-reply@example.com', [user_email])
            productos.delete()
            return JsonResponse({'success': True})

        return JsonResponse({'success': False})

    productos = ProductoCesta.objects.filter(usuario=request.user)
    precio = sum(producto.precio * producto.cantidad for producto in productos)

    return render(request, 'pasarelaPago.html', {'precio': precio})
