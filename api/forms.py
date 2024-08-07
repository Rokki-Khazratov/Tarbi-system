from django import forms
from django.contrib.postgres.forms import SimpleArrayField
from .models import MonthArchive

class MonthArchiveForm(forms.ModelForm):
    missed_days = SimpleArrayField(forms.IntegerField())

    class Meta:
        model = MonthArchive
        fields = [
            'year', 'month_name', 'kid', 'missed_days', 'tarif', 'left_sum', 
            'missday_count', 'missday_cost', 'is_paid'
        ]
