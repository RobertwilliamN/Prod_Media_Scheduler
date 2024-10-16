from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Publicacao
from django.urls import reverse_lazy
from .forms import PublicacaoForm,PublicacaoFilterForm

@method_decorator(login_required, name='dispatch')
class PublicacaoListView(ListView):
    model = Publicacao
    template_name = 'lista.html'
    context_object_name = 'publicacoes'
    paginate_by = 100  # Define quantas publicações por página

    def get_queryset(self):
        queryset = super().get_queryset()
        form = PublicacaoFilterForm(self.request.GET or None)

        if form.is_valid():
            perfil = form.cleaned_data.get('perfil')
            rede_social = form.cleaned_data.get('rede_social')
            status = form.cleaned_data.get('status')
            pais = form.cleaned_data.get('pais')
            data_inicio = form.cleaned_data.get('data_inicio')
            data_fim = form.cleaned_data.get('data_fim')

            if perfil:
                queryset = queryset.filter(perfil=perfil)
            if rede_social:
                queryset = queryset.filter(rede_social__in=[rede_social])
            if status:
                queryset = queryset.filter(status=status)
            if pais:
                queryset = queryset.filter(perfil__pais=pais).distinct() 
            if data_inicio:
                queryset = queryset.filter(data_agendada__gte=data_inicio)
            if data_fim:
                queryset = queryset.filter(data_agendada__lte=data_fim)

        for publicacao in queryset:
            publicacao.paises_unicos = publicacao.perfil.values_list('pais', flat=True).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PublicacaoFilterForm(self.request.GET or None)
        return context

@method_decorator(login_required, name='dispatch')
class PublicacaoCreateView(CreateView):
    model = Publicacao
    form_class = PublicacaoForm
    template_name = 'publicacao_form.html'
    success_url = reverse_lazy('list-publicacoes')

@method_decorator(login_required, name='dispatch')
class PublicacaoUpdateView(UpdateView):
    model = Publicacao
    form_class = PublicacaoForm
    template_name = 'publicacao_form.html'
    success_url = reverse_lazy('list-publicacoes')

@method_decorator(login_required, name='dispatch')
class PublicacaoDeleteView(DeleteView):
    model = Publicacao
    template_name = 'publicacao_confirm_delete.html'
    success_url = reverse_lazy('list-publicacoes')

