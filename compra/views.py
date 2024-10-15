from django.shortcuts import render, redirect
from .models import Carrito, CarritoFlan, OrdenCompra
from web.models import Flan
from django.http import JsonResponse
import mercadopago
from django.conf import settings
from django.shortcuts import redirect, render
from .models import Carrito, OrdenCompra
from django.http import JsonResponse

def procesar_pago(request):
    carrito = Carrito.objects.filter(usuario=request.user).first()
    
    # Configuración del SDK de Mercado Pago en modo sandbox
    sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
    
    # Configuración de la preferencia
    preference_data = {
        "items": [
            {
                "title": "Compra en OnlyFlans",
                "quantity": 1,
                "unit_price": float(carrito.total)
            }
        ],
        "back_urls": {
            "success": request.build_absolute_uri('/compra/confirmacion/'),
            "failure": request.build_absolute_uri('/compra/fallo/'),
            "pending": request.build_absolute_uri('/compra/pendiente/')
        },
        "auto_return": "approved",
    }
    
    # Crear la preferencia en modo sandbox
    preference_response = sdk.preference().create(preference_data)
    print("Respuesta de Mercado Pago:", preference_response)  # Para revisar la respuesta completa
    preference = preference_response.get("response", {})

    # Redirigir al sandbox_init_point para pruebas
    if 'sandbox_init_point' in preference:
        return redirect(preference["sandbox_init_point"])
    else:
        return JsonResponse({'error': 'No se pudo generar el enlace de pago de prueba.'}, status=400)

def confirmacion_pago(request):
    return render(request, 'confirmacion.html')

def fallo_pago(request):
    return render(request, 'fallo.html')

def pendiente_pago(request):
    return render(request, 'pendiente.html')

def agregar_al_carrito(request, slug):
    if request.method == 'POST':
        try:
            carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
            flan = Flan.objects.get(slug=slug)
            item, created = CarritoFlan.objects.get_or_create(carrito=carrito, flan=flan)
            if not created:
                item.cantidad += 1
            item.save()
            return JsonResponse({'success': True})
        except Flan.DoesNotExist:
            return JsonResponse({'error': 'Producto no encontrado'}, status=404)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def ver_carrito(request):
    carrito = Carrito.objects.filter(usuario=request.user).first()
    return render(request, 'carrito.html', {'carrito': carrito})