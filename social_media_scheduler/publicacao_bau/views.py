from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Publicacao_Bau
from .forms import PublicacaoBauForm

# Listagem de publicações no banco
class PublicacaoListView(ListView):
    model = Publicacao_Bau
    template_name = 'list.html'
    context_object_name = 'publicacoes'

# Criação de uma nova publicação no banco
class PublicacaoCreateView(CreateView):
    model = Publicacao_Bau
    form_class = PublicacaoBauForm
    template_name = 'publicacao_bau_form.html'
    success_url = reverse_lazy('list-publicacoes_banco')

# Edição de uma publicação no banco
class PublicacaoUpdateView(UpdateView):
    model = Publicacao_Bau
    form_class = PublicacaoBauForm
    template_name = 'publicacao_bau_form.html'
    success_url = reverse_lazy('list-publicacoes_banco')

# Deletar uma publicação do banco
class PublicacaoDeleteView(DeleteView):
    model = Publicacao_Bau
    template_name = 'publicacao_bau_confirm_delete.html'
    success_url = reverse_lazy('list-publicacoes_banco')

