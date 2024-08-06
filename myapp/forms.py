from django import forms

class DateFilterForm(forms.Form):
    date_start = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    date_stop = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
