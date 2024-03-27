from django.contrib import admin
from django.urls import path
from .views import PmocList,ControlePmocList,AtividadeUpdate,AtividadeProblemaUpdate

urlpatterns = [
    path('sistema/controle/pmoc/', ControlePmocList, name='controle_list'),
    path('sistema/pmoc/<uuid:id>/', PmocList, name='pmoc_list'),

    path('sistema/pmoc/atividade/<uuid:id>/', AtividadeUpdate, name='atividade_list'),
    path('sistema/pmoc/atividade/problema/<uuid:id>/', AtividadeProblemaUpdate, name='atividade_problema_list'),
    
]