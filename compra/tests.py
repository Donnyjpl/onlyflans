from django.test import TestCase
from web.models import Flan
from .models import Carrito

class CarritoTestCase(TestCase):
    def setUp(self):
        self.producto = Flan.objects.create(nombre='Flan', precio=100)
        self.carrito = Carrito.objects.create()  # Asegúrate de que Carrito esté definido correctamente

    def test_agregar_producto_al_carrito(self):
        self.carrito.agregar_producto(self.producto)
        self.assertIn(self.producto, self.carrito.productos.all())

    def test_eliminar_producto_del_carrito(self):
        self.carrito.agregar_producto(self.producto)
        self.carrito.eliminar_producto(self.producto)
        self.assertNotIn(self.producto, self.carrito.productos.all())

