from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.contrib import messages
from django.urls import reverse
from app.forms import RegistrationForm
from django.contrib.auth import authenticate, login
from .models import Pedido, Producto, ProductoPedido
from .models import ProductoCesta
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render
from .models import Pedido


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
    if request.user.is_authenticated:
        productos = ProductoCesta.objects.filter(usuario=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        productos = ProductoCesta.objects.filter(usuario=None, session_key=session_key)

    if request.method == 'POST':
        user_name = request.POST.get('name')
        user_email = request.POST.get('email')
        address = request.POST.get('address')
        postal_code = request.POST.get('postalCode')
        card_number = request.POST.get('cardNumber')  
        
        amount = sum(producto.producto.precio * producto.cantidad for producto in productos)
        payment_successful = True

        if payment_successful:
            pedido = Pedido.objects.create(
                email=user_email,
                direccion=address,
                codigo_postal=postal_code,
                total=amount
                
            )
            for item in productos:
                ProductoPedido.objects.create(
                    pedido=pedido,
                    producto=item.producto,
                    cantidad=item.cantidad
                )

            subject = "Confirmación de Pago"
            message = f"¡Gracias por tu compra!\n\nProducto(s):\n"
            for producto in productos:
                message += f"{producto.producto.nombre} x{producto.cantidad} - ${producto.producto.precio * producto.cantidad}\n"
            message += f"\nTotal a Pagar: ${amount}\nDirección de Envío: {address}, {postal_code}"
            send_mail(subject, message, 'no-reply@example.com', [user_email])
            productos.delete()
            return HttpResponseRedirect(reverse('pedidos'))

        return JsonResponse({'success': False})

    precio = sum(producto.producto.precio * producto.cantidad for producto in productos)

    return render(request, 'pasarelaPago.html', {'precio': precio})
def cesta(request):
    if request.user.is_authenticated:
        productos_cesta = ProductoCesta.objects.filter(usuario=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        productos_cesta = ProductoCesta.objects.filter(usuario=None, session_key=session_key)
    
    # Calcular el total
    total_precio = sum(item.producto.precio * item.cantidad for item in productos_cesta)

    return render(request, 'cesta.html', {
        'productos': productos_cesta,
        'precio': total_precio
    })

def agregar_a_cesta(request, producto_nombre):
    producto = get_object_or_404(Producto, nombre=producto_nombre)
    # Obtener la cantidad desde el formulario
    cantidad = int(request.POST.get('cantidad', 1))
    if request.user.is_authenticated:
        usuario = request.user
        session_key = None
    else:
        usuario = None
        session_key = request.session.session_key
        if not session_key:
            request.session.create()  # Crear una sesión si no existe
            session_key = request.session.session_key

    # Verificar si el producto ya está en la cesta
    try:
        cesta_producto = ProductoCesta.objects.get(usuario=usuario, producto=producto, session_key=session_key)
        # Si ya existe, actualizamos la cantidad
        cesta_producto.cantidad += cantidad
        cesta_producto.save()
        mensaje = f'{producto.nombre} actualizado en la cesta.'
    except ProductoCesta.DoesNotExist:
        # Si no existe, creamos una nueva entrada
        cesta_producto = ProductoCesta.objects.create(
            usuario=usuario,
            producto=producto,
            cantidad=cantidad,
            session_key=session_key
        )
        mensaje = f'{producto.nombre} añadido a la cesta.'

    # Responder con un mensaje de confirmación en formato JSON
    return JsonResponse({
        'mensaje': mensaje,
        'cantidad': cesta_producto.cantidad
    })

def eliminar_producto(request, producto_id):
    # Eliminar un producto de la cesta del usuario autenticado
     # Obtener el producto en la cesta del usuario
    producto_cesta = get_object_or_404(ProductoCesta, usuario=request.user, producto_id=producto_id)

    # Obtener la cantidad que se quiere eliminar desde el formulario (por ejemplo, 'cantidad_a_eliminar')
    cantidad_a_eliminar = int(request.POST.get('cantidad_a_eliminar', 1))

    if producto_cesta.cantidad > cantidad_a_eliminar:
        # Si hay más de la cantidad que queremos eliminar, solo restamos
        producto_cesta.cantidad -= cantidad_a_eliminar
        producto_cesta.save()
    else:
        # Si la cantidad es igual o menor, eliminamos el producto de la cesta
        producto_cesta.delete()

    return redirect('ver_cesta')

def eliminar_producto_no_autenticado(request, producto_id):
    # Eliminar un producto de la cesta para un usuario no autenticado (basado en la sesión)
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
    
     # Obtener el producto en la cesta del usuario
    producto_cesta = get_object_or_404(ProductoCesta, usuario=request.user, producto_id=producto_id)

    # Obtener la cantidad que se quiere eliminar desde el formulario (por ejemplo, 'cantidad_a_eliminar')
    cantidad_a_eliminar = int(request.POST.get('cantidad_a_eliminar', 1))

    if producto_cesta.cantidad > cantidad_a_eliminar:
        # Si hay más de la cantidad que queremos eliminar, solo restamos
        producto_cesta.cantidad -= cantidad_a_eliminar
        producto_cesta.save()
    else:
        # Si la cantidad es igual o menor, eliminamos el producto de la cesta
        producto_cesta.delete()

    return redirect('ver_cesta')


def pedidos(request):
    pedidos_info = []
    no_pedidos = False

    if request.user.is_authenticated:
        # Si el usuario está autenticado, buscar pedidos asociados a su correo.
        pedidos = Pedido.objects.filter(email=request.user.email).order_by('-fecha')
    else:
        # Si no está autenticado, manejar el caso del formulario de correo.
        email = request.POST.get('email')  # Capturar el correo desde el formulario.
        if email:
            pedidos = Pedido.objects.filter(email=email).order_by('-fecha')
            if not pedidos:
                no_pedidos = True
        else:
            pedidos = None

    if pedidos:
        # Preparar información de los pedidos si existen.
        for pedido in pedidos:
            productos_info = []
            for producto_pedido in pedido.productos.all():
                total_producto = producto_pedido.producto.precio * producto_pedido.cantidad
                productos_info.append({
                    'nombre': producto_pedido.producto.nombre,
                    'cantidad': producto_pedido.cantidad,
                    'precio': producto_pedido.producto.precio,
                    'total': total_producto,
                    'imagen':producto_pedido.producto.imagen
                })
            total_pedido = sum(producto['total'] for producto in productos_info)  # Total del pedido
            pedidos_info.append({
                'fecha': pedido.fecha,
                'productos': productos_info,
                'total_pedido': total_pedido,
                'estado': pedido.estado
            })

    return render(request, 'pedidos.html', {'pedidos_info': pedidos_info, 'no_pedidos': no_pedidos})
