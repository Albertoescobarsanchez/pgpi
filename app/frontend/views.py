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