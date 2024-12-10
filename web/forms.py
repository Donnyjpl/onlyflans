from django import forms
from .models import Flan, Contacto,Usuario,OpinionCliente
from django.contrib.auth.forms import SetPasswordForm


class CustomPasswordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="Nueva Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu nueva contraseña'}),
    )
    new_password2 = forms.CharField(
        label="Confirmar Nueva Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirma tu nueva contraseña'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
    
    
class CustomEmailForm(forms.Form):
    email = forms.EmailField(
        label="Correo Electrónico",
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu correo electrónico'}),
    )
    
class FlanForm(forms.ModelForm):
    class Meta:
        model = Flan
        fields = ['name', 'description', 'precio','image_url', 'is_private']
        # Puedes personalizar las etiquetas de los campos aquí si lo deseas
        labels = {
            'name': 'Nombre',
            'description': 'Descripción',
            'image_url': 'URL de la Imagen',
            'precio': 'Precio del Producto',
            'is_private': '¿Es privado?',
        }
class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['customer_name', 'customer_email', 'message']
        labels = {
            'customer_name': 'Nombre:',
            'customer_email': 'Correo Electrónico:',
            'message': 'Mensaje:',
        }
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',  # Clase de Bootstrap
                'placeholder': 'Ingresa tu nombre',  # Placeholder
            }),
            'customer_email': forms.EmailInput(attrs={
                'class': 'form-control',  # Clase de Bootstrap
                'placeholder': 'Ingresa tu correo electrónico',  # Placeholder
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',  # Clase de Bootstrap
                'cols': 30,
                'rows': 3,
                'placeholder': 'Escribe tu mensaje aquí...',  # Placeholder
            }),
        }
      
class UsuarioForm(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'telefono']  # Incluye los campos que quieres en el formulario de registro
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
            'telefono': 'Teléfono',
        }
        error_messages = {
            'username': {
                'unique': 'Ya existe un usuario con ese nombre de usuario. Por favor, elige otro.',
            }
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None  # Elimina el mensaje de ayuda del campo username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # Utiliza set_password para guardar la contraseña de manera segura
        if commit:
            user.save()
            
class LoginForm(forms.Form):
    username = forms.CharField(
        label='Nombre de usuario',
        widget=forms.TextInput(attrs={
            'class': 'form-control',  # Clase de Bootstrap
            'placeholder': 'Ingresa tu nombre de usuario',  # Placeholder
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',  # Clase de Bootstrap
            'placeholder': 'Ingresa tu contraseña',  # Placeholder
        })
    )
class OpinionClienteForm(forms.ModelForm):
    # Campo para valoración del 1 al 5
    valoracion = forms.ChoiceField(label='Valoración', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')],
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    
    # Campo oculto para guardar automáticamente el nombre de usuario
    nombre_cliente = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = OpinionCliente
        fields = ['nombre_cliente', 'opinion', 'valoracion']
        widgets = {
            'opinion': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),  # Widget para un área de texto multilínea
        }