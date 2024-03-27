from django.contrib import admin
from django.urls import path
from .views import ImprimirPmoc,RespTecnicoList,importar_atividades,ImprimirCronograma,ImprimirEquipamento,RespTecnicoCreate,RespTecnicoUpdate,EmpresaUpdate,EmpresaList,importar_atendimentos,importar_equipamentos,ClienteList,ClienteDelete,ClienteCreate,ClienteUpdate,EquipamentoList,ContratoList,AtendimentoList,ContratoDelete,ContratoCreate,ContratoUpdate,AtendimentoCreate,AtendimentoDelete,AtendimentoUpdate,EquipamentoCreate,EquipamentoUpdate,EquipamentoDelete,AtividadeList,AtividadeCreate,AtividadeDelete,AtividadeUpdate,TipoList,TipoCreate,TipoUpdate,TipoDelete


urlpatterns = [

    path('sistema/imprimir_pmoc/<uuid:id>/', ImprimirPmoc, name='imprimir'),
    path('sistema/imprimir_cronograma/<uuid:id>/', ImprimirCronograma, name='imprimir_cronograma'),
    path('sistema/imprimir_equipamento/<uuid:id>/', ImprimirEquipamento, name='imprimir_equipamento'),

    path('sistema/empresas/', EmpresaList, name='empresa_list'),
    path('sistema/empresas/editar/<uuid:id>/', EmpresaUpdate, name='empresa_edit'),

    path('sistema/resp_tecnico/', RespTecnicoList, name='resp_tecnico_list'),
    path('sistema/resp_tecnico/cadastrar/', RespTecnicoCreate, name='resp_tecnico_create'),
    path('sistema/resp_tecnico/editar/<uuid:id>/', RespTecnicoUpdate, name='resp_tecnico_edit'),

    path('sistema/clientes/', ClienteList, name='cliente_list'),
    path('sistema/clientes/cadastrar/', ClienteCreate, name='cliente_create'),
    path('sistema/clientes/editar/<uuid:id>/', ClienteUpdate, name='cliente_edit'),
    path('sistema/clientes/excluir/<uuid:id>/', ClienteDelete, name='cliente_delete'),

    path('sistema/equipamentos/<uuid:id>/', EquipamentoList, name='equipamento_list'),
    path('sistema/equipamentos/cadastrar/<uuid:id>', EquipamentoCreate, name='equipamento_create'),
    path('sistema/equipamentos/editar/<uuid:id>/', EquipamentoUpdate, name='equipamento_edit'),
    path('sistema/equipamentos/excluir/<uuid:id>/', EquipamentoDelete, name='equipamento_delete'),

    path('sistema/contratos/', ContratoList, name='contrato_list'),
    path('sistema/contratos/cadastrar/', ContratoCreate, name='contrato_create'),
    path('sistema/contratos/editar/<uuid:id>/', ContratoUpdate, name='contrato_edit'),
    path('sistema/contratos/excluir/<uuid:id>/', ContratoDelete, name='contrato_delete'),

    path('sistema/tipos/', TipoList, name='tipo_list'),
    path('sistema/tipos/cadastrar/', TipoCreate, name='tipo_create'),
    path('sistema/tipos/editar/<uuid:id>/', TipoUpdate, name='tipo_edit'),
    path('sistema/tipos/excluir/<uuid:id>/', TipoDelete, name='tipo_delete'),

    path('sistema/atendimentos/<uuid:contrato_id>/', AtendimentoList, name='atendimento_list'),
    path('sistema/atendimentos/cadastrar/<uuid:contrato_id>/', AtendimentoCreate, name='atendimento_create'),
    path('sistema/atendimentos/editar/<uuid:id>/', AtendimentoUpdate, name='atendimento_edit'),
    path('sistema/atendimentos/excluir/<uuid:id>/', AtendimentoDelete, name='atendimento_delete'),

    path('sistema/atividades/<uuid:id>/', AtividadeList, name='periodicidade_list'),
    path('sistema/atividades/cadastrar/<uuid:id>/', AtividadeCreate, name='periodicidade_create'),
    path('sistema/atividades/excluir/<uuid:id>/', AtividadeDelete, name='periodicidade_delete'),
    path('sistema/atividades/editar/<uuid:id>/', AtividadeUpdate, name='periodicidade_edit'),

    path('sistema/import/atendimentos', importar_atendimentos, name='importar_atendimentos'),
    path('sistema/import/equipamentos', importar_equipamentos, name='importar_equipamentos'),
    path('sistema/import/atividades', importar_atividades, name='importar_atividades'),

]