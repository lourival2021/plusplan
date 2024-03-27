from django.forms import ModelForm
from .models import Cliente,Equipamento,Contrato,Atendimento,Atividade,Tipo,Empresa,Responsavel_Tecnico
from django import forms


class MaiusculasTextInput(forms.TextInput):
    def value_from_datadict(self, data, files, name):
        value = super().value_from_datadict(data, files, name)
        return value.upper() if value else value
    
class MaskedCEPInput(forms.TextInput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs.update({'maxlength': '9', 'pattern': '[0-9]{5}-[0-9]{3}', 'placeholder': '00000-000'})
    

class EmpresaForm(ModelForm):
    cep = forms.CharField(max_length=9, widget=MaskedCEPInput())
    class Meta:
        model = Empresa
        fields = ['tipo_documento', 'cpf', 'cnpj', 'nome', 'endereco', 'bairro', 'cidade', 'uf', 'cep','telefone','email','resp_tecnico']
        widgets = {
            'nome': MaiusculasTextInput(),
            'endereco': MaiusculasTextInput(),
            'bairro': MaiusculasTextInput(),
            'cidade': MaiusculasTextInput(),
            'uf': MaiusculasTextInput(),
            'cep': MaiusculasTextInput(),
            'telefone': forms.TextInput(attrs={'type': 'tel'}),
            'email': forms.EmailInput(),
            'resp_tecnico': MaiusculasTextInput(),
        }


class RespTecnicoForm(ModelForm):
    cep = forms.CharField(max_length=9, widget=MaskedCEPInput())
    class Meta:
        model = Responsavel_Tecnico
        fields = ['tipo_documento', 'cpf', 'cnpj', 'nome', 'endereco', 'bairro', 'cidade', 'uf', 'cep','telefone','email','art','rigistro_conselho']
        widgets = {
            'nome': MaiusculasTextInput(),
            'endereco': MaiusculasTextInput(),
            'bairro': MaiusculasTextInput(),
            'cidade': MaiusculasTextInput(),
            'uf': MaiusculasTextInput(),
            'cep': MaiusculasTextInput(),
            'telefone': forms.TextInput(attrs={'type': 'tel'}),
            'email': forms.EmailInput(),
            'art': MaiusculasTextInput(),
            'rigistro_conselho': MaiusculasTextInput(),
        }


class ClienteForm(ModelForm):
    cep = forms.CharField(max_length=9, widget=MaskedCEPInput())
    class Meta:
        model = Cliente
        fields = ['tipo_documento', 'cpf', 'cnpj', 'nome', 'endereco', 'bairro', 'cidade', 'uf', 'cep','telefone','email']
        
        widgets = {
            'nome': MaiusculasTextInput(),
            'endereco': MaiusculasTextInput(),
            'bairro': MaiusculasTextInput(),
            'cidade': MaiusculasTextInput(),
            'uf': MaiusculasTextInput(),
            'cep': MaiusculasTextInput(),
            'telefone': forms.TextInput(attrs={'type': 'tel'}),
            'email': forms.EmailInput(),
        }
    

class EquipamentoForm(ModelForm):
    class Meta:
        model = Equipamento      
        exclude = ['usuario','atendimento','codigo']

    def clean(self):
        cleaned_data = super().clean()
        ativo = cleaned_data.get('ativo')
        inativo = cleaned_data.get('inativo')

        if ativo == inativo == False:
            raise forms.ValidationError("Por favor, selecione um estado: ativo ou inativo.")

        if ativo and inativo:
            raise forms.ValidationError("Por favor, selecione apenas um estado: ativo ou inativo.")

        return cleaned_data


class TipoForm(ModelForm):
    class Meta:
        model = Tipo      
        exclude = ['usuario']
        

class AtividadeForm(ModelForm):
    class Meta:
        model = Atividade      
        fields = ['competencia','periodicidade']
        
        widgets = {
            'inicio_manutencao': forms.TextInput(attrs={'class': 'datepicker'}),
            'termino_manutencao': forms.TextInput(attrs={'class': 'datepicker'}),
        }


class ContratoForm(ModelForm):
   
    class Meta:

        model = Contrato
        #fields = "__all__"
        exclude = ['usuario','empresa']
        widgets = {
            'contrato': MaiusculasTextInput(),
            'pregao': MaiusculasTextInput(),

            'inicio_contrato': forms.TextInput(attrs={'class': 'datepicker'}),
            'fim_contrato': forms.TextInput(attrs={'class': 'datepicker'}),
            'data_renovacao': forms.TextInput(attrs={'class': 'datepicker'}),
            'qtd_equipamento_ativo': forms.TextInput(attrs={'readonly': 'readonly'}),
            'qtd_equipamento_inativo': forms.TextInput(attrs={'readonly': 'readonly'}),
        }
        

class AtendimentoForm(forms.ModelForm):
    cep = forms.CharField(max_length=9, widget=MaskedCEPInput())
    class Meta:
        model = Atendimento
        fields = ['nome', 'endereco', 'bairro', 'cidade', 'uf', 'cep', 'telefone', 'email']
        widgets = {
            'nome': MaiusculasTextInput(),
            'endereco': MaiusculasTextInput(),
            'bairro': MaiusculasTextInput(),
            'cidade': MaiusculasTextInput(),
            'uf': MaiusculasTextInput(),
            'telefone': forms.TextInput(attrs={'type': 'tel'}),
            'email': forms.EmailInput(),
        }
    


