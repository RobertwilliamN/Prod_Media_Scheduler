from django.contrib import admin
from .models import Publicacao, RedeSocial

@admin.register(Publicacao)
class PublicacaoAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'data_agendada', 'status')  # Remova 'rede_social' daqui
    filter_horizontal = ('rede_social',)

@admin.register(RedeSocial)
class RedeSocialAdmin(admin.ModelAdmin):
    pass


