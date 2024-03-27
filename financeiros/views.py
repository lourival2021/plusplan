from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib import messages
from django.db.models.deletion import ProtectedError
from .models import Financeiro,Contrato
from .forms import FinanceiroForm


@login_required
def ControleFinanceiroList(request): 

    contratos = Contrato.objects.filter(empresa=request.user.empresa).order_by('-id')
    return render(request, 'financeiros/listar_contratos.html', {'contratos': contratos})


@login_required
def FinanceiroList(request,id): 
    
    user = request.user  # Obtenha o usuário logado
    contrato_id=id
    
    form = FinanceiroForm()  
    contratos = Contrato.objects.filter(usuario=user,id=contrato_id)
    financeiros = Financeiro.objects.filter(usuario=request.user, contrato=contrato_id).order_by('-id')
    return render(request, 'financeiros/listar_financeiros.html', {'form': form, 'financeiros': financeiros, 'contratos':contratos})


@login_required
def FinanceiroDelete(request, id):
    
    financeiro = get_object_or_404(Financeiro, pk=id)

    if request.method == 'POST':
        
        try:
            financeiro.delete()
            messages.success(request, 'Financeiro excluído com sucesso.')
            #return redirect('financeiro_list')
            url = reverse('financeiro_list', args=[financeiro.contrato_id])
            return redirect(url)
        except ProtectedError as e:
            messages.error(request, 'Não é possível excluir esse financeiro devido a dependências.')
   
    url_cancelar = reverse('financeiro_list', args=[financeiro.contrato_id])   
    return render(request, 'cadastros/exclusao_cliente.html', {'url_cancelar':url_cancelar,'financeiro': financeiro})


@login_required
def FinanceiroCreate(request,contrato_id):
    
    contrato_id=contrato_id

    #financeiros = Financeiro.objects.filter(usuario=request.user, )
    contratos = get_object_or_404(Contrato, usuario=request.user, id=contrato_id)

    if request.method == "POST":

        form = FinanceiroForm(request.POST)

        if form.is_valid():

            financeiro = form.save(commit=False)
            financeiro.usuario = request.user
            financeiro.contrato = contratos
            financeiro.save()

            #return redirect('financeiro_list')
            url = reverse('financeiro_list', args=[financeiro.contrato_id])
            return redirect(url)

    else:
        form = FinanceiroForm
       
    return render(request, 'cadastros/form_cliente.html', {'form': form, 'contratos': contratos})
   

@login_required
def FinanceiroUpdate(request, id):

    financeiros = Financeiro.objects.filter(usuario=request.user)
  
    financeiro = get_object_or_404(Financeiro, pk=id)
   
    form = FinanceiroForm(instance=financeiro)
  
    if request.method == "POST":
     
        form = FinanceiroForm(request.POST, instance=financeiro)
       
        if form.is_valid():
            
            financeiro = form.save(commit=False)
            financeiro.usuario = request.user
            financeiro.save()

            #return redirect('financeiro_list')
            url = reverse('financeiro_list', args=[financeiro.contrato_id])
            return redirect(url)
        
    else:
        return render(request, 'cadastros/form_cliente.html', {'form': form, 'financeiros': financeiros})
   