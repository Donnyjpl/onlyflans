from django.views.generic import ListView
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponseForbidden
from .forms import FlanForm,UsuarioForm,LoginForm,ContactoForm,OpinionClienteForm
from .models import Flan,Contacto



# Create your views here.

def inicio(request):
    
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
    flanes_privados = Flan.objects.filter(is_private=True)
    context = {
        'productos': flanes_privados
    }
 
    return render(request, 'bienvenido.html', context)

@login_required
def create_flan(request):
    if request.method == 'POST':
        form = FlanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio')  # Redirige a donde quieras después de guardar
    else:
        form = FlanForm()
    
    return render(request, 'flanes/create_flan.html', {'form': form})

def contacto(request):
    if request.method == 'POST':
        formm = ContactoForm(request.POST)
        if formm.is_valid():
            formm.save()  # Guarda el formulario en la base de datos si es válido
            return HttpResponseRedirect('../success/')  # Redirige a donde sea apropiado después de enviar el formulario
    else:
        formm= ContactoForm()

    return render(request, 'contacto.html', {'formm': formm})

def success(request):
    return render(request, 'flanes/success.html')

@login_required
def lista_mensajes(request):
    mensajes=Contacto.objects.filter(contacted=False)
    return render(request, 'flanes/lista_mensajes.html', {'mensajes': mensajes})

def marcar_contactado(request, uuid):
    mensaje = get_object_or_404(Contacto, contact_form_uuid=uuid)
    
    if request.method == 'POST':
        # Marcar el mensaje como contactado
        mensaje.contacted = True
        mensaje.date_contacted = timezone.now()  # Asignar la fecha actual
        mensaje.save()
        
        # Redirigir a la página de confirmación
        return redirect('confirmacion_contacto', uuid=uuid)
    
    return redirect('lista_mensajes')  # En caso de acceso directo a la URL sin POST

def confirmacion_contacto(request, uuid):
    mensaje = get_object_or_404(Contacto, contact_form_uuid=uuid)
    return render(request, 'flanes/confirmacion_contacto.html', {'mensaje': mensaje})

def add_user(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registro_exitoso')
    else:
        form = UsuarioForm()
    return render(request, 'usuario/agregar_usuario.html', {'form': form})

def registro_exitoso(request):
    return render(request, 'usuario/registro_exitoso.html')

def custom_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page.
                return redirect('bievenido')  # Cambia 'home' por el nombre de tu URL de página principal
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})
@login_required
def crear_opinion(request, slug):
    producto = get_object_or_404(Flan, slug=slug)
    
    if request.method == 'POST':
        form = OpinionClienteForm(request.POST)
        if form.is_valid():
            opinion = form.save(commit=False)
            opinion.producto = producto
            opinion.nombre_cliente = request.user.username  # Asigna el nombre de usuario actual
            opinion.save()
            # Redirige a la página de opiniones del producto usando el slug
            return redirect('opiniones_producto', slug=producto.slug)
    else:
        initial_data = {'nombre_cliente': request.user.username}  # Establece el nombre de usuario actual
        form = OpinionClienteForm(initial=initial_data)
    
    return render(request, 'flanes/crear_opinion.html', {'form': form, 'producto': producto})

def opiniones_producto(request, slug):
    producto = get_object_or_404(Flan, slug=slug)
    opiniones = producto.opiniones.all().order_by('-created_at')[:5]
    return render(request, 'flanes/opiniones.html', {'producto': producto, 'opiniones': opiniones})

def admin_usuario(request):
    return render(request, 'admin.html')
