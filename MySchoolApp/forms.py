# forms.py
from django import forms
from .models import News_session

class NewsSessionAdminForm(forms.ModelForm):
    class Meta:
        model = News_session
        fields = '__all__'

    short_post_text = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Enter short post text here...'})
    )
