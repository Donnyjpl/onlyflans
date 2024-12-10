from django.urls import path
from .views import agregar_al_carrito, ver_carrito, procesar_pago,confirmacion_pago
from .views import   fallo_pago, pendiente_pago,actualizar_cantidad,eliminar_flan,eliminar_carrito

urlpatterns = [
    path('agregar/<slug:slug>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', ver_carrito, name='ver_carrito'),
    path('eliminar_carrito/<int:carrito_id>/', eliminar_carrito, name='eliminar_carrito'),
    
    
    
    path('pago/', procesar_pago, name='procesar_pago'),
    path('confirmacion/', confirmacion_pago, name='confirmacion_pago'),
    path('fallo/', fallo_pago, name='fallo_pago'),
    path('pendiente/', pendiente_pago, name='pendiente_pago'),
    

    
    path('actualizar/<slug:slug>/', actualizar_cantidad, name='actualizar_cantidad'),
    path('eliminar/<slug:slug>/', eliminar_flan, name='eliminar_flan'),
    ]
