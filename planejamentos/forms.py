from django.forms import ModelForm
from .models import Atividade
from django import forms


class MaiusculasTextInput(forms.TextInput):
    def value_from_datadict(self, data, files, name):
        value = super().value_from_datadict(data, files, name)
        return value.upper() if value else value


class AtividadeForm(ModelForm):
    class Meta:
        model = Atividade      
        fields = ['inicio_manutencao','termino_manutencao','problema','status']
        
        widgets = {
            'inicio_manutencao': forms.TextInput(attrs={'class': 'datepicker'}),
            'termino_manutencao': forms.TextInput(attrs={'class': 'datepicker'}),
        }

        
class AtividadeProblemaForm(ModelForm):
    class Meta:
        model = Atividade      
        fields = ['problema']

        widgets = {
            'problema': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'readonly': 'readonly'}),  
        }
        
        
        

    