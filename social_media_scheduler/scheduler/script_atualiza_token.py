import os
import sys
from datetime import datetime, timedelta
import django
import pytz
import requests

# Adicione o caminho do projeto ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configura o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_scheduler.settings')
django.setup()

from publicacao.models import Perfil

def get_long_lived_token(short_lived_token, app_id, app_secret):
    """Obtém um token de longo prazo a partir de um token de curto prazo usando as credenciais da aplicação."""
    url = 'https://graph.facebook.com/v14.0/oauth/access_token'
    params = {
        'grant_type': 'fb_exchange_token',
        'fb_exchange_token': short_lived_token,
        'client_id': app_id,
        'client_secret': app_secret,
    }
    response = requests.post(url, params=params)
    data = response.json()
    return data.get('access_token'), data.get('expires_in')

def atualizar_tokens_facebook():
    local_tz = pytz.timezone('America/Sao_Paulo')  
    agora_local = datetime.now(local_tz)

    print(f"Data e hora atual (local): {agora_local}")

    perfis = Perfil.objects.all()  # Carrega todos os perfis

    for perfil in perfis:
        if perfil.rede_social == 'Facebook':
            if perfil.token:  # Verifica se o perfil tem um token
                new_token, expires_in = get_long_lived_token(perfil.token, perfil.app_id, perfil.app_secret)
                if new_token:
                    expiry_date = datetime.now() + timedelta(seconds=expires_in)
                    perfil.token = new_token
                    perfil.token_expires_at = expiry_date
                    perfil.save()
                    print(f"Token atualizado para o perfil {perfil.id}. Novo token: {new_token}")
                else:
                    print(f"Erro ao atualizar o token para o perfil {perfil.id}: data.get('error')")
            else:
                print(f"Nenhum token encontrado para o perfil {perfil.id}")
        else:
           atualiza_token_instagram(perfil.token, perfil.app_secret, perfil.id)


def atualiza_token_instagram(access_token, app_secret, perfil):
    print('Atualizando token Instagram para o perfil:', perfil)

    if not access_token:
        print(f"Nenhum token encontrado para o perfil {perfil}.")
        return {"success": False, "error": "Nenhum token encontrado", "Perfil": perfil}

    try:
        # URL para estender o token
        url = f"https://graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token&access_token={access_token}&client_secret={app_secret}"
        
        # Requisição para obter o token de longo prazo
        response = requests.get(url)

        # Imprime o status e o conteúdo da resposta para depuração
        print(f"Status da resposta: {response.status_code}")
        print(f"Resposta: {response.text}")

        long_lived_token_data = response.json()

        # Verifica se a resposta contém o token de longo prazo
        if 'access_token' in long_lived_token_data:
            return {"success": True, "access_token": long_lived_token_data['access_token'], "Perfil": perfil}
        else:
            return {"success": False, "error": long_lived_token_data, "Perfil": perfil}

    except Exception as e:
        return {"success": False, "error": str(e), "Perfil": perfil}

if __name__ == "__main__":
    atualizar_tokens_facebook()
