from django.http import JsonResponse, Http404, HttpResponse
from perfil.models import Perfil  # Importe o modelo Perfil
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import requests
import folium
import geopandas as gpd
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from geopy.geocoders import Nominatim
from .models import Localizacao
from .forms import MapaForm
import os
from dotenv import load_dotenv

# Carregar o .env
load_dotenv()

# Defina seu token padrão aqui (ou obtenha-o de um arquivo de configuração)
TOKEN_PADRAO = os.getenv('TOKEN_SECRET').strip()

# Capturando as coordernadas
def get_coordinates(endereco):
    # Inicializando o geocoder
    geolocator = Nominatim(user_agent="meu_app")

    # Geocodificando o endereço
    location = geolocator.geocode(endereco)

    if location:
        return location.latitude, location.longitude
    else:
        return None, None
    
# Atualiza as informações de coordenadas a partir do endereço do banco
def atualizar_coordenadas(loc):
    # Obtém o endereço do objeto
    endereco = loc.endereco  # Supondo que o campo do endereço se chama 'endereco'
    
    # Obter as coordenadas
    latitude, longitude = get_coordinates(endereco)
    
    # Atualiza a localização com as novas coordenadas
    loc.latitude = latitude
    loc.longitude = longitude
    loc.save()  # Salva as alterações no banco de dados
    if latitude is not None and longitude is not None:
        print(f"Atualizado: {endereco} - Latitude: {latitude}, Longitude: {longitude}")
    else:
        print(f"Endereço não encontrado: {endereco}")


#Metodos para views da página mapa
@method_decorator(login_required, name='dispatch')
class MapaListView(ListView):
    model = Localizacao
    template_name = 'list_mapas.html'
    context_object_name = 'enderecos'
    
@method_decorator(login_required, name='dispatch')
class MapaCreateView(CreateView):
    model = Localizacao
    form_class = MapaForm
    template_name = 'cria_edita_mapa.html'
    success_url = reverse_lazy('MapaListView')

    def form_valid(self, form):
        response = super().form_valid(form)  # Salva o objeto no banco de dados
        atualizar_coordenadas(self.object)  # Chama a função passando o objeto recém-criado
        return response

@method_decorator(login_required, name='dispatch')
class MapaUpdateView(UpdateView):
    model = Localizacao
    form_class = MapaForm
    template_name = 'cria_edita_mapa.html'
    success_url = reverse_lazy('MapaListView')
    
    def form_valid(self, form):
        response = super().form_valid(form)  # Salva o objeto no banco de dados
        atualizar_coordenadas(self.object)  # Chama a função passando o objeto recém-criado
        return response

@method_decorator(login_required, name='dispatch')
class MapaDeleteView(DeleteView):
    model = Localizacao
    template_name = 'publicacao_confirm_delete.html'
    success_url = reverse_lazy('MapaListView')
    
@method_decorator(login_required, name='dispatch')
class MapasView(TemplateView):
    template_name = 'mapas_criados.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Buscando cidades distintas
        context['enderecos'] = Localizacao.objects.values('cidade').distinct()
        return context


def get_instagram_info(request, perfil_nome):
    try:
        # Obtenha o token dos parâmetros da URL
        token = request.GET.get('Token').strip()
        
        # Validação do token
        if token != TOKEN_PADRAO:
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


def get_mapa(request, cidade):
    # Atualiza as coordenadas das localizações
    #atualizar_coordenadas()

    # Busca as localizações filtradas pelo estado
    localizacoes = Localizacao.objects.filter(cidade=cidade.upper())  # Filtra pelo estado
    # localizacoes = Localizacao.objects.filter(cidade__iexact=cidade.upper())
    # Adicionando um print para verificar as localizações

    print(localizacoes)

    for loc in localizacoes:
        print(f"Endereço: {loc.endereco}, Latitude: {loc.latitude}, Longitude: {loc.longitude}")
        
    # Criando o mapa com o ponto inicial definido
    mapa = folium.Map(location=[loc.latitude, loc.longitude], zoom_start=13)

    popup_content = f'<div style="font-size: 14px; color: green; font-weight: bold;">Obra - Protege Piso</div>'
    
    # Adicionando camadas de estilo com atribuições
    #folium.TileLayer('Stamen Terrain', attr='Map tiles by Stamen Design, under CC BY 3.0.').add_to(mapa)
    #folium.TileLayer('Stamen Toner', attr='Map tiles by Stamen Design, under CC BY 3.0.').add_to(mapa)
    #folium.TileLayer('Stamen Watercolor', attr='Map tiles by Stamen Design, under CC BY 3.0.').add_to(mapa)
    #folium.TileLayer('CartoDB positron', attr='Map tiles by CartoDB').add_to(mapa)
    #folium.TileLayer('CartoDB dark_matter', attr='Map tiles by CartoDB').add_to(mapa)
    
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Tiles © Esri & the GIS User Community',
        name='Esri Satellite'
    ).add_to(mapa)
    
    # Adicionando controle de camadas
    folium.LayerControl().add_to(mapa)

    # Adicionando marcadores para cada localização
    for loc in localizacoes:
        popup_content = f'<div style="font-size: 14px; color: green; font-weight: bold;">Obra - Protege Piso {loc.estado}</div>'
        if loc.latitude is not None and loc.longitude is not None:
            # Adicionando um marcador no mapa
            folium.Marker(
                location=[loc.latitude, loc.longitude],
                popup=folium.Popup(popup_content, max_width=200),
                icon=folium.Icon(color='green')
            ).add_to(mapa)
        else:
            print(f"Coordenadas não encontradas para: {loc.endereco}")

 # Gerando o HTML do mapa
    mapa_html = f'''
    <div style="width: 100%; height: 80%; overflow: hidden;">
        {mapa._repr_html_()}
    </div>
    <style>
        html, body {{
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
        }}

        /* Media Query para telas menores */
        @media (max-width: 768px) {{
            div {{
                height: 50vh; /* Ajusta a altura para 50% da viewport em telas menores */
            }}
        }}
    </style>
    '''
    return HttpResponse(mapa_html, content_type='text/html')

