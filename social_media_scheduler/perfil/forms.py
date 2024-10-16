from django import forms
from .models import Perfil

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['nome', 'token', 'page_id', 'app_id', 'app_secret', 'rede_social','pais']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Digite um nome para o Perfil'}),
            'token': forms.TextInput(attrs={'placeholder': 'Digite o Token da página'}),
            'page_id': forms.TextInput(attrs={'placeholder': 'Digite o Page/User ID'}),
            'app_id': forms.TextInput(attrs={'placeholder': 'Digite o APP ID'}),
            'app_secret': forms.TextInput(attrs={'placeholder': 'Digite o APP Secret'}),
            'rede_social': forms.Select(attrs={'class': 'form-select'}),
            'pais': forms.Select(attrs={'class': 'form-select'})
        }
