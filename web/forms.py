from django import forms
from .models import Flan, Contacto,Usuario,OpinionCliente

class FlanForm(forms.ModelForm):
    class Meta:
        model = Flan
        fields = ['name', 'description', 'image_url', 'is_private']
        # Puedes personalizar las etiquetas de los campos aquí si lo deseas
        labels = {
            'name': 'Nombre',
            'description': 'Descripción',
            'image_url': 'URL de la Imagen',
            'is_private': '¿Es privado?',
        }
class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['customer_name','customer_email', 'message']
        labels = {
            'customer_name': 'Nombre:',
            'customer_email': 'Correo Electrónico:',
            'message': 'Mensaje:',
        }
        widgets = {
            'message': forms.Textarea(attrs={'cols': 30, 'rows': 3}),  # Ajusta el tamaño del TextArea
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
    username = forms.CharField(label='Nombre de usuario')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    
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