from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='Usuário',
        max_length=254,
        widget=forms.TextInput(attrs={
            'placeholder': 'Usuário',  
            'class': 'form-input',  
        })
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Insira sua senha', 
            'class': 'form-input',  
        })
    )

class CustomCadastroForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

       

