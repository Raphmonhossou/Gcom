"""from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Utilisateur
from django.contrib.auth.models import User

class InscriptionForm(UserCreationForm):
     class Meta:
         model = User
         fields = ('username', 'email', 'password1', 'password2')
    
     def clean_password2(self):
         password1 = self.cleaned_data['password1']
         password2 = self.cleaned_data['password2']
         if password1 != password2:
             raise forms.ValidationError('Les mots de passe ne correspondent pas.')
         return password2
     """