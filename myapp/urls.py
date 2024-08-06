from django.urls import path
from .views import fetch_insights,insights_view

urlpatterns = [
    path('plot/', fetch_insights, name='fetch_insights'),
    path('insights/', insights_view, name='insights'),
]
