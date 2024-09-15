from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from .form import CustomAuthenticationForm, CustomCadastroForm
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordChangeForm

# Login de usuário
@login_required
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/publicacao/list')  # Redirecionar 
            else:
                messages.error(request, "Usuário ou senha inválidos.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


# Cadastro de usuário
@login_required
def CadastroView(request):
    if not request.user.is_authenticated:
        return redirect('/user/login')  # Redirecionar para a página de login se não estiver autenticado

    if request.method == 'POST':
        form = CustomCadastroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('/user/sucesso')  
    else:
        form = CustomCadastroForm()
    
    return render(request, 'cadastro.html', {'form': form})


def sucesso_cadastro(request):
    return render(request, 'sucesso_cadastro.html')


# Alterando senha
class CustomPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'password_change.html'
    success_url = reverse_lazy('password_change_done')  # Redireciona após a alteração com sucesso
# Senha alterada com sucesso!
class PasswordChangeDoneView(PasswordChangeView):
    template_name = 'password_change_done.html'


# Deletar usuário
@login_required
def delete_user(request):
    if request.method == 'POST':
        user = get_object_or_404(get_user_model(), pk=request.user.pk)
        user.delete()
      
        return redirect('/user/login')  # Redireciona para a página inicial ou outra página após a exclusão
    return render(request, 'confirm_delete.html')