from django import forms
from .models import Publicacao_Bau


class PublicacaoBauForm(forms.ModelForm):
    class Meta:
        model = Publicacao_Bau
        fields = ['foto_video', 'descricao', 'pais']  # Removendo 'data_agendada'
        widgets = {
            'foto_video': forms.FileInput(attrs={'class': 'form-control upload-input'}),
            'descricao': forms.Textarea(attrs={'placeholder': 'Digite a descrição da publicação', 'class': 'form-control'}),
            'pais': forms.Select(attrs={'class': 'form-select'})
        }
        labels = {
            'foto_video': 'Enviar Foto/Vídeo',
            'descricao': 'Descrição',
        }

    def __init__(self, *args, **kwargs):
        super(PublicacaoBauForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.foto_video:
            self.fields['foto_video'].label = f"Arquivo atual: {self.instance.foto_video.name} (Alterar para outro arquivo)"

