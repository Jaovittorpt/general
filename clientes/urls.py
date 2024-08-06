from django.urls import path
from .views import adicionar_clientes, detalhes_cliente

urlpatterns = [
    path('adicionar/', adicionar_clientes, name='adicionar-cliente'),
    path('clientes/<int:cliente_id>/', detalhes_cliente, name='detalhes-cliente'),
]

