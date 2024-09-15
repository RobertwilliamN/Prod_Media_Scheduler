from django.urls import path
from .views import get_instagram_info

urlpatterns = [
    path('get-instagram-info/<str:perfil_nome>/', get_instagram_info, name='get_instagram_info'),
]

