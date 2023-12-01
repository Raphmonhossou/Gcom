
from django.core import validators
import re
from django import forms
from contact.models import Contact
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

class ContactForm(forms.ModelForm):
      
      phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Téléphone'}),
        validators=[
            validators.RegexValidator(
                regex='^\d{8}$',  # La regex '\d{8}' signifie exactement 8 chiffres
                message='Veuillez saisir exactement 8 chiffres.',
                code='invalid_phone'
            )
        ]
    )
      class Meta:
            model = Contact
            # fields = ('name','email','phone','ifu','categorie','type','adress')
            fields = '__all__'

            widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom complet'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Téléphone'}),
            'ifu': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ifu','min':'1'}),
            'categorie': forms.Select(attrs={'class': 'form-control'}, choices=[('Client', 'Client'), ('Prospect', 'Prospect'), ('Fournisseur', 'Fournisseur')]),
            'type': forms.Select(attrs={'class': 'form-control'}, choices=[('Particulier', 'Particulier'), ('Societe', 'Société')]),
            'adress': forms.Textarea(attrs={'class': 'form-control','rows':3, 'placeholder': 'Adresse'}),
            # 'type': forms.RadioSelect(attrs={'class': 'form-check-input radio-inline'}, choices=[('Particulier', 'Particulier'), ('Societe', 'Société')]),
            # 'categorie': forms.RadioSelect(attrs={'class': 'form-check-input radio-inline'}, choices=[('Client', 'Client'), ('Prospect', 'Prospect'), ('Fournisseur', 'Fournisseur')]),

       
        }
  
      
  
  
  

    #   def clean_phone(self):
    #     phone = self.cleaned_data.get('phone')
    #     if not re.match(r'^\d{8}$', phone):
    #         raise forms.ValidationError(
    #              _('Le numéro de téléphone doit être composé de 8 chiffres.'),
    #             code='invalid_phone_number'
    #         )
    #     return phone