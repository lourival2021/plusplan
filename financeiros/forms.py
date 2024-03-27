from django.forms import ModelForm
from .models import Financeiro
from django import forms


class MaiusculasTextInput(forms.TextInput):
    def value_from_datadict(self, data, files, name):
        value = super().value_from_datadict(data, files, name)
        return value.upper() if value else value


class FinanceiroForm(ModelForm):
    class Meta:
        model = Financeiro
        fields = ['competencia','preventiva','corretiva','instalacao','pecas','custo']
        widgets = {
            'competencia': MaiusculasTextInput(),
        }