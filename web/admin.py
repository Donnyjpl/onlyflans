from django.contrib import admin
from .models import Flan, Contacto,Usuario,OpinionCliente

# Asegúrate de importar correctamente tu modelo Flan

@admin.register(Flan)
class FlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image_url', 'is_private')  # Mostrar estos campos en la lista de Flanes
    search_fields = ('name', 'description')  # Campos por los cuales se puede buscar

# No olvides registrar tus modelos aquí si es necesario
@admin.register(Contacto)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ('customer_email', 'customer_name','message')
    search_fields = ('customer_email', 'customer_name')
    readonly_fields = ('contact_form_uuid',)  # Hace que el campo UUID sea solo de lectura

    def has_add_permission(self, request):
        return False  # Evita que se pueda agregar un formulario de contacto desde el admin
admin.site.register(Usuario)

@admin.register(OpinionCliente)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ('producto', 'nombre_cliente','opinion')
    search_fields = ('producto', 'nombre_cliente','opinion')
    readonly_fields = ('producto',)  # Hace que el campo UUID sea solo de lectura
