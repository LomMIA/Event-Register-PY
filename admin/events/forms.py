from django.forms import ModelForm
from django import forms
from .models import Event

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['name','description','starts_at','capacity','location','status']
        widgets = {
            'starts_at': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'
            ),
        }