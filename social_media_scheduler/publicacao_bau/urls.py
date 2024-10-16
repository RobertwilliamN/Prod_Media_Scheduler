from django.urls import path, include
from . import views

urlpatterns = [
    path('publicacao/list/', views.PublicacaoListView.as_view(), name='list-publicacoes_banco'),
    path('create/', views.PublicacaoCreateView.as_view(), name='create-publicacao_banco'),
    path('<int:pk>/edit/', views.PublicacaoUpdateView.as_view(), name='edit-publicacao_banco'),
    path('<int:pk>/delete/', views.PublicacaoDeleteView.as_view(), name='delete-publicacao_banco'),
]

