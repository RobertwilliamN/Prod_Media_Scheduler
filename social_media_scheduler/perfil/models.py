from django.db import models

class Perfil(models.Model):
    REDES_SOCIAIS_CHOICES = [
        ('Facebook', 'Facebook'),
        ('Instagram', 'Instagram'),
    ]

     # Novo campo de país
    PAIS_CHOICES = [
        ('Portugal', 'Portugal'),
        ('EUA', 'EUA'),
        ('Brazil', 'Brazil'),
        # Adicione outros países conforme necessário
    ]

    nome = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
    page_id = models.CharField(max_length=255)
    app_id = models.CharField(max_length=255)
    app_secret = models.CharField(max_length=255)
    rede_social = models.CharField(max_length=50, choices=REDES_SOCIAIS_CHOICES, default="Facebook")
    pais = models.CharField(max_length=50, choices=PAIS_CHOICES, default="Brazil")

    def __str__(self):
        return f"{self.nome} ({self.rede_social})"
