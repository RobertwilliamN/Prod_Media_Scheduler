from django.http import JsonResponse, Http404
from perfil.models import Perfil  # Importe o modelo Perfil
import requests
import os
from dotenv import load_dotenv

# Carregar o .env
load_dotenv()

# Defina seu token padrão aqui (ou obtenha-o de um arquivo de configuração)
#TOKEN_PADRAO = os.getenv('TOKEN_SECRET')

TOKEN_PADRAO = os.getenv('TOKEN_SECRET').strip()

def get_instagram_info(request, perfil_nome):
    try:
        # Obtenha o token dos parâmetros da URL
        Token = request.GET.get('Token').strip()
        
        # Validação do token
        if Token != TOKEN_PADRAO:
            return JsonResponse({'error': 'Token de acesso ao Webservice inválido.'}, status=403)
        
        # Busque o perfil no banco de dados pelo nome e rede social (Instagram)
        perfil = Perfil.objects.filter(nome=perfil_nome, rede_social='Instagram').first()
        
        if not perfil:
            return JsonResponse({'error': 'Perfil do Instagram não encontrado.'}, status=404)
        
        # Verifique se o perfil tem um token do Instagram
        access_token = perfil.token  # Ajuste de acordo com o campo correto do token
        
        if not access_token:
            return JsonResponse({'error': 'Token do Instagram não encontrado para este perfil.'}, status=404)

        # URL da API do Instagram para buscar informações do perfil
        url_get_profile = f"https://graph.instagram.com/me?fields=id,username,biography,followers_count,follows_count,media_count,name,profile_picture_url&access_token={access_token}"
        response_profile = requests.get(url_get_profile)
        
        url_get_media = f"https://graph.instagram.com/me/media?fields=id,caption,media_type,media_url,permalink,timestamp&access_token={access_token}"
        response_media = requests.get(url_get_media)
        
        if response_profile.status_code == 200 and response_media.status_code == 200:
            perfil_data = response_profile.json()  # Informações do perfil
            media_data = response_media.json()  # Informações das mídias
            
            # Combine as duas respostas em um único dicionário
            data = {
                'perfil': perfil_data,
                'midias': media_data
            }
            # Retorne as informações do Instagram em formato JSON
            return JsonResponse(data, status=200)
        
        else:
            # Se houver erro na requisição à API do Instagram
            return JsonResponse({'error': 'Erro ao buscar dados do Instagram', 'details': {'perfil_status': response_profile.status_code, 'media_status': response_media.status_code}}, status=500)

    except Exception as e:
        # Qualquer outro erro inesperado
        return JsonResponse({'error': str(e)}, status=500)

