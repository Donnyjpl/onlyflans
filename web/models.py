from django.db import models
from django.utils.text import slugify 
import uuid
from django.contrib.auth.models import AbstractUser

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
    
    
class Contacto(models.Model):
    contact_form_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    customer_name = models.CharField(max_length=64)
    customer_email = models.EmailField()
    message = models.TextField()
        
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