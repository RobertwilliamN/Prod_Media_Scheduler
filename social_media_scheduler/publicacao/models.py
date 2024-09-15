# publicacao/models.py
from django.db import models
from perfil.models import Perfil  
import os

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
        if self.foto_video:
            if os.path.isfile(self.foto_video.path):
                os.remove(self.foto_video.path)
        super(Publicacao, self).delete(*args, **kwargs)