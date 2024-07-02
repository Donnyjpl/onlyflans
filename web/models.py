from django.db import models
from django.utils.text import slugify 
import uuid
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.

class Flan(models.Model):
    flan_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=64)
    description = models.TextField()
    image_url = models.URLField()
    slug = models.SlugField(unique=True)
    is_private = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Flan, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    @property
    def promedio_valoracion(self):
        if self.opiniones.exists():
            total_valoraciones = sum(opinion.valoracion for opinion in self.opiniones.all())
            return total_valoraciones / self.opiniones.count()
        else:
            return 0  # Retorna 0 si no hay opiniones
        
class Contacto(models.Model):
    contact_form_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    customer_name = models.CharField(max_length=64)
    customer_email = models.EmailField()
    message = models.TextField()
    contacted = models.BooleanField(default=False)  # Campo para indicar si el mensaje ha sido contactado
    date_contacted = models.DateTimeField(null=True, blank=True)  # Fecha y hora en que se contactó al cliente 
  
    def __str__(self):
        return f"Formulario de Contacto - {self.contact_form_uuid}"
    
class Usuario(AbstractUser):
    # Agrega los campos personalizados si los tienes
    telefono = models.CharField(max_length=20)
    
    # Define related_name único para los campos ManyToManyField
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_users',  # Ejemplo de related_name único
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_users',  # Ejemplo de related_name único
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.'
    )
    def __str__(self):
        return self.username 
     
class OpinionCliente(models.Model):
    producto = models.ForeignKey(Flan, on_delete=models.CASCADE, related_name='opiniones')
    nombre_cliente = models.CharField(max_length=100)
    opinion = models.TextField()
    valoracion = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    created_at = models.DateTimeField(auto_now_add=True)  # Campo para la fecha de creación

    def __str__(self):
        return f'Opinión de {self.nombre_cliente} sobre {self.producto.name}'  # Acceso al nombre del producto usando self.producto.name
