from django import forms
from .models import Complaint, ComplaintUpdate

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['category', 'title', 'description', 'priority']
        widgets = {
            'description': forms.Textarea(attrs={'rows':4}),
        }

class ComplaintUpdateForm(forms.ModelForm):
    class Meta:
        model = ComplaintUpdate
        fields = ['status', 'note']
        widgets = {
            'note': forms.Textarea(attrs={'rows':3}),
        }