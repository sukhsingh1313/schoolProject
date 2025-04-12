# forms.py
from django import forms
from django.core.validators import RegexValidator

class ResultSearchForm(forms.Form):
    roll_no = forms.CharField(
        label='Enrollment Number',
        max_length=20,
        validators=[
            RegexValidator(
                regex='^[A-Z0-9/-]+$',
                message='Enter a valid enrollment number'
            )
        ]
    )
    dob = forms.DateField(
        label='Date of Birth',
        widget=forms.DateInput(attrs={'type': 'date'})
    )