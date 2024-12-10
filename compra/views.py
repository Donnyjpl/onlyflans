from django.shortcuts import render, redirect
from .models import Carrito, CarritoFlan, Flan, OrdenCompra
from web.models import Flan
from django.http import JsonResponse
import mercadopago
from django.conf import settings
import requests
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required  # Para verificar si el usuario
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator
import logging

logger = logging.getLogger(__name__)

def obtener_tasa_cambio(base_currency, target_currency):
    api_key = 'd566bb4382ccd449a0a569adc8213351'
    url = f'https://data.fixer.io/api/latest?access_key={api_key}&base={base_currency}&symbols={target_currency}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data.get('success'):
            return data['rates'].get(target_currency)
        else:
            error_message = data.get('error', {}).get('info', 'Error desconocido')
            raise Exception(f"Error al obtener la tasa de cambio: {error_message}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error de red: {str(e)}")

# Cambiar la moneda base a USD
def vista_producto(request):
    precio_clp = 1000  # Precio en pesos chilenos
    moneda = 'USD'  # Define la moneda de destino
    precio_convertido = None  # Inicializa la variable

    try:
        # Obtener las tasas de cambio
        tasa_clp = obtener_tasa_cambio('EUR', 'CLP')
        tasa_usd = obtener_tasa_cambio('EUR', 'USD')

        if tasa_clp is None or tasa_usd is None:
            raise Exception("Tasa de cambio no válida")

        # Convertir de CLP a USD
        precio_convertido = (precio_clp / tasa_clp) * tasa_usd
        mensaje = f"Precio en {moneda}: {precio_convertido:.2f} {moneda}"
    except Exception as e:
        mensaje = str(e)

    return render(request, 'producto.html', {
        'mensaje': mensaje,
        'precio_clp': precio_clp,
        'precio_convertido': precio_convertido,
        'moneda': moneda
    })



def procesar_pago(request):
    # Asegúrate de que el usuario esté autenticado
    if not request.user.is_authenticated:
        return redirect('login')  # Redirigir a la página de inicio de sesión

    carrito = Carrito.objects.filter(usuario=request.user).first()
    if not carrito or carrito.total <= 0:
        return JsonResponse({'error': 'El carrito está vacío o no tiene un total válido.'}, status=400)
    
    total_en_clp = float(carrito.total) if carrito else 0

    # Obtener la moneda local del usuario
    moneda_local = obtener_moneda_local(request.user.pais)
    
    # Solo trabajamos en CLP para este ejemplo
    total_en_moneda_local_int = round(total_en_clp)

    # Configuración del SDK de Mercado Pago
    sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)

    # Configuración de la preferencia
    preference_data = {
        "items": [
            {
                "title": "Compra en OnlyFlans",
                "quantity": 1,
                "unit_price": total_en_moneda_local_int  # Usar precio en CLP
            }
        ],
        "back_urls": {
            "success": request.build_absolute_uri('/compra/confirmacion/'),
            "failure": request.build_absolute_uri('/compra/fallo/'),
            "pending": request.build_absolute_uri('/compra/pendiente/')
        },
        "auto_return": "approved",
    }

    # Crear la preferencia en Mercado Pago
    try:
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response.get("response", {})
        
        if 'init_point' in preference:
            return redirect(preference["init_point"])  # Redirigir al usuario a la página de pago
        else:
            error_message = preference_response.get("message", "Error desconocido.")
            return JsonResponse({'error': error_message}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def obtener_moneda_local(pais):
    # Mapa simple de países a monedas
    monedas = {
        'CL': 'CLP',  # Chile
        'PE': 'PEN',  # Perú
        # Agrega más países y sus monedas aquí
    }
    return monedas.get(pais, 'CLP')  # Devuelve CLP si el país no está en el mapa

# Resto de las funciones...



def confirmacion_pago(request):
    # Aquí puedes obtener información de la transacción desde Mercado Pago
    # Por ejemplo, podrías recibir un ID de pago o parámetros de consulta.

    if request.method == "GET":
        # Aquí deberías realizar la lógica para verificar el estado del pago
        # Puedes usar el SDK de Mercado Pago para verificar el estado
        # Ejemplo:
        payment_id = request.GET.get('payment_id')  # Asume que obtienes este ID
        sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
        
        payment_response = sdk.payment().get(payment_id)
        payment_info = payment_response.get("response", {})
        
        # Verifica si el pago fue exitoso
        if payment_info.get("status") == "approved":
            # Si el pago fue exitoso, puedes crear la orden de compra
            carrito = Carrito.objects.filter(usuario=request.user).first()
            if carrito:
                orden = OrdenCompra.objects.create(
                    carrito=carrito,
                    total=carrito.total,
                    pagado=True,
                    fecha_pago=timezone.now()
                    )
                 # Actualizar los productos del carrito para asignarles la orden de compra
                for item in carrito.carritoflan_set.filter(orden_compra__isnull=True):
                    item.orden_compra = orden
                    item.save()
                # Puedes redirigir a una página de éxito o mostrar un mensaje
                return render(request, 'confirmacion.html', {'orden': orden})
        else:
            # Manejar el caso de pago fallido
            return render(request, 'fallo.html', {'error': 'El pago no fue exitoso.'})
    
    return redirect('error')  # Manejo de errores si no es un GET

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

# def ver_carrito(request):
#     carrito = Carrito.objects.filter(usuario=request.user).first()
#     return render(request, 'carrito.html', {'carrito': carrito})
@login_required
def ver_carrito(request):
    # Busca el carrito existente del usuario
    carrito = Carrito.objects.filter(usuario=request.user).first()

    # Verifica si el carrito existe
    if carrito:
        # Comprueba si hay una orden pagada asociada con este carrito
        orden_pagada = OrdenCompra.objects.filter(carrito=carrito, pagado=True).exists()

        if orden_pagada:
            # Si hay una orden pagada, crea un nuevo carrito
            carrito = Carrito.objects.create(usuario=request.user)
            messages.info(request, 'Tu orden anterior ha sido pagada. Se ha creado un nuevo carrito.')

    else:
        # Si no hay carrito, crea uno nuevo
        carrito = Carrito.objects.create(usuario=request.user)
        messages.info(request, 'Tu carrito está vacío. ¡Explora nuestros productos!')

    # Filtrar productos no pagados
    productos_no_pagados = carrito.carritoflan_set.filter(orden_compra__isnull=True)

    total_en_clp = carrito.total if carrito else 0
    moneda_local = 'PEN'  # Cambia según la lógica de tu aplicación
    total_en_moneda_local = 0  # Inicializamos la variable

    if total_en_clp > 0:
        try:
            tasa_eur_a_clp = obtener_tasa_cambio('EUR', 'CLP')
            tasa_eur_a_pen = obtener_tasa_cambio('EUR', moneda_local)

            if tasa_eur_a_clp and tasa_eur_a_pen:
                total_en_eur = float(total_en_clp) / float(tasa_eur_a_clp)  # Convertir a float
                total_en_moneda_local = total_en_eur * float(tasa_eur_a_pen)  # Convertir a float
            else:
                logger.error("Error al obtener tasas de cambio.")
        except Exception as e:
            logger.exception("Error en el cálculo de tasas de cambio: %s", e)

    return render(request, 'carrito.html', {
        'productos_no_pagados': productos_no_pagados,
        'carrito': carrito,
        'total_en_moneda_local': total_en_moneda_local,
        'moneda_local': moneda_local,
    })



@login_required
def eliminar_flan(request, slug):
    carrito = get_object_or_404(Carrito, usuario=request.user)
    flan = get_object_or_404(Flan, slug=slug)
    carrito_flan = get_object_or_404(CarritoFlan, carrito=carrito, flan=flan)
    carrito_flan.delete()
    return JsonResponse({'success': True})

@csrf_exempt
@login_required
def actualizar_cantidad(request, slug):
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 0))
        flan = get_object_or_404(Flan, slug=slug)
        carrito = get_object_or_404(Carrito, usuario=request.user)
        carrito_flan = get_object_or_404(CarritoFlan, carrito=carrito, flan=flan)
         # Imprimir información para depuración
        print(f'Actualizando flan: {flan.name}, nueva cantidad: {cantidad}')
        if cantidad <= 0:
            carrito_flan.delete()
        else:
            carrito_flan.cantidad = cantidad
            carrito_flan.save()

        return JsonResponse({'success': True, 'message': 'Cantidad actualizada.'})

    return JsonResponse({'error': 'Método no permitido.'}, status=405)
@login_required
def eliminar_carrito(request, carrito_id):
    if request.method == 'POST':
        carrito = get_object_or_404(Carrito, id=carrito_id)

        # Verificar si hay órdenes asociadas y si están pagadas
        if carrito.ordencompra_set.filter(pagado=False).exists():
            # Si hay órdenes no pagadas, elimina el carrito
            carrito.delete()
            return JsonResponse({'success': True, 'message': 'Carrito eliminado.'})
        else:
            return JsonResponse({'success': False, 'message': 'No se puede eliminar el carrito porque contiene órdenes pagadas.'})

    return JsonResponse({'success': False, 'message': 'Método no permitido.'})

