from django.contrib import admin
from django.urls import path, include
from .views import bienvenido, acerca, inicio, create_flan, contacto, success, add_user, registro_exitoso, opiniones_producto, crear_opinion
from .views import lista_mensajes, marcar_contactado, confirmacion_contacto  # Asegúrate de importar las vistas necesarias

urlpatterns = [
    path('', inicio, name='inicio'),
    path('bienvenido/', bienvenido, name='bienvenido'),
    path('acerca/', acerca, name='acerca'),
    path('crear/', create_flan, name='crear'),
    path('contacto/', contacto, name='contacto'),
    path('mensajes/', lista_mensajes, name='lista_mensajes'),
    path('marcar-contactado/<uuid:uuid>/', marcar_contactado, name='marcar_contactado'),
    path('confirmacion-contacto/<uuid:uuid>/', confirmacion_contacto, name='confirmacion_contacto'),  # Aquí faltaba una coma
    path('success/', success, name='success'),
    path('registro/', add_user, name='user'), 
    path('registro_exitoso/', registro_exitoso, name='registro_exitoso'), 
    path('producto/<slug:slug>/opinion/', crear_opinion, name='crear_opinion'),
    path('producto/<slug:slug>/opiniones/', opiniones_producto, name='opiniones_producto'),
    path('accounts/', include('django.contrib.auth.urls')),  # Coma al final de esta línea para evitar errores futuros
]
