from django.urls import path
from .views import get_instagram_info, get_mapa, MapaListView,MapaDeleteView, MapaCreateView, MapaUpdateView, MapasView

urlpatterns = [
    path('get-instagram-info/<str:perfil_nome>/', get_instagram_info, name='get_instagram_info'),
    path('mapa/list/enderecos',MapaListView.as_view(),name='MapaListView'),
    path('mapa/create/',MapaCreateView.as_view(), name='create_mapa'),
    path('mapa/<int:pk>/edit/',MapaUpdateView.as_view(), name='edit_mapa'),
    path('mapa/<int:pk>/delete/',MapaDeleteView.as_view(), name='delete_mapa'),
    path('mapas',MapasView.as_view(), name='lista_mapa'),
    path('mapa/<str:cidade>/',get_mapa, name='get_mapa'),
]

