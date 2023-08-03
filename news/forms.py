from django import forms
from .models import ContactModel, NewsModel

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactModel
        fields = '__all__'
        
class CreateForm(forms.ModelForm):
    class Meta:
        model = NewsModel
        fields = ['title', 'content', 'image']