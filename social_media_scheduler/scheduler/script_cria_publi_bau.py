import os
import sys
import random
from datetime import datetime
import django
from django.utils import timezone

# Adicione o caminho do projeto ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configura o Django antes de importar os modelos
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_scheduler.settings')
django.setup()

# Importações após a configuração do Django
from publicacao_bau.models import Publicacao_Bau
from publicacao.models import Publicacao, RegistroPostagem
from perfil.models import Perfil

def obter_perfis_disponiveis(hoje):
    """
    Obtém perfis que ainda não receberam uma publicação no dia corrente.
    """
    perfis_postados_hoje = RegistroPostagem.objects.filter(
        data_postagem__date=hoje
    ).values_list('perfil_id', flat=True)

    perfis_disponiveis = Perfil.objects.exclude(id__in=perfis_postados_hoje)
    
    return list(perfis_disponiveis)

def obter_publicacao_aleatoria_por_pais_e_perfil(pais, perfil):
    """
    Retorna uma publicação aleatória do Baú do mesmo país, garantindo que
    não tenha sido postada anteriormente pelo perfil especificado.
    """
    publicacoes_bau = Publicacao_Bau.objects.filter(pais=pais)
    
    if not publicacoes_bau.exists():
        return None

    # Tenta até 5 vezes encontrar uma publicação que ainda não tenha sido postada pelo perfil
    for _ in range(5):
        publicacao_aleatoria = random.choice(publicacoes_bau)
        
        # Verifica se a publicação já foi usada por este perfil específico
        if not RegistroPostagem.objects.filter(publicacao_bau=publicacao_aleatoria, perfil=perfil).exists():
            return publicacao_aleatoria

    return None  # Retorna None se não encontrar uma publicação disponível

def vincular_publicacoes_bau(lote=5):
    """
    Vincula publicações do Baú a perfis em lotes, validando o país e garantindo aleatoriedade.
    As postagens só ocorrerão se o país do perfil e da publicação forem os mesmos.
    Não repete postagens para o mesmo perfil.
    """
    # Obtém a hora atual
    agora = timezone.localtime()
    hora_atual = agora.time()

    # Define o horário de início e término (08:00 e 19:00)
    hora_inicio = datetime.strptime("08:00", "%H:%M").time()
    hora_fim = datetime.strptime("19:00", "%H:%M").time()

    # Verifica se o horário atual está fora do intervalo permitido
    if hora_atual < hora_inicio or hora_atual > hora_fim:
        print(f"Fora do horário permitido: {hora_atual}. O script só roda entre 08:00 e 19:00.")
        return

    hoje = timezone.localdate()
    print("Data de Hoje: ", hoje)
    
    perfis_disponiveis = obter_perfis_disponiveis(hoje)
    
    if not perfis_disponiveis:
        print("Todos os perfis já receberam publicações hoje.")
        return

    # Seleciona perfis de forma aleatória
    perfis_para_postar = random.sample(perfis_disponiveis, min(lote, len(perfis_disponiveis)))
    data_agendada = timezone.make_aware(datetime.now(), timezone.get_current_timezone())

    for perfil in perfis_para_postar:
        print(f"Processando perfil: {perfil.id} - {perfil.nome} - País: {perfil.pais}")

        # Obtém uma publicação aleatória disponível para o país do perfil e que ainda não foi postada por este perfil
        publicacao_bau = obter_publicacao_aleatoria_por_pais_e_perfil(perfil.pais, perfil)

        if not publicacao_bau:
            print(f"Não há publicações disponíveis para o perfil {perfil.nome} ({perfil.pais})")
            continue

        print(f"Publicação encontrada para o perfil {perfil.nome}: {publicacao_bau.descricao} ({publicacao_bau.pais})")

        # Criando uma nova publicação
        nova_publicacao = Publicacao.objects.create(
            foto_video=publicacao_bau.foto_video,
            descricao=publicacao_bau.descricao,
            data_agendada=data_agendada,
            status='Agendado'
        )

        nova_publicacao.perfil.add(perfil)

        # Registrar a postagem para evitar duplicações
        RegistroPostagem.objects.create(
            publicacao_bau=publicacao_bau,
            perfil=perfil,
            data_postagem=data_agendada
        )
        
        print(f"Publicação agendada criada com sucesso: {nova_publicacao.descricao}")

# Executa a função para vincular publicações
if __name__ == "__main__":
    vincular_publicacoes_bau()

