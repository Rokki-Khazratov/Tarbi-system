from django import forms
from .models import MonthArchive
import json
from django.core.exceptions import ValidationError

class MonthArchiveForm(forms.ModelForm):
    missed_days = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter missed days as comma-separated values, e.g., 2,4,5,7'}),
        help_text='Enter missed days as comma-separated values, e.g., 2,4,5,7'
    )

    class Meta:
        model = MonthArchive
        fields = ['year', 'month', 'kid', 'missed_days', 'tarif', 'left_sum', 'missday_cost', 'is_paid']

    def clean_missed_days(self):
        missed_days = self.cleaned_data['missed_days']
        try:
            # Convert the comma-separated string into a list of integers
            missed_days_list = [int(day.strip()) for day in missed_days.split(',') if day.strip().isdigit()]
            return json.dumps(missed_days_list)  # Convert the list to a JSON format
        except ValueError:
            raise forms.ValidationError("Invalid format. Ensure you enter only numbers separated by commas.")

    def clean(self):
        cleaned_data = super().clean()
        kid = cleaned_data.get("kid")
        year = cleaned_data.get("year")
        month = cleaned_data.get("month")

        # Check if a record already exists for this kid, year, and month
        if MonthArchive.objects.filter(kid=kid, year=year, month=month).exists():
            raise ValidationError("A record already exists for this kid in this month and year.")

        return cleaned_data
