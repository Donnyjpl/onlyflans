from django import forms
from .models import Flan, ContactForm,Usuario

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
class ContactFormForm(forms.ModelForm):
    class Meta:
        model = ContactForm
        fields = ['customer_name','customer_email', 'message']
        labels = {
            'customer_name': 'Nombre:',
            'customer_email': 'Correo Electrónico:',
            'message': 'Mensaje:',
        }
        widgets = {
            'message': forms.Textarea(attrs={'cols': 30, 'rows': 3}),  # Ajusta el tamaño del TextArea
        }
        
        
class ContactFormModelForm(forms.ModelForm):
    class Meta:
        model = ContactForm
        fields = ['customer_email', 'customer_name', 'message']
      
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

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # Utiliza set_password para guardar la contraseña de manera segura
        if commit:
            user.save()