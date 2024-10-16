from django import forms
from .models import Localizacao

class MapaForm(forms.ModelForm):
    class Meta:
        model = Localizacao
        fields = ['estado', 'endereco', 'bairro', 'cidade']  # Campos relevantes para o endereço
        widgets = {
            'estado': forms.Select(attrs={'class': 'form-control'}),  # Mudou para Select
            'endereco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o endereço'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o bairro'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite a cidade'}),
        }
        labels = {
            'estado': 'Estado',
            'endereco': 'Endereço',
            'bairro': 'Bairro',
            'cidade': 'Cidade',
        }

    def __init__(self, *args, **kwargs):
        super(MapaForm, self).__init__(*args, **kwargs)
        # Adicionalmente, você pode fazer outras customizações aqui se necessário

