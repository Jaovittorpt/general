from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import ClienteForm
from .models import Cliente

@login_required
def adicionar_clientes(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            return JsonResponse({
                'success': True,
                'client': {
                    'nome': cliente.nome,
                    'email': cliente.email,
                    'nome_da_empresa': cliente.nome_da_empresa,
                    'cnpj': cliente.cnpj,
                    'faturamento': str(cliente.faturamento),
                    'valor_do_contrato': str(cliente.valor_do_contrato),
                    'tempo_de_contrato': cliente.tempo_de_contrato,
                }
            })
        else:
            return JsonResponse({'success': False})
    
    form = ClienteForm()
    clientes = Cliente.objects.all()
    return render(request, 'clientes/adicionar_cliente.html', {'form': form, 'clientes': clientes})

@login_required
def detalhes_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    return render(request, 'clientes/detalhes_cliente.html', {'cliente': cliente})