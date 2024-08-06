# No arquivo de views do app myapp (myapp/views.py)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .graph_api import GraphAPI
from django.db.models import Sum
from .models import DailyInsight
from .forms import DateFilterForm

@login_required
def fetch_insights(request):
    access_token = 'EAA0SSfZBx8OsBOZC3JzxlUM49Lb7ZAaB26M0cmgA3LZAn3gPptKvn1HfuXLR34TkO4vcWzZBp0wBD80GYqMNGQLYrZCQKpIfRFcO25gO3dcKs3i5ZBB7fKCPCwvDImRfBJZCZAMhoQgRHx7r75DXzTFFypyifzDCHwIZArcNfOZBcDZBMvnGF5yvCpW70Im3dr29fW1YGcVxHv17yZCY9Dejo'
    ad_account_id = '1623385671749376'
    graph_api = GraphAPI(access_token, ad_account_id)
    
    # Obter insights e salvar no banco de dados
    graph_api.get_insights(date_start='2023-01-01', date_stop='2023-01-31')
    
    return render(request, 'plot.html')

@login_required
def insights_view(request):
    form = DateFilterForm(request.GET or None)
    insights = DailyInsight.objects.all()

    date_start = None
    date_stop = None

    if form.is_valid():
        date_start = form.cleaned_data.get('date_start')
        date_stop = form.cleaned_data.get('date_stop')

        if date_start:
            insights = insights.filter(day__gte=date_start)
        if date_stop:
            insights = insights.filter(day__lte=date_stop)

    # Calculando valores agregados
    total_spend = insights.aggregate(total=Sum('spend'))['total'] or 0
    total_purchases = insights.aggregate(total=Sum('purchases'))['total'] or 0
    total_reach = insights.aggregate(total=Sum('reach'))['total'] or 0
    
    if total_purchases > 0:
        cost_per_purchase = total_spend / total_purchases
    else:
        cost_per_purchase = 0

    aggregates = {
        'total_spend': total_spend,
        'total_purchases': total_purchases,
        'cost_per_purchase': round(cost_per_purchase, 2),
        'total_reach': total_reach
    }

    context = {
        'form': form,
        'insights': insights,
        'aggregates': aggregates
    }

    return render(request, 'insight.html', context)
