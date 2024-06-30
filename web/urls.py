from django.contrib import admin
from django.urls import path,include
from .views import bienvenido, acerca,inicio,create_flan,contacto,success,add_user,registro_exitoso,opiniones_producto,crear_opinion


urlpatterns = [
    path('', inicio, name='inicio'),
    path('bienvenido/', bienvenido, name='bienvenido'),
    path('acerca/', acerca, name='acerca'),
    path('crear/', create_flan, name='crear'),
    path('contacto/', contacto, name='contacto'),
    path('success/', success, name='success'),
    path('registro/', add_user, name='user'), 
    path('registro_exitoso/', registro_exitoso, name='registro_exitoso'), 
    path('producto/<int:producto_id>/opinion/', crear_opinion, name='crear_opinion'),
    path('producto/<int:producto_id>/opiniones/', opiniones_producto, name='opiniones_producto'),
    path('accounts/', include('django.contrib.auth.urls'))     
                                           
]