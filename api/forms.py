from django import forms
from .models import MonthArchive
import json

class MonthArchiveForm(forms.ModelForm):
    missed_days = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = MonthArchive
        fields = [
            'year', 'month', 'kid', 'missed_days', 'tarif', 'left_sum', 
            'missday_cost', 'is_paid'
        ]

    def clean_missed_days(self):
        missed_days = self.cleaned_data['missed_days']
        try:
            # Ensure the data is valid JSON
            data = json.loads(missed_days)
            if not isinstance(data, list) or not all(isinstance(i, int) for i in data):
                raise forms.ValidationError("Invalid format for missed_days. Must be a list of integers.")
        except json.JSONDecodeError:
            raise forms.ValidationError("Invalid JSON format.")
        return missed_days
