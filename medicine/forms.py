from django import forms
from .models import Medicine


class Medicinedata(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = (('name', 'catagory','price'))









