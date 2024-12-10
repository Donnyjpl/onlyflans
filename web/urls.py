from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import bienvenido, acerca, inicio, create_flan, contacto, success, add_user, registro_exitoso, opiniones_producto, crear_opinion
from .views import lista_mensajes, marcar_contactado, confirmacion_contacto,admin_usuario,redimensionar_imagen


from .views import (
    CustomPasswordResetConfirmView,
    CustomPasswordResetDoneView,
    CustomPasswordResetCompleteView,
    custom_password_reset_request,
)



urlpatterns = [
    path('', inicio, name='inicio'),
    path('bienvenido/', bienvenido, name='bienvenido'),
    path('acerca/', acerca, name='acerca'),
    path('crear/', create_flan, name='crear'),
    path('contacto/', contacto, name='contacto'),
    path('admin2/', admin_usuario, name='admin2'),
    path('mensajes/', lista_mensajes, name='lista_mensajes'),
    path('marcar-contactado/<uuid:uuid>/', marcar_contactado, name='marcar_contactado'),
    path('confirmacion-contacto/<uuid:uuid>/', confirmacion_contacto, name='confirmacion_contacto'),  # Aquí faltaba una coma
    path('success/', success, name='success'),
    
    path('registro/', add_user, name='user'), 
    path('registro_exitoso/', registro_exitoso, name='registro_exitoso'),
     
     
    path('password_reset/', custom_password_reset_request, name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('redimensionar_imagen/<slug:flan_slug>/', redimensionar_imagen, name='redimensionar_imagen'),
    
    path('producto/<slug:slug>/opinion/', crear_opinion, name='crear_opinion'),
    path('producto/<slug:slug>/opiniones/', opiniones_producto, name='opiniones_producto'),
    path('accounts/', include('django.contrib.auth.urls')),  # Coma al final de esta línea para evitar errores futuros
]# Solo en desarrollo, servir archivos de medios
