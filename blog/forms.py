from django import forms
from .models import BlogModel
from ckeditor.widgets import CKEditorWidget

class CreateForm(forms.ModelForm):
    class Meta:
        model = BlogModel
        fields = ['title', 'content', 'image']
        
class B_Post(forms.Form):
    content = forms.CharField(widget=CKEditorWidget())