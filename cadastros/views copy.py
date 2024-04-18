from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib import messages
from django.db.models.deletion import ProtectedError
from .models import Cliente,Equipamento,Contrato,Atendimento,Atividade,Tipo,Empresa,Responsavel_Tecnico
from .forms import RespTecnicoForm,ClienteForm,EquipamentoForm,ContratoForm,AtendimentoForm,AtividadeForm,TipoForm,EmpresaForm
import pandas as pd
from django.contrib.auth.models import User  
from django.db import IntegrityError
from django.contrib.auth.models import Group
from datetime import datetime
import calendar
from django.http import HttpResponse
from django.db.models import Count


@login_required
def ImprimirPmoc(request, id):
    user = request.user  # Obtenha o usuário logado
    atendimento_id=id
    atendimentos = Atendimento.objects.filter(empresa=user.empresa_id,id=atendimento_id)
    equipamentos = Equipamento.objects.filter(empresa=user.empresa_id, atendimento=atendimento_id).order_by('-id')
   
    # Lista para armazenar todas as atividades associadas aos equipamentos
    atividades = []

    # Iterar sobre os equipamentos para obter as atividades associadas a cada um
    for equipamento in equipamentos:
        atividades_equipamento = Atividade.objects.filter(empresa=user.empresa, equipamento=equipamento).order_by('-id')
        atividades.extend(atividades_equipamento)

    return render(request, 'cadastros/pmoc.html', {'atendimentos': atendimentos,'equipamentos': equipamentos,'atividades':atividades})


@login_required
def ImprimirCronograma(request, id):
    user = request.user  # Obtenha o usuário logado
    contrato_id = id
    
    atendimentos = Atendimento.objects.filter(empresa=user.empresa, contrato=contrato_id).order_by('-id')
    
    # Buscar todas as atividades relacionadas aos equipamentos que estão associados aos atendimentos
    atividades = Atividade.objects.filter(equipamento__atendimento__in=atendimentos)
    
    return render(request, 'cadastros/pmoc_cronogramas.html', {'atendimentos': atendimentos, 'atividades': atividades})


@login_required
def ImprimirEquipamento(request, id):
    user = request.user  # Obtenha o usuário logado
    atendimento_id = id
    
    equipamentos = Equipamento.objects.filter(empresa=user.empresa, atendimento=atendimento_id).order_by('-id')
    
    return render(request, 'cadastros/pmoc_equipamentos.html', {'equipamentos': equipamentos})

######################################################################

@login_required
def RespTecnicoList(request): 

    user = request.user.empresa_id  # Obtenha o usuário logado
    form = RespTecnicoForm() 
    
    resp_tecnicos = Responsavel_Tecnico.objects.filter(empresa=user).order_by('-id')
    return render(request, 'cadastros/listar_resp_tecnicos.html', {'form': form, 'resp_tecnicos': resp_tecnicos})


@login_required
def RespTecnicoCreate(request):

    resp_tecnicos = Responsavel_Tecnico.objects.filter(usuario=request.user)

    if request.method == "POST":

        form = RespTecnicoForm(request.POST)

        if form.is_valid():

            resp_tecnico = form.save(commit=False)
            resp_tecnico.usuario = request.user
            resp_tecnico.empresa = request.user.empresa
            resp_tecnico.save()

            return redirect('resp_tecnico_list')

    else:
        form = ClienteForm(initial={'tipo_documento': 'pj'})
       
    return render(request, 'cadastros/form_cliente.html', {'form': form, 'resp_tecnicos': resp_tecnicos})
   

@login_required
def RespTecnicoUpdate(request, id):
    resp_tecnicos = Responsavel_Tecnico.objects.filter(usuario=request.user)
    # Certifique-se de filtrar a empresa pelo ID e pelo usuário atual
    resp_tecnico = get_object_or_404(Responsavel_Tecnico, pk=id)
    
    if request.method == "POST":
        form = RespTecnicoForm(request.POST, instance=resp_tecnico)
        if form.is_valid():
            form.save()  # Não é necessário commit=False se não houver outras operações a serem feitas
            return redirect('resp_tecnico_list')
    else:
        # Se o método da requisição não for POST, crie o formulário com a instância da empresa
        form = RespTecnicoForm(instance=resp_tecnico)
    
    return render(request, 'cadastros/form_cliente.html', {'form': form, 'resp_tecnicos': resp_tecnicos})

###########################################################################

login_required
def EmpresaList(request): 

    user = request.user.empresa_id  # Obtenha o usuário logado
    form = EmpresaForm() 
    
    empresas = Empresa.objects.filter(id=user).order_by('-id')
    return render(request, 'cadastros/listar_empresas.html', {'form': form, 'empresas': empresas})


@login_required
def EmpresaUpdate(request, id):
    empresas = Empresa.objects.filter(usuario=request.user)
    # Certifique-se de filtrar a empresa pelo ID e pelo usuário atual
    empresa = get_object_or_404(Empresa, pk=id)
    
    if request.method == "POST":
        form = EmpresaForm(request.POST, instance=empresa)
        if form.is_valid():
            form.save()  # Não é necessário commit=False se não houver outras operações a serem feitas
            return redirect('dashboard')
    else:
        # Se o método da requisição não for POST, crie o formulário com a instância da empresa
        form = EmpresaForm(instance=empresa)
    
    return render(request, 'cadastros/form_cliente.html', {'form': form, 'empresas': empresas})


############################################################################

@login_required
def ClienteList(request):
    # Obtenha a empresa do usuário autenticado
    empresa_do_usuario = request.user.empresa_id

    # Filtrar os clientes com base na empresa do usuário autenticado
    clientes = Cliente.objects.filter(empresa=empresa_do_usuario).order_by('-id')

    form = ClienteForm()
    
    return render(request, 'cadastros/listar_clientes.html', {'form': form, 'clientes': clientes})


@login_required
def ClienteDelete(request, id):
    
    cliente = get_object_or_404(Cliente, pk=id)

    if request.method == 'POST':
        
        try:
            cliente.delete()
            messages.success(request, 'Cliente excluído com sucesso.')
            return redirect('cliente_list')
        except ProtectedError as e:
            messages.error(request, 'Não é possível excluir esse cliente devido a dependências.')
     
    url_cancelar = reverse('cliente_list')  
    return render(request, 'cadastros/exclusao_cliente.html', {'url_cancelar':url_cancelar,'cliente': cliente})


@login_required
def ClienteCreate(request):

    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.usuario = request.user
            cliente.empresa = request.user.empresa  # Usar a empresa do usuário autenticado
            cliente.save()
            return redirect('cliente_list')
    else:
        form = ClienteForm(initial={'tipo_documento': 'pj'})
       
    return render(request, 'cadastros/form_cliente.html', {'form': form})


@login_required
def ClienteUpdate(request, id):
    clientes = Cliente.objects.filter(usuario=request.user)
    cliente = get_object_or_404(Cliente, pk=id)
    
    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.usuario = request.user
            cliente.save()
            return redirect('cliente_list')
    else:
        form = ClienteForm(instance=cliente)  # Moveu esta linha para dentro do bloco 'else'
    
    return render(request, 'cadastros/form_cliente.html', {'form': form, 'clientes': clientes})


###########################################################
    
@login_required
def EquipamentoList(request,id): 
    
    empresa_do_usuario = request.user.empresa_id
    
    #user = request.user  # Obtenha o usuário logado
    atendimento_id = id
    
    form = EquipamentoForm() 
    atendimentos = Atendimento.objects.filter(empresa=empresa_do_usuario,id=atendimento_id)
    equipamentos = Equipamento.objects.filter(empresa=empresa_do_usuario, atendimento=atendimento_id).order_by('-id')
    return render(request, 'cadastros/listar_equipamentos.html', {'form': form, 'equipamentos': equipamentos, 'atendimentos':atendimentos})


@login_required
def EquipamentoDelete(request, id):
    
    equipamento = get_object_or_404(Equipamento, pk=id)

    if request.method == 'POST':
        
        try:
            equipamento.delete()
            messages.success(request, 'Equipamento excluído com sucesso.')
            
            url = reverse('equipamento_list', args=[equipamento.atendimento_id])
            return redirect(url)

        except ProtectedError as e:
            messages.error(request, 'Não é possível excluir esse equipamento devido a dependências.')
    url_cancelar = reverse('equipamento_list', args=[equipamento.atendimento_id]) 
    return render(request, 'cadastros/exclusao_cliente.html', {'url_cancelar':url_cancelar,'equipamento': equipamento})

@login_required
def EquipamentoCreate(request, id):
    atendimento_id = id
    atendimentos = get_object_or_404(Atendimento, usuario=request.user, id=atendimento_id)
    
    if request.method == "POST":
        form = EquipamentoForm(request.POST)
        if form.is_valid():
            equipamento = form.save(commit=False)
            equipamento.usuario = request.user
            equipamento.atendimento = atendimentos
            equipamento.empresa = request.user.empresa
            equipamento.save()
            
            # Atualizar a quantidade de equipamentos ativos no contrato
            contrato = Contrato.objects.get(atendimento=atendimentos)
            contrato.qtd_equipamento_ativo = Equipamento.objects.filter(atendimento=atendimentos, ativo=True).count()
            contrato.save()

            # Redirecionar para a página de listagem de equipamentos do atendimento
            url = reverse('equipamento_list', args=[equipamento.atendimento_id])
            return redirect(url)
    else:
        form = EquipamentoForm()

    return render(request, 'cadastros/form_cliente.html', {'form':form, 'atendimentos':atendimentos})


@login_required
def EquipamentoUpdate(request, id):
    equipamento = get_object_or_404(Equipamento, pk=id, usuario=request.user)
    equipamentos = Equipamento.objects.filter(usuario=request.user)

    if request.method == "POST":
        form = EquipamentoForm(request.POST, instance=equipamento)

        if form.is_valid():
            equipamento = form.save(commit=False)
            equipamento.usuario = request.user
            equipamento.save()

            # Redirecionar para a lista de equipamentos do contrato atualizado
            url = reverse('equipamento_list', args=[equipamento.atendimento_id])
            return redirect(url)
    else:
        form = EquipamentoForm(instance=equipamento)
    
    contexto = {'form': form, 'equipamentos': equipamentos}
    return render(request, 'cadastros/form_cliente.html', contexto)


#####################################################################

@login_required
def TipoList(request): 

    user = request.user  # Obtenha o usuário logado
    
    form = TipoForm() 
    tipos = Tipo.objects.filter(usuario=user)
    return render(request, 'cadastros/listar_tipos.html', {'form': form, 'tipos': tipos})


@login_required
def TipoCreate(request):
    tipos = Tipo.objects.filter(usuario=request.user)

    if request.method == "POST":
        form = TipoForm(request.POST)

        if form.is_valid():
            tipo = form.save(commit=False)
            tipo.usuario = request.user
            tipo.save()
        
            return redirect('tipo_list')
    else:
        form = TipoForm()

    contexto = {'form': form, 'tipos': tipos}
    return render(request, 'cadastros/form_cliente.html', contexto)


@login_required
def TipoUpdate(request, id):

    tipos = Tipo.objects.filter(usuario=request.user)
  
    tipo = get_object_or_404(Tipo, pk=id)
   
    form = TipoForm(instance=tipo)
  
    if request.method == "POST":
     
        form = TipoForm(request.POST, instance=tipo)
       
        if form.is_valid():
            
            tipo = form.save(commit=False)
            tipo.usuario = request.user
            tipo.save()

            return redirect('tipo_list')
        
    else:
        return render(request, 'cadastros/form_cliente.html', {'form': form, 'tipos': tipos})
   

@login_required
def TipoDelete(request, id):
    
    tipo = get_object_or_404(Tipo, pk=id)

    if request.method == 'POST':
        
        try:
            tipo.delete()
            messages.success(request, 'Tipo excluído com sucesso.')
            return redirect('tipo_list')
        except ProtectedError as e:
            messages.error(request, 'Não é possível excluir esse tipo devido a dependências.')
     
    return render(request, 'cadastros/exclusao_cliente.html', {'tipo': tipo})


######################################################################

@login_required
def AtividadeList(request,id): 

    equipamento_id = id
    empresa_do_usuario = request.user.empresa_id
    
    form = AtividadeForm() 
    equipamentos = Equipamento.objects.filter(empresa=empresa_do_usuario,id=equipamento_id)
    periodicidades = Atividade.objects.filter(empresa=empresa_do_usuario, equipamento=equipamento_id)
    return render(request, 'cadastros/listar_periodicidades.html', {'form': form, 'periodicidades': periodicidades, 'equipamentos':equipamentos})


@login_required
def AtividadeCreate(request, id):
    equipamento_id = id

    equipamentos = get_object_or_404(Equipamento, usuario=request.user, id=equipamento_id)

    if request.method == 'POST':
        form = AtividadeForm(request.POST)
        if form.is_valid():
            atividade = form.save(commit=False)
            atividade.usuario = request.user
            atividade.empresa = request.user.empresa
            atividade.equipamento = equipamentos

            mes_escolhido = form.cleaned_data['competencia']
            #periodicidade = form.cleaned_data['periodicidade']
            ano_atual = datetime.now().year
            ultimo_dia_mes = calendar.monthrange(ano_atual, mes_escolhido)[1]
            inicio_manutencao = datetime(ano_atual, mes_escolhido, 1)
            termino_manutencao = datetime(ano_atual, mes_escolhido, ultimo_dia_mes)

            atividade.competencia = mes_escolhido
            atividade.inicio_manutencao = inicio_manutencao
            atividade.termino_manutencao = termino_manutencao

            atividade.save()

            url = reverse('periodicidade_list', args=[atividade.equipamento_id])
            return redirect(url)
    else:
        form = AtividadeForm()

    contexto = {'form': form, 'equipamentos': equipamentos}
    return render(request, 'cadastros/form_atividades.html', contexto)


@login_required
def AtividadeUpdate(request, id):
    periodicidade = get_object_or_404(Atividade, pk=id, usuario=request.user)
    periodicidades = Atividade.objects.filter(usuario=request.user, pk=id)

    if request.method == "POST":
        form = AtividadeForm(request.POST, instance=periodicidade)

        if form.is_valid():
            periodicidade = form.save(commit=False)
            periodicidade.usuario = request.user
            periodicidade.save()

           # return redirect('contrato_list')
            url = reverse('periodicidade_list', args=[periodicidade.equipamento_id])
            return redirect(url)
    else:
        form = AtividadeForm(instance=periodicidade)
    
    contexto = {'form': form, 'periodicidades': periodicidades}
    return render(request, 'cadastros/form_cliente.html', contexto)


@login_required
def AtividadeDelete(request, id):
    
    periodicidade = get_object_or_404(Atividade, pk=id)

    if request.method == 'POST':
        
        try:
            periodicidade.delete()
            messages.success(request, 'Periodicidade excluído com sucesso.')
            #return redirect('periodicidade_list')
            url = reverse('periodicidade_list', args=[periodicidade.equipamento_id])
            return redirect(url)
        except ProtectedError as e:
            messages.error(request, 'Não é possível excluir esse periodo devido a dependências.')
    
    url_cancelar = reverse('periodicidade_list', args=[periodicidade.equipamento_id])  
    return render(request, 'cadastros/exclusao_cliente.html', {'url_cancelar':url_cancelar,'periodicidade': periodicidade})


####################################################################

@login_required
def ContratoList(request): 

    # Obtenha a empresa do usuário autenticado
    empresa_do_usuario = request.user.empresa_id

    # Filtrar os clientes com base na empresa do usuário autenticado
    contratos = Contrato.objects.filter(empresa=empresa_do_usuario).order_by('-id')

    return render(request, 'cadastros/listar_contratos.html', 
                  {'contratos': contratos})


@login_required
def ContratoDelete(request, id):
    
    contrato = get_object_or_404(Contrato, pk=id)

    if request.method == 'POST':
        
        try:
            contrato.delete()
            messages.success(request, 'Contrato excluído com sucesso.')
            return redirect('contrato_list')
        except ProtectedError as e:
            messages.error(request, 'Não é possível excluir esse contrato devido a dependências.')
    
    url_cancelar = reverse('contrato_list')  
    return render(request, 'cadastros/exclusao_cliente.html', {'url_cancelar':url_cancelar,'contrato': contrato})


@login_required
def ContratoCreate(request):

    contratos = Contrato.objects.filter(usuario=request.user)

    if request.method == "POST":

        form = ContratoForm(request.POST)

        if form.is_valid():

            contrato = form.save(commit=False)
            contrato.usuario = request.user
            contrato.empresa = request.user.empresa
            contrato.save()

            return redirect('contrato_list')

    else:
        form = ContratoForm
       
    return render(request, 'cadastros/form_cliente.html', {'form': form, 'contratos': contratos})
   

@login_required
def ContratoUpdate(request, id):

    contratos = Contrato.objects.filter(usuario=request.user)
  
    contrato = get_object_or_404(Contrato, pk=id)
   
    form = ContratoForm(instance=contrato)
  
    if request.method == "POST":
     
        form = ContratoForm(request.POST, instance=contrato)
       
        if form.is_valid():
            
            contrato = form.save(commit=False)
            contrato.usuario = request.user
            contrato.save()

            return redirect('contrato_list')
        
    else:   
        return render(request, 'cadastros/form_cliente.html', {'form': form, 'contratos': contratos})


#############################################################

@login_required
def AtendimentoList(request, contrato_id): 
    user = request.user  # Obtenha o usuário logado
    contrato = get_object_or_404(Contrato, pk=contrato_id)  # Obtenha o contrato pelo ID ou retorne um erro 404 se não existir
    empresa_do_usuario = user.empresa_id
    
    # Verifique se o usuário é da mesma empresa do contrato ou é um superusuário
    if user.is_superuser or empresa_do_usuario == contrato.empresa_id:
        form = AtendimentoForm()  
        contratos = Contrato.objects.filter(empresa=contrato.empresa_id, id=contrato_id)
        atendimentos = Atendimento.objects.filter(contrato=contrato_id).order_by('nome')
        return render(request, 'cadastros/listar_atendimentos.html', {'form': form, 'atendimentos': atendimentos, 'contratos': contratos})
    else:
        # Caso o usuário não tenha permissão para acessar os atendimentos deste contrato, você pode redirecioná-lo para uma página de erro ou retornar uma resposta de erro.
        return HttpResponse("Você não tem permissão para acessar este contrato.")


@login_required
def AtendimentoCreate(request,contrato_id):
    # Recebe o ID do contrato da URL
    contrato_id = contrato_id
    
    # Obtém o contrato específico do usuário atual
    contratos = get_object_or_404(Contrato, usuario=request.user, id=contrato_id)

    if request.method == "POST":
        # Se o formulário foi submetido
        form = AtendimentoForm(request.POST) 
        if form.is_valid():
            # Se o formulário é válido, salva o novo atendimento
            atendimento = form.save(commit=False)
            atendimento.usuario = request.user
            atendimento.contrato = contratos
     
            atendimento.save()
            # Redireciona para a página de lista de contratos após a criação do atendimento
            url = reverse('atendimento_list', args=[atendimento.contrato_id])
            return redirect(url)
    else:
        # Se for uma requisição GET, cria um novo formulário em branco
        form = AtendimentoForm()
       
    # Renderiza o template com o formulário e a lista de atendimentos
    return render(request, 'cadastros/form_cliente.html', {'form': form, 'contratos': contratos})


@login_required
def AtendimentoDelete(request, id):
    
    atendimento = get_object_or_404(Atendimento, pk=id)

    if request.method == 'POST':
        
        try:
            atendimento.delete()
            messages.success(request, 'Unidade de atendimento excluída com sucesso.')
           
            url = reverse('atendimento_list', args=[atendimento.contrato_id])
            return redirect(url)
        except ProtectedError as e:
            messages.error(request, 'Não é possível excluir essa unidade devido a dependências.')
     
    url_cancelar = reverse('atendimento_list', args=[atendimento.contrato_id])  
    return render(request, 'cadastros/exclusao_cliente.html', {'url_cancelar':url_cancelar,'atendimento': atendimento})


@login_required
def AtendimentoUpdate(request, id):

    atendimentos = Atendimento.objects.filter(usuario=request.user)
  
    atendimento = get_object_or_404(Atendimento, pk=id)
   
    form = AtendimentoForm(instance=atendimento)
  
    if request.method == "POST":
     
        form = AtendimentoForm(request.POST, instance=atendimento)
       
        if form.is_valid():
            
            atendimento = form.save(commit=False)
            atendimento.usuario = request.user
            atendimento.save()

            url = reverse('atendimento_list', args=[atendimento.contrato_id])
            return redirect(url)
        
    else:
        return render(request, 'cadastros/form_cliente.html', {'form': form, 'atendimentos': atendimentos})
   
########################################################################
    
@login_required
def importar_equipamentos(request):
    if request.method == 'POST' and request.FILES['arquivo_excel']:
        arquivo_excel = request.FILES['arquivo_excel']
        # Leia o arquivo Excel
        df_equipamentos = pd.read_excel(arquivo_excel)

        # Iterar sobre cada linha do DataFrame
        for index, row in df_equipamentos.iterrows():
            codigo = row['CODIGO']  # Supondo que 'codigo' é o nome da coluna com códigos de equipamento
            atendimento = row['ATENDIMENTO'] 
            tipo = row['TIPO']  # Supondo que 'tipo' é o nome da coluna com tipos de equipamento
            marca = row['MARCA']  # Supondo que 'marca' é o nome da coluna com marcas de equipamento
            tag = row['TAG'] 
            mod_evaporador = row['EVAPORADOR'] 
            mod_condensador = row['CONDENSADOR'] 
            ambiente = row['AMBIENTE'] 
            capacidade = row['CAPACIDADE'] 
            gas_refrigerante = row['GASREFRIGERANTE'] 
            usuario_id = row['USUARIO']

            # Obtenha o usuário com o ID fornecido
            usuario = User.objects.get(id=usuario_id)

            # Obtenha todos os atendimentos com o código fornecido
            atendimentos = Atendimento.objects.filter(codigo=codigo)

            # Crie um novo registro de equipamento para cada atendimento correspondente
            for atendimento in atendimentos:
                Equipamento.objects.create(
                    codigo=codigo,
                    atendimento=atendimento,
                    marca=marca,
                    tipo=tipo,
                    tag=tag,
                    mod_evaporador=mod_evaporador,
                    mod_condensador=mod_condensador,
                    ambiente=ambiente,
                    capacidade=capacidade,
                    gas_refrigerante=gas_refrigerante,
                    
                    usuario=usuario,
                    # Outros campos do modelo Equipamento, se houver
                )

        return render(request, 'cadastros/importar.html')

    return render(request, 'cadastros/importar.html')

@login_required
def importar_atividades(request):
    if request.method == 'POST' and request.FILES['arquivo_excel']:
        arquivo_excel = request.FILES['arquivo_excel']
        # Leia o arquivo Excel
        df_atividades = pd.read_excel(arquivo_excel)

        # Iterar sobre cada linha do DataFrame
        for index, row in df_atividades.iterrows():
            codigo_atendimento = row['CODIGO']  # Supondo que 'codigo_atendimento' é o nome da coluna com códigos de atendimento
            periodicidade = row['PERIODICIDADE']  # Supondo que 'periodicidade' é o nome da coluna com periodicidade de atividades
            competencia = row['COMPETENCIA']  # Supondo que 'competencia' é o nome da coluna com competência de atividades
            usuario_id = row['USUARIO']

            # Obtenha o usuário com o ID fornecido
            usuario = User.objects.get(id=usuario_id)

            # Obtenha o atendimento com o código fornecido
            atendimento = Atendimento.objects.get(codigo=codigo_atendimento)

            # Obtenha todos os equipamentos associados a esse atendimento
            equipamentos = Equipamento.objects.filter(atendimento=atendimento)

            # Crie um novo registro de atividade para cada equipamento correspondente
            for equipamento in equipamentos:
                Atividade.objects.create(
                    equipamento=equipamento,
                    periodicidade=periodicidade,
                    competencia=competencia,
                    usuario=usuario,
                    # Outros campos do modelo Atividade, se houver
                )

        return render(request, 'cadastros/importar.html')

    return render(request, 'cadastros/importar.html')

@login_required
def importar_atendimentos(request):
    if request.method == 'POST' and request.FILES['arquivo_excel']:
        arquivo_excel = request.FILES['arquivo_excel']
        df = pd.read_excel(arquivo_excel)

        for index, row in df.iterrows():
            contrato_id = row['CONTRATO']  # Assumindo que 'contrato_id' é uma coluna no seu arquivo Excel
            usuario_id = row['USUARIO']  # Assumindo que 'usuario_id' é uma coluna no seu arquivo Excel

            # Obtendo os objetos Contrato e Usuario correspondentes aos ids
            contrato = Contrato.objects.get(id=contrato_id)
            usuario = User.objects.get(id=usuario_id)  # Correção aqui: obtenha o usuário por id

            # Criando o objeto Atendimento com as relações com Contrato e Usuario
            atendimento = Atendimento(
                codigo=row['CODIGO'],
                nome=row['NOME'],
                cnpj=row['CNPJ'],
                endereco=row['ENDERECO'],
                bairro=row['BAIRRO'],
                cidade=row['CIDADE'],
                uf=row['UF'],
                cep=row['CEP'],
                contrato=contrato,
                usuario=usuario
            )
            atendimento.save()

        return render(request, 'cadastros/importar.html')

    return render(request, 'cadastros/importar.html')
