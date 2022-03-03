from django import forms
from django.forms import ModelForm
from string import Template
from .models import TimeData

class TimeEntryDetailForm(forms.Form):
    #created = forms.DateTimeField()
    recorded_date = forms.DateField()
    hours = forms.IntegerField()
    minutes = forms.IntegerField()
    comments = forms.CharField(widget=forms.Textarea)
    overtime = forms.ChoiceField(
        choices=[('base', 'base'), ('overtime', 'overtime')])

class TimeEntryDetailModelForm(ModelForm):
    class Meta:
        model = TimeData
        fields = ['record_date', 'recorded_time', 'comments', 'overtime']

