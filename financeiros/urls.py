from django.contrib import admin
from django.urls import path
from .views import FinanceiroList,ControleFinanceiroList,FinanceiroDelete,FinanceiroCreate,FinanceiroUpdate

urlpatterns = [
   
    path('sistema/controle/financeiros/', ControleFinanceiroList, name='controle_financeiro_list'),
    
    path('sistema/financeiros/<uuid:id>/', FinanceiroList, name='financeiro_list'),
    path('sistema/financeiros/editar/<uuid:id>/', FinanceiroUpdate, name='financeiro_edit'),
    path('sistema/financeiros/excluir/<uuid:id>/', FinanceiroDelete, name='financeiro_delete'),
    path('sistema/financeiros/cadastrar/<uuid:contrato_id>/', FinanceiroCreate, name='financeiro_create'),
]