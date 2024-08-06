from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'email', 'nome_da_empresa', 'cnpj', 'faturamento', 'valor_do_contrato', 'tempo_de_contrato']
