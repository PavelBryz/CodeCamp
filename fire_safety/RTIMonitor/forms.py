from django.forms import ModelForm, TextInput, DateInput
from .models import Incident


class IncidentForm(ModelForm):
    class Meta:
        model = Incident
        fields = ['place', 'date', 'description']

        widgets = {
            'place': TextInput(attrs={'class': 'form-control'}),
            'date': DateInput(attrs={'placeholder': 'dd/mm/YYYY', 'class': 'form-control'}),
            'description': TextInput(attrs={'class': 'form-control'})
        }
