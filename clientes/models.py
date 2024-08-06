from django.db import models

# Create your models here.
# clientes/models.py

from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    nome_da_empresa = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18)
    faturamento = models.DecimalField(max_digits=10, decimal_places=2)
    valor_do_contrato = models.DecimalField(max_digits=10, decimal_places=2)
    tempo_de_contrato = models.IntegerField(help_text="Tempo de contrato em meses")

    def __str__(self):
        return self.nome
