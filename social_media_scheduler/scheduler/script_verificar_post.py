import os
import sys
from datetime import datetime
import django
import pytz

# Adicione o caminho do projeto ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configura o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_scheduler.settings')
django.setup()

from publicacao.models import Publicacao
from api_post_facebook import postagem, postagem_video
from api_post_instagram import postar_no_instagram

def verificar_publicacoes():
    local_tz = pytz.timezone('America/Sao_Paulo')  
    agora_local = datetime.now(local_tz)

    print(f"Data e hora atual (local): {agora_local}")
    
    # Filtra publicações baseadas no status e rede social, e verifica a data de agendamento
    publicacoes = Publicacao.objects.filter(
        status='Agendado',
        data_agendada__lte=agora_local  # Verifica se a data de agendamento é menor ou igual a data atual
    )
    
    for publicacao in publicacoes:
        sucesso_total = True  # Mantem o rastreamento do sucesso para todos os perfis

        for perfil in publicacao.perfil.all():
            pub = {
                "page_id": perfil.page_id,
                "token": perfil.token,
                "mensagem": publicacao.descricao,
                "arquivo": publicacao.foto_video.path if publicacao.foto_video else None,
                "app_id": perfil.app_id, 
                "publicacao": publicacao,
                "rede_social": perfil.rede_social,
            }
            
            print(f"Publicação encontrada: ID={publicacao.id}, Descrição='{publicacao.descricao}', Data Agendada='{publicacao.data_agendada}', Status='{publicacao.status}', Rede Social=", perfil.rede_social)
            
            sucesso = False  # Inicializa a variável sucesso
            
            # Verificando se a rede social é Facebook
            if pub["rede_social"] == "Facebook":
                # Postar no Facebook
                
                if pub["arquivo"]:
                    file_extension = os.path.splitext(pub["arquivo"])[1].lower()
                    file_name = os.path.basename(pub["arquivo"])  # Obtém o nome do arquivo
                    file_path = pub["arquivo"]  # Mantém o caminho completo do arquivo
                    file_length = os.path.getsize(file_path)  # Obtém o tamanho do arquivo em bytes
                   
                    if file_extension in ['.jpg', '.jpeg', '.png']:
                        sucesso = postagem(pub["page_id"], pub["token"], pub["arquivo"], pub["mensagem"], pub["publicacao"])
                    elif file_extension == '.mp4':
                        file_name = os.path.basename(pub["arquivo"])
                        file_path = pub["arquivo"]
                        file_length = os.path.getsize(file_path)
                        file_type = 'video/mp4'
                        sucesso = postagem_video(pub["page_id"], pub["token"], file_name, file_path, file_length, file_type, pub["mensagem"], pub["app_id"], pub["publicacao"])
                    else:
                        print(f"Tipo de arquivo não suportado: {file_extension}")
                        sucesso = False
                else:
                    print("Nenhum arquivo para postagem")
                    sucesso = False
                    
                    
            elif pub["rede_social"] == "Instagram":
                # Postar no Instagram
                
                 # Domínio onde os arquivos serão hospedados
                dominio = "https://app.ketzim.com"
                
                caminho_arquivo = pub["arquivo"].replace("/app/social_media_scheduler", "")

                # Gera a URL combinando o domínio com o caminho relativo do arquivo
                url = dominio + caminho_arquivo
    
                #  Extrai a parte da URL, removendo o caminho até o arquivo
                #result = pub['arquivo'].split('/app/social_media_scheduler/media/', 1)[-1].strip()

                # Remove barras à esquerda e garante que a URL comece corretamente com 'https://'
                #url = result.lstrip('/')
                #if url.startswith('https:/'):
                #    url = url.replace('https:/', 'https://')  

                print("ARQUIVO", url)  
                
                
                sucesso, mensagem = postar_no_instagram(
                    image_url=url,
                    caption=pub["mensagem"],
                    access_token=pub["token"],
                    ig_user_id=pub["page_id"],
                    publicacao=pub["publicacao"],
                )
                if not sucesso:
                    print(f"Erro ao postar no Instagram: {mensagem}")
            
            # Verifica se houve falha em alguma das postagens
            if not sucesso:
                sucesso_total = False
                print(f"Erro ao realizar a postagem para o perfil {perfil.id}")

        if sucesso_total:
            publicacao.status = 'Postado'
            publicacao.save()
        else:
            print(f"Falha na postagem para um ou mais perfis para a publicação {publicacao.id}")
            publicacao.status = 'Post Error'
            publicacao.save()

if __name__ == "__main__":
    verificar_publicacoes()
