from django.shortcuts import render

def home(request):
    return render(request, 'home.html') 

def login(request):
    return render(request,'login.html')

def register(request):
    return render(request,'register.html')

def cesta(request):
    return render(request, 'cesta.html')

def editarUsuario(request):
    return render(request, 'editarUsuario.html')
    
def editarProductos(request):
    return render(request, 'editarProductos.html')

def vistaProducto(request):
    return render(request, 'vistaProducto.html')