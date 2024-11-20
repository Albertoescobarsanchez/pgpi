from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label="Correo Electrónico"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Contraseña"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirmar Contraseña"
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        labels = {
            'username': 'Nombre de Usuario',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'username': None,  
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 4:
            raise forms.ValidationError("El nombre de usuario debe tener al menos 4 caracteres.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está en uso. Por favor, ingrese otro.")
        return email
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        try:
            validate_password(password)
        except ValidationError as e:
            raise forms.ValidationError(e)
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data
