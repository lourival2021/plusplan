from django.db import models
from django.contrib.auth.models import User
import uuid
from django.conf import settings


class Responsavel_Tecnico(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    TIPO_DOCUMENTO_CHOICES = [
        ('pf', 'Pessoal Física'),
        ('pj', 'Pessoa Jurídica'),
    ]

    tipo_documento = models.CharField(max_length=4, choices=TIPO_DOCUMENTO_CHOICES)
    cnpj = models.CharField(max_length=18, unique=True, null=True, blank=True)
    cpf = models.CharField(max_length=14, unique=True, null=True, blank=True)

    nome = models.CharField(verbose_name="Nome", max_length=45, null=True)   
    endereco = models.CharField(verbose_name="Endereço", max_length=255, blank=True)
    bairro = models.CharField(verbose_name="Bairro", max_length=45, blank=True)
    cidade = models.CharField(verbose_name="Cidade", max_length=45, blank=True)
    uf = models.CharField(verbose_name="UF", max_length=2, blank=True)
    cep = models.CharField(verbose_name="Cep", max_length=45, blank=True) 
    telefone = models.CharField(verbose_name="Telefone", max_length=45, blank=True) 
    email = models.EmailField(verbose_name="Email", max_length=45, blank=True) 
    
    rigistro_conselho = models.CharField(verbose_name="Registro no Conselho de Classe", max_length=45, blank=True, null=True)
    art = models.CharField(verbose_name="ART", max_length=45, blank=True, null=True)    
    
    empresa = models.OneToOneField('Empresa', on_delete=models.SET_NULL, null=True, blank=True, related_name='Responsavel_Tecnico')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    registro_atualizado = models.DateTimeField(auto_now=True)
    registro_criado = models.DateTimeField(auto_now_add=True)

    def __str__(self): 
        return self.nome

    class Meta:
        db_table = 'resp_tecnico'


class Empresa(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    TIPO_DOCUMENTO_CHOICES = [
        ('pf', 'Pessoal Física'),
        ('pj', 'Pessoa Jurídica'),
    ]

    tipo_documento = models.CharField(max_length=4, choices=TIPO_DOCUMENTO_CHOICES)
    cnpj = models.CharField(max_length=18, unique=True, null=True, blank=True)
    cpf = models.CharField(max_length=14, unique=True, null=True, blank=True)

    nome = models.CharField(verbose_name="Nome", max_length=255, null=True)   
    endereco = models.CharField(verbose_name="Endereço", max_length=255, blank=True)
    bairro = models.CharField(verbose_name="Bairro", max_length=45, blank=True)
    cidade = models.CharField(verbose_name="Cidade", max_length=45, blank=True)
    uf = models.CharField(verbose_name="UF", max_length=2, blank=True)
    cep = models.CharField(verbose_name="Cep", max_length=45, blank=True) 
    telefone = models.CharField(verbose_name="Telefone", max_length=45, blank=True) 
    email = models.EmailField(verbose_name="Email", max_length=45, blank=True) 
    
    resp_tecnico = models.OneToOneField('Responsavel_Tecnico', on_delete=models.SET_NULL, null=True, related_name='empresa_do_responsavel')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='empresa_do_usuario')
    registro_atualizado = models.DateTimeField(auto_now=True)
    registro_criado = models.DateTimeField(auto_now_add=True)

    def __str__(self): 
        return self.nome

    class Meta:
        db_table = 'empresa'


class Cliente(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    TIPO_DOCUMENTO_CHOICES = [
        ('pf', 'Pessoal Física'),
        ('pj', 'Pessoa Jurídica'),
    ]

    tipo_documento = models.CharField(max_length=4, choices=TIPO_DOCUMENTO_CHOICES)
    cnpj = models.CharField(max_length=18, unique=True, null=True, blank=True)
    cpf = models.CharField(max_length=14, unique=True, null=True, blank=True)

    nome = models.CharField(verbose_name="Nome", max_length=45, null=True)   
    endereco = models.CharField(verbose_name="Endereço", max_length=255, blank=True)
    bairro = models.CharField(verbose_name="Bairro", max_length=45, blank=True)
    cidade = models.CharField(verbose_name="Cidade", max_length=45, blank=True)
    uf = models.CharField(verbose_name="UF", max_length=2, blank=True)
    cep = models.CharField(verbose_name="Cep", max_length=45, blank=True) 
    telefone = models.CharField(verbose_name="Telefone", max_length=45, blank=True) 
    email = models.EmailField(verbose_name="Email", max_length=45, blank=True) 
    
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE,blank=True, null=True)
    registro_atualizado = models.DateTimeField(auto_now=True)
    registro_criado = models.DateTimeField(auto_now_add=True)

    def __str__(self): 
        return self.nome

    class Meta:
        db_table = 'cliente'


class Contrato(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pregao = models.CharField(verbose_name="Pregão", max_length=45, null=True)   
    contrato = models.CharField(verbose_name="Contrato", max_length=45, null=True)   
    objeto = models.TextField(verbose_name="Objeto do Contrato", blank=True)

    custo = models.DecimalField(default=0,max_digits=10, decimal_places=2, verbose_name="Valor Contratual (Global)")  
    expectativa_faturamento = models.DecimalField(default=0,max_digits=10, decimal_places=2,verbose_name="Expectativa de faturamento mensal (Conforme Aditivos)")
    qtd_equipamento_ativo = models.DecimalField(default=0,max_digits=10, decimal_places=0,verbose_name="Equipamentos Ativos", blank=True)
    qtd_equipamento_inativo = models.DecimalField(default=0,max_digits=10, decimal_places=0,verbose_name="Equipamentos Inativos", blank=True)
    equipe_fixa = models.CharField(verbose_name="Equipe fixa",max_length=45, choices=[('Sim', 'Sim'), ('Não', 'Não')],blank=True, null=True)   
    qtd_equipe = models.DecimalField(default=0,max_digits=10, decimal_places=0,verbose_name="Quantidade de equipe", blank=True)
    veiculo = models.DecimalField(default=0,max_digits=10, decimal_places=0,verbose_name="Quantidade de veículos", blank=True)
    pagt_pecas = models.CharField(verbose_name="Quem paga as peças", max_length=45, blank=True, null=True)  
    pagt_corretivas = models.CharField(verbose_name="Quem paga as corretivas", max_length=45, blank=True, null=True)  
    pagt_mensal_demanda = models.CharField(verbose_name="Pagamento é mensal ou por demanda",max_length=45, choices=[('Mensal', 'Mensal'), ('Demanda', 'Demanda')],blank=True, null=True)   
    periodicidade =  models.CharField(verbose_name="Periodicidade das preventivas - (MENSAL/BIMESTRAL/SEMESTRAL/ANUAL)", max_length=45, blank=True,null=True)  
    inicio_contrato =  models.DateField(verbose_name="Inicio do contrato", blank=True,null=True)  
    periodo_renovacao = models.CharField(verbose_name="Periodo de renovação - EX.: 01 (UM) ANO OU 02 (DOIS) ANOS e 12 (DOZE) DIAS)", max_length=45, blank=True,null=True)  
    fim_contrato =  models.DateField(verbose_name="Fim do contrato", blank=True,null=True)   
    data_renovacao = models.DateField(verbose_name="Data de renovação", blank=True,null=True)  
    vigencia_final = models.CharField(verbose_name="Vigência final", max_length=45, blank=True,null=True)  
    prazo_corretiva = models.TextField(verbose_name="Prazo de corretivas", blank=True)
    link_doc = models.CharField(verbose_name="Link dos documentos", max_length=255, blank=True, null=True)     
    
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    registro_atualizado = models.DateTimeField(auto_now=True)
    registro_criado = models.DateTimeField(auto_now_add=True)

    def __str__(self): 
        return self.contrato

    class Meta:
        db_table = 'contrato'


class Atendimento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo = models.CharField(max_length=45, blank=True, null=True, verbose_name='Código')
    cnpj = models.CharField(max_length=25, null=True, blank=True)
    nome = models.CharField(verbose_name="Nome", max_length=45, null=True)   
    endereco = models.CharField(verbose_name="Endereço", max_length=255, blank=True)
    bairro = models.CharField(verbose_name="Bairro", max_length=45, blank=True)
    cidade = models.CharField(verbose_name="Cidade", max_length=45, blank=True)
    uf = models.CharField(verbose_name="UF", max_length=2, blank=True)
    cep = models.CharField(verbose_name="Cep", max_length=9, blank=True) 
    telefone = models.CharField(verbose_name="Telefone", max_length=45, blank=True) 
    email = models.EmailField(verbose_name="Email", max_length=45, blank=True) 
    
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE,blank=True, null=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    registro_atualizado = models.DateTimeField(auto_now=True)
    registro_criado = models.DateTimeField(auto_now_add=True)

    def __str__(self): 
        return self.nome

    class Meta:
        db_table = 'atendimento'


class Tipo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=45, verbose_name='Nome') 
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    registro_atualizado = models.DateTimeField(auto_now=True)
    registro_criado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome
    
    class Meta:
        db_table = 'tipo'

class Equipamento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo = models.CharField(max_length=45, blank=True, null=True, verbose_name='Código')
    tipo = models.CharField(max_length=45, null=True, verbose_name='Tipo')
    atendimento = models.ForeignKey(Atendimento, on_delete=models.CASCADE, verbose_name='Unidade de Atendimento')
    ambiente = models.CharField(max_length=45, blank=True, null=True, verbose_name='Ambiente')
    marca = models.CharField(max_length=45, blank=True, null=True, verbose_name='Marca')  # Campo não obrigatório
    tag = models.CharField(max_length=45, blank=True, null=True, verbose_name='Tag')  # Campo não obrigatório
    numero_serie = models.CharField(max_length=45, blank=True, null=True, verbose_name='Número de Série')  # Campo não obrigatório
    capacidade = models.CharField(max_length=45, blank=True, null=True, verbose_name='Capacidade')  # Campo não obrigatório
    mod_evaporador = models.CharField(max_length=45, blank=True, null=True, verbose_name='Modelo de Evaporador')  # Campo não obrigatório
    mod_condensador = models.CharField(max_length=45, blank=True, null=True, verbose_name='Modelo de Condensador')  # Campo não obrigatório
    gas_refrigerante = models.CharField(max_length=45, blank=True, null=True, verbose_name='Gás Refrigerante')  # Campo não obrigatório

    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    inativo = models.BooleanField(default=False, verbose_name='Inativo')  

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE,blank=True, null=True)
    registro_atualizado = models.DateTimeField(auto_now=True)
    registro_criado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo} - {self.capacidade} - {self.atendimento} - {self.ambiente} - {self.tag}"

    class Meta:
        db_table = 'equipamento'


class Atividade(models.Model):

    MESES = [
        (1, 'Janeiro'),
        (2, 'Fevereiro'),
        (3, 'Março'),
        (4, 'Abril'),
        (5, 'Maio'),
        (6, 'Junho'),
        (7, 'Julho'),
        (8, 'Agosto'),
        (9, 'Setembro'),
        (10, 'Outubro'),
        (11, 'Novembro'),
        (12, 'Dezembro'),
        
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE, verbose_name='Equipamento')
    competencia = models.IntegerField(choices=MESES)
    periodicidade = models.CharField(max_length=45, choices=[('M', 'Mensal'), ('B', 'Bimestral'), ('T', 'Trimestral'), ('S', 'Semestral'), ('A', 'Anual')], verbose_name='Periodicidade da Atividade')
    
    problema = models.TextField(verbose_name="Relatar problema", blank=True)
    inicio_manutencao = models.DateField(blank=True, null=True, verbose_name='Data Início da Manutenção')  # Campo não obrigatório
    ultima_manutencao = models.DateField(blank=True, null=True, verbose_name='Última Manutenção')  # Campo não obrigatório
    termino_manutencao = models.DateField(blank=True, null=True, verbose_name='Data de Término da Manutenção')  # Campo não obrigatório
    status = models.CharField(max_length=45, choices=[('Pendente', 'Pendente'), ('Atrasado', 'Atrasado'), ('Concluído', 'Concluído')], verbose_name='Status', default='Pendente')
    
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE,blank=True, null=True)
    registro_atualizado = models.DateTimeField(auto_now=True)
    registro_criado = models.DateTimeField(auto_now_add=True) 

    def __str__(self): 
       #return self.periodicidade
    
       return f"{self.get_competencia_display()} - {self.inicio_manutencao} a {self.ultima_manutencao}, Atividade: {self.periodicidade}"

    class Meta:
        db_table = 'atividade'






