from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Perfil
from publicacao_bau.models import Publicacao_Bau
from publicacao.models import RegistroPostagem
from .forms import PerfilForm
from django.db.models import Count
from django.utils.decorators import method_decorator


@login_required
def listar_perfis(request):
    # Obtém o total de publicações no Publicacao_Bau
    total_publicacoes_no_bau = Publicacao_Bau.objects.count()

    # Anota o número de postagens feitas para cada perfil
    perfis = Perfil.objects.annotate(
        postagens_feitas=Count('registropostagem', distinct=True)  # Contando quantas postagens foram feitas por perfil
    ).all()

    # Adiciona o total de publicacoes no Bau para todos os perfis
    for perfil in perfis:
        perfil.publicacoes_no_bau = total_publicacoes_no_bau  # A mesma contagem para todos os perfis

    return render(request, 'listar_perfis.html', {'perfis': perfis})

@login_required
def criar_perfil(request):
    if request.method == 'POST':
        form = PerfilForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/perfil/list')
    else:
        form = PerfilForm()
    return render(request, 'criar_perfil.html', {'form': form})

@login_required
def editar_perfil(request, pk):
    perfil = get_object_or_404(Perfil, pk=pk)
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('listar-perfis')
    else:
        form = PerfilForm(instance=perfil)
    return render(request, 'editar_perfil.html', {'form': form, 'perfil': perfil})

@login_required
def apagar_perfil(request, pk):
    perfil = get_object_or_404(Perfil, pk=pk)
    if request.method == 'POST':
        perfil.delete()
        return redirect('listar-perfis')
    return render(request, 'apagar_perfil.html', {'perfil': perfil})
