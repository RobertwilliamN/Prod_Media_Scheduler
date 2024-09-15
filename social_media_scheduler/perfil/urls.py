from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.listar_perfis, name='listar-perfis'),
    path('create/', views.criar_perfil, name='criar-perfil'),
    path('<int:pk>/edit/', views.editar_perfil, name='editar-perfil'),  
    path('<int:pk>/delete/', views.apagar_perfil, name='apagar-perfil'),  
]
