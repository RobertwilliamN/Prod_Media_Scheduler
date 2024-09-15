from django import forms
from .models import Publicacao, Perfil, RedeSocial


class PublicacaoForm(forms.ModelForm):
    class Meta:
        model = Publicacao
        fields = ['foto_video', 'descricao', 'data_agendada', 'status', 'perfil']
        widgets = {
            'foto_video': forms.FileInput(attrs={'class': 'form-control upload-input'}),
            'perfil': forms.SelectMultiple(attrs={'class': 'form-control perfil-select'}),
            'descricao': forms.Textarea(attrs={'placeholder': 'Digite a descrição da publicação'}),
            'data_agendada': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                
                },
                format='%Y-%m-%dT%H:%M'
            ),
        }
        labels = {
            'foto_video': 'Enviar Foto/Vídeo',
            'descricao': 'Descrição',
            'data_agendada': 'Data de Agendamento',
            'status': 'Status',
            'perfil': 'Selecione um Perfil',
        }
        def __init__(self, *args, **kwargs):
            super(PublicacaoForm, self).__init__(*args, **kwargs)
            if self.instance and self.instance.pk and self.instance.foto_video:
                 self.fields['foto_video'].label = f"Arquivo atual: {self.instance.foto_video.name} (Alterar para outro arquivo)"
    

class PublicacaoFilterForm(forms.Form):
    STATUS_CHOICES = [
        ('', 'Todos'),
        ('Agendado', 'Agendado'),
        ('Postado', 'Postado'),
    ]

    pais = forms.ChoiceField(
        choices=[('', 'Todos')] + [(perfil['pais'], perfil['pais']) for perfil in Perfil.objects.values('pais').distinct()],
        required=False,
        label='País'
    )

    perfil = forms.ModelChoiceField(queryset=Perfil.objects.all(), required=False, label='Perfil')
    #rede_social = forms.ModelChoiceField(queryset=RedeSocial.objects.all(), required=False, label='Rede Social')
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False, label='Status')
    data_inicio = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label='Data Início')
    data_fim = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label='Data Fim')
