from django.core.management.base import BaseCommand
from compra.models import Carrito  # Asegúrate de que la ruta sea correcta
from django.utils import timezone

class Command(BaseCommand):
    help = 'Elimina carritos que han expirado'

    def handle(self, *args, **kwargs):
        expired_carts = Carrito.objects.filter(creado__lt=timezone.now() - timezone.timedelta(hours=1))
        count = expired_carts.count()
        expired_carts.delete()
        self.stdout.write(self.style.SUCCESS(f'Se han eliminado {count} carritos expirados.'))
