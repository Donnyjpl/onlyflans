from django.views.generic import ListView
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import FlanForm, UsuarioForm, LoginForm, ContactoForm, OpinionClienteForm
from .models import Flan, Contacto
from django.core.mail import send_mail
from django.views import View
from django.core.paginator import Paginator
from django.contrib.auth.views import (PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView)
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render
from PIL import Image
import requests
from io import BytesIO
from django.conf import settings
import os

# Suponiendo que tienes un modelo Flan
from .models import Flan
from django.shortcuts import render
from PIL import Image
import requests
from io import BytesIO
from django.conf import settings
import os

# Vista personalizada para solicitar el restablecimiento de contraseña
def custom_password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            # Generar UID y token para el restablecimiento de contraseña
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            domain = request.get_host()
            reset_link = f"http://{domain}{reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})}"

            # Enviar el correo con el enlace de restablecimiento
            subject = "Restablecimiento de contraseña"
            message = f"""Hola {user.username},
Hemos recibido una solicitud para restablecer tu contraseña. Si no realizaste esta solicitud, puedes ignorar este correo.

Para restablecer tu contraseña, haz clic en el siguiente enlace:
<a href="{reset_link}">Restablecer contraseña</a>

Este enlace es válido solo por 24 horas.

Gracias,
Tu equipo"""

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
                html_message=message
            )
            
            return render(request, 'registration/password_reset_done.html')
        else:
            error_message = "No se encontró un usuario con ese correo electrónico."
            return render(request, 'registration/password_reset_form.html', {'error_message': error_message})

    return render(request, 'registration/password_reset_form.html')


# Vista personalizada para confirmar el restablecimiento de contraseña
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['custom_message'] = "¡Tu contraseña ha sido restablecida con éxito!"
        return context

# Usamos las vistas por defecto para las siguientes dos etapas
class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'


# Vista de inicio que muestra los flanes públicos

def inicio(request):
    # Obtener los flanes públicos
    flanes_publicos = Flan.objects.filter(is_private=False)

    # Imprimir las URLs de las imágenes para verificar
    for flan in flanes_publicos:
        print(f"Flan: {flan.name}, Imagen URL: {flan.image_url}")  # Imprime el nombre y la URL de la imagen

    # Configura el paginador (10 productos por página)
    paginator = Paginator(flanes_publicos, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Imprimir el contenido del page_obj para verificar que los productos están pasando bien
    for producto in page_obj:
        print(f"Producto: {producto.name}, Imagen URL: {producto.image_url}")  # Imprime el nombre y la URL de cada producto

    context = {
        'productos': page_obj,
        'page_obj': page_obj
    }

    return render(request, 'index.html', context)

# Vista de información sobre la empresa
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

# Vista de bienvenida que muestra los flanes privados
@login_required
def bienvenido(request):
    flanes_privados = Flan.objects.filter(is_private=True).order_by('name')
    
    # Configura el paginador (10 productos por página)
    paginator = Paginator(flanes_privados, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
         'productos': page_obj,
         'page_obj': page_obj
    }
    return render(request, 'bienvenido.html', context)

# Vista para crear un nuevo flan
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

# Vista de contacto
def contacto(request):
    if request.method == 'POST':
        formm = ContactoForm(request.POST)
        if formm.is_valid():
            formm.save()  # Guarda el formulario en la base de datos si es válido
            return HttpResponseRedirect('../success/')  # Redirige a donde sea apropiado después de enviar el formulario
    else:
        formm = ContactoForm()

    return render(request, 'contacto.html', {'formm': formm})

# Vista de éxito después del contacto
def success(request):
    return render(request, 'flanes/success.html')

# Vista para listar los mensajes de contacto
@login_required
def lista_mensajes(request):
    mensajes = Contacto.objects.filter(contacted=False)
    return render(request, 'flanes/lista_mensajes.html', {'mensajes': mensajes})

# Vista para marcar un mensaje como contactado
def marcar_contactado(request, uuid):
    mensaje = get_object_or_404(Contacto, contact_form_uuid=uuid)
    
    if request.method == 'POST':
        mensaje.contacted = True
        mensaje.date_contacted = timezone.now()  # Asignar la fecha actual
        mensaje.save()
        
        return redirect('confirmacion_contacto', uuid=uuid)
    
    return redirect('lista_mensajes')  # En caso de acceso directo a la URL sin POST

# Vista de confirmación de contacto
def confirmacion_contacto(request, uuid):
    mensaje = get_object_or_404(Contacto, contact_form_uuid=uuid)
    return render(request, 'flanes/confirmacion_contacto.html', {'mensaje': mensaje})

# Vista para agregar un nuevo usuario
def add_user(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registro_exitoso')
    else:
        form = UsuarioForm()
    return render(request, 'usuario/agregar_usuario.html', {'form': form})

# Vista de registro exitoso
def registro_exitoso(request):
    return render(request, 'usuario/registro_exitoso.html')

# Vista personalizada para el inicio de sesión
def custom_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('bienvenido')  # Cambia 'bienvenido' por el nombre de tu URL de página principal
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

# Vista para crear una opinión sobre un producto
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
            return redirect('opiniones_producto', slug=producto.slug)
    else:
        initial_data = {'nombre_cliente': request.user.username}  # Establece el nombre de usuario actual
        form = OpinionClienteForm(initial=initial_data)
    
    return render(request, 'flanes/crear_opinion.html', {'form': form, 'producto': producto})

# Vista para mostrar las opiniones de un producto
def opiniones_producto(request, slug):
    producto = get_object_or_404(Flan, slug=slug)
    opiniones = producto.opiniones.all().order_by('-created_at')[:5]
    return render(request, 'flanes/opiniones.html', {'producto': producto, 'opiniones': opiniones})

# Vista de administrador de usuarios
def admin_usuario(request):
    return render(request, 'admin.html')

# Clase para enviar correos electrónicos (ejemplo)
class EnviarCorreoView(View):
    def get(self, request):
        # Lógica para enviar el correo electrónico
        subject = 'Correo de recuperación de contraseña'
        message = 'Hola, aquí está tu contraseña: contraseña'
        
        try:
            send_mail(
                subject,
                message,
                'tu_correo@gmail.com',  # Remitente
                ['destinatario@example.com'],  # Lista de destinatarios
                fail_silently=False,
            )
            mensaje = "Correo enviado correctamente."
        except Exception as e:
            mensaje = f"Error al enviar el correo: {str(e)}"
        
        return render(request, 'template.html', {'mensaje': mensaje})
