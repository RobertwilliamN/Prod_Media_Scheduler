from django.urls import path, include
from . import views

urlpatterns = [
    path('list/', views.PublicacaoListView.as_view(), name='list-publicacoes'),
    path('create/', views.PublicacaoCreateView.as_view(), name='create-publicacao'),
    path('<int:pk>/edit/', views.PublicacaoUpdateView.as_view(), name='edit-publicacao'),
    path('<int:pk>/delete/', views.PublicacaoDeleteView.as_view(), name='delete-publicacao'),
]
