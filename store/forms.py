from django.forms import ModelForm, TextInput, EmailInput
from django.forms.utils import ErrorList

from .models import Contact


class ParagraphErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()
    def as_divs(self):
        if not self: return ''
        return '<div class="errorlist">%s</div>' % ''.join(['<p class="small error">%s</p>' % e for e in self])

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "phone_number", "mail"]
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'phone_number': TextInput(attrs={'class': 'form-control'}),
            'mail': EmailInput(attrs={'class': 'form-control'})
        }
