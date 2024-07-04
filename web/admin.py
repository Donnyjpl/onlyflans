from django.contrib import admin
from .models import Flan, Contacto, Usuario, OpinionCliente


# Register your models here.

@admin.register(Flan)
class FlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image_url', 'is_private')
    search_fields = ('name', 'description')

@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'customer_email', 'contacted', 'date_contacted')
    search_fields = ('customer_name', 'customer_email')
    readonly_fields = ('contact_form_uuid',)

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'telefono', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'telefono')

@admin.register(OpinionCliente)
class OpinionClienteAdmin(admin.ModelAdmin):
    list_display = ('producto', 'nombre_cliente', 'valoracion', 'created_at')
    search_fields = ('producto__name', 'nombre_cliente')
    readonly_fields = ('producto', 'created_at')
