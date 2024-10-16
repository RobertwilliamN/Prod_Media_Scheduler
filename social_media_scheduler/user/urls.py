# user/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
 
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('cadastro/', views.CadastroView, name='cadastro'),
    path('sucesso/', views.sucesso_cadastro, name='sucesso-cadastro'),
    path('password_change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('delete/', views.delete_user, name='delete_user'),  # URL para exclusão de usuário
    
]
