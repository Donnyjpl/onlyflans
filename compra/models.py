from django.db import models
from web.models import Flan  # Asegúrate de importar el modelo Flan desde su aplicación correspondiente
from django.conf import settings

class Carrito(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    flanes = models.ManyToManyField(Flan, through='CarritoFlan')
    creado = models.DateTimeField(auto_now_add=True)

    @property
    def total(self):
        return sum(item.subtotal for item in self.carritoflan_set.all())

    def __str__(self):
        return f"Carrito {self.id} de {self.usuario}"

class CarritoFlan(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    flan = models.ForeignKey(Flan, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.flan.precio * self.cantidad

class OrdenCompra(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    pagado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_pago = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Orden {self.id} - Total: {self.total}"
