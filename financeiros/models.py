from django.db import models
from django.contrib.auth.models import User
from cadastros.models import Contrato # Certifique-se de importar corretamente
import uuid
from django.conf import settings


class Financeiro(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    competencia = models.CharField(verbose_name="Competencia", max_length=45, null=True)  
    preventiva = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preventiva", null=True, blank=True)
    corretiva = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Corretiva", null=True, blank=True)
    instalacao = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Instalação", null=True, blank=True)
    pecas = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Peças", null=True, blank=True)
    custo = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Custo")
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    registro_atualizado = models.DateTimeField(auto_now=True)
    registro_criado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.competencia}' 

    class Meta:
        db_table = 'financeiro'