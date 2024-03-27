from django.contrib import admin
from .models import Cliente, Contrato, Equipamento, Atividade, Tipo, Atendimento,Empresa, Responsavel_Tecnico

# Register your models here.
admin.site.register(Empresa)
admin.site.register(Cliente)
admin.site.register(Contrato)
admin.site.register(Atividade)
admin.site.register(Tipo)
admin.site.register(Atendimento)
admin.site.register(Equipamento)
admin.site.register(Responsavel_Tecnico)



