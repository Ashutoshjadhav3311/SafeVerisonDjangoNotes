from django import forms
from django.forms import ModelForm, fields
from . models import Notes,RevisionCheckbox

class NotesForm(ModelForm):
    heading = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder":"Enter Title"
    }))
    text = forms.CharField(max_length=500, widget=forms.Textarea(attrs={
         "class": "form-control", "placeholder":"Enter Notes", "rows":"8"
    }))
   
    class Meta:
        model = Notes
        fields = ['heading', 'text']
class RevisionCheckboxForm(forms.ModelForm):
    class Meta:
        model = RevisionCheckbox
        fields = '__all__'