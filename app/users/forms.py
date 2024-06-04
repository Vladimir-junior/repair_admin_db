from django import forms
from .models import RepairOrder

class RepairOrderForm(forms.ModelForm):
    class Meta:
        model = RepairOrder
        fields = ['user', 'description_device', 'date_start', 'worker',]
