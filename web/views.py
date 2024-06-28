from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponseForbidden
from .forms import FlanForm,ContactFormForm,UsuarioForm
from .models import Flan
from django.contrib.auth.decorators import login_required

# Create your views here.

def inicio(request):
    # Aquí podrías obtener los productos desde la base de datos
    flanes_publicos = Flan.objects.filter(is_private=False)
    context = {
        'productos': flanes_publicos
    }
    return render(request, 'index.html', context)

def acerca(request):
    descripcion = """
        <p><strong>OnlyFlans</strong> es una empresa enfocada en el mundo de la pastelería y los postres, especializándose en la venta de flan. Fundada en 2021 en Santiago de Chile, como una empresa familiar ubicada en Providencia, a pasos del metro Parque Bustamante.</p>
        
        <p>El objetivo principal de OnlyFlans es ofrecer productos de calidad a su clientela, mostrándose como una empresa seria desde su reciente creación.</p>
        
        <p>En nuestro sitio web, presentamos una variedad de productos disponibles para el público general, así como productos especiales reservados exclusivamente para usuarios registrados. Esta estrategia busca generar una base sólida de clientes potenciales y fidelizar a nuestros clientes recurrentes.</p>
        
        <p>Estamos preparados para futuras características como la venta de productos a través de internet, entre otras innovaciones.</p>
    """
    empresa = "OnlyFlans S.A."
    fecha_creacion = "2021"
    context = {
        'empresa': empresa,
        'fecha_creacion': fecha_creacion,
        'descripcion': descripcion
    }
    return render(request, 'acerca.html', context)

@login_required
def bienvenido(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("Esta página está protegida. Necesitas iniciar sesión.")
    
    flanes_privados = Flan.objects.filter(is_private=True)
    context = {
        'productos': flanes_privados
    }
    return render(request, 'bienvenido.html', context)


def create_flan(request):
    if request.method == 'POST':
        form = FlanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio')  # Redirige a donde quieras después de guardar
    else:
        form = FlanForm()
    
    return render(request, 'create_flan.html', {'form': form})

def contacto(request):
    if request.method == 'POST':
        form = ContactFormForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el formulario en la base de datos si es válido
            return HttpResponseRedirect('../success/')  # Redirige a donde sea apropiado después de enviar el formulario
    else:
        form = ContactFormForm()

    return render(request, 'contacto.html', {'form': form})

def success(request):
    return render(request, 'success.html')


def add_user(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registro_exitoso')
    else:
        form = UsuarioForm()
    return render(request, 'agregar_usuario.html', {'form': form})

def registro_exitoso(request):
    return render(request, 'registro_exitoso.html')