# publicacao/models.py
from django.db import models
from perfil.models import Perfil  
import os
from publicacao_bau.models import Publicacao_Bau  # Ajuste o caminho conforme necessário

class RedeSocial(models.Model):
    nome = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.nome

class Publicacao(models.Model):
    STATUS_CHOICES = [
        ('Agendado', 'Agendado'),
        ('Postado', 'Postado'),
    ]

    foto_video = models.FileField(upload_to='uploads/', blank=True, null=True, max_length=120)
    descricao = models.TextField()
    data_agendada = models.DateTimeField()
    rede_social = models.ManyToManyField(RedeSocial)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Agendado')
    perfil = models.ManyToManyField(Perfil)  
    post_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        redes = ", ".join([rede.nome for rede in self.rede_social.all()])
        return f"{self.descricao[:50]} - {redes}"
    
    def delete(self, *args, **kwargs):
        #if self.foto_video:
            #if os.path.isfile(self.foto_video.path):
                # os.remove(self.foto_video.path)
        super(Publicacao, self).delete(*args, **kwargs)


class RegistroPostagem(models.Model):
    publicacao_bau = models.ForeignKey(Publicacao_Bau, on_delete=models.CASCADE)  # Corrigido para letra minúscula
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    data_postagem = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('publicacao_bau', 'perfil')  # Corrigido para 'publicacao_bau' em minúsculas

    def __str__(self):
        return f"{self.publicacao_bau.descricao} - {self.perfil.nome}"


