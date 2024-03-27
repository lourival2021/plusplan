from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib import messages
from django.db.models.deletion import ProtectedError
from .models import Contrato,Equipamento,Atividade,Atendimento
from .forms import AtividadeForm,AtividadeProblemaForm
from itertools import groupby
from operator import attrgetter
from django.utils.html import strip_tags
from django.core.paginator import Paginator
from django.db.models import Q


def ControlePmocList(request):
        
    contratos = Contrato.objects.filter(empresa=request.user.empresa_id).order_by('-id')
    return render(request, 'planejamentos/listar_contratos.html', 
                  {'contratos': contratos})


def PmocList(request, id):
    contrato_id = id

    search_value = request.GET.get('search_value')
    atendimento_id = request.GET.get('atendimento')
    atividade = request.GET.get('competencia')

    atendimentos = Atendimento.objects.filter(empresa=request.user.empresa_id, contrato=contrato_id)
    equipamentos = Equipamento.objects.filter(empresa=request.user.empresa_id, atendimento__contrato_id=contrato_id)

    if search_value:
        equipamentos = equipamentos.filter(
            Q(codigo__icontains=search_value) |
            Q(ambiente__icontains=search_value) |
            Q(tipo__icontains=search_value) |
            Q(tag__icontains=search_value) |
            Q(marca__icontains=search_value)
        )

    if atendimento_id:
        equipamentos = equipamentos.filter(atendimento_id=atendimento_id)

    # Obtendo todas as atividades correspondentes aos equipamentos
    atividades = []
    for equipamento in equipamentos:
        if atividade:  # Verifica se a atividade foi selecionada
            if atividade != '':  # Verifica se a atividade é diferente de vazio
                if atividade == '0':  # Se atividade for '0', mostrar todas as atividades
                    atividades.extend(equipamento.atividade_set.all())
                else:
                    atividades.extend(equipamento.atividade_set.filter(competencia=atividade))

    # Paginando as atividades
    atividades_por_pagina = 10
    paginator = Paginator(atividades, atividades_por_pagina)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'planejamentos/listar_pmocs.html', {'page_obj': page_obj, 'atendimentos': atendimentos})


@login_required
def AtividadeUpdate(request, id):
    atividade = get_object_or_404(Atividade, pk=id, usuario=request.user)
    atividades = Atividade.objects.filter(usuario=request.user, pk=id)

    if request.method == "POST":
        form = AtividadeForm(request.POST, instance=atividade)

        if form.is_valid():
            atividade = form.save(commit=False)

            # Se o campo 'problema' for preenchido, remova as tags HTML antes de salvar
            problema_texto = form.cleaned_data['problema']
            if problema_texto:
                problema_texto_sem_tags = strip_tags(problema_texto)
                atividade.problema = problema_texto_sem_tags

            atividade.usuario = request.user
            atividade.save()

            # Redirecionar para a página desejada após o salvamento bem-sucedido
            url = reverse('controle_list')
            return redirect(url)
    else:
        form = AtividadeForm(instance=atividade)
    
    contexto = {'form': form, 'atividades': atividades}
    return render(request, 'cadastros/form_cliente.html', contexto)


@login_required
def AtividadeProblemaUpdate(request, id):
    atividade = get_object_or_404(Atividade, pk=id, usuario=request.user)
    atividades = Atividade.objects.filter(usuario=request.user, pk=id)

    if request.method == "POST":
        form = AtividadeProblemaForm(request.POST, instance=atividade)
        if form.is_valid():
           
            url = reverse('controle_list')
            return redirect(url)
    else:
        form = AtividadeProblemaForm(instance=atividade)

    contexto = {'form': form, 'atividades': atividades}
    return render(request, 'cadastros/form_cliente.html', contexto)

