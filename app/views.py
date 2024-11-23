from django.shortcuts import redirect, render

from django.contrib import messages
from app.forms import RegistrationForm
from django.contrib.auth import authenticate, login

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
    return render(request, 'vistaProducto.html')