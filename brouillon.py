from django import forms
from django.shortcuts import render, redirect

from gstock.form import CommandeFournisseurForm, LigneCommandeForm, LigneCommandeFormSet
from gstock.models import CommandeFournisseur, LigneCommande, Produit


def ma_vue(request):
    if request.method == 'POST':
        # Si le formulaire est soumis, instancier le formulaire avec les données de la requête
        commande_form = CommandeFournisseurForm(request.POST)
        ligne_commande_form = LigneCommandeForm(request.POST)
        
        if commande_form.is_valid() and ligne_commande_form.is_valid():
            # Enregistrer les instances de modèles si les formulaires sont valides
            commande = commande_form.save()
            ligne_commande = ligne_commande_form.save(commit=False)
            ligne_commande.commande = commande
            ligne_commande.save()
            
            return redirect('nom_de_votre_vue_de_confirmation')
    else:
        # Si c'est une requête GET, instancier les formulaires vides
        commande_form = CommandeFournisseurForm()
        ligne_commande_form = LigneCommandeForm()

    return render(request, 'votre_template.html', {'commande_form': commande_form, 'ligne_commande_form': ligne_commande_form})



def commande_fournisseur_view(request):
    if request.method == 'POST':
        commande_form = CommandeFournisseurForm(request.POST)
        #lignes_commande_formset = LigneCommandeFormSet(request.POST, prefix='lignes_commande')
        lignes_commande_formset = LigneCommandeFormSet(request.POST, instance=CommandeFournisseur())

        if commande_form.is_valid() and lignes_commande_formset.is_valid():
             commande = commande_form.save()
            
             for ligne_form in lignes_commande_formset:
                 ligne_commande = ligne_form.save(commit=False)
                 ligne_commande.commande = commande
                 ligne_commande.save()
            
               # vider les formulaires
                 commande_form = CommandeFournisseurForm()
                 lignes_commande_formset = LigneCommandeFormSet(instance=CommandeFournisseur())

                 commande_fournisseur = CommandeFournisseur.objects.all()
                 nbr = commande_fournisseur.count()
     
                 return render(request, 'gstock/commande-fournisseur.html', {'commande_form': commande_form, 'lignes_commande_formset': lignes_commande_formset,'commande_fournisseur':commande_fournisseur,'nbr':nbr})
    else:
        # Si c'est une requête GET, instancier les formulaires vides
        commande_form = CommandeFournisseurForm()
        lignes_commande_formset = LigneCommandeFormSet(instance=CommandeFournisseur())

    commande_fournisseur = CommandeFournisseur.objects.all()
    nbr = commande_fournisseur.count()   
    return render(request, 'gstock/commande-fournisseur.html', {'commande_form': commande_form, 'lignes_commande_formset': lignes_commande_formset,'commande_fournisseur':commande_fournisseur,'nbr':nbr})


class CommandeFournisseurForm(forms.ModelForm):
    produits = forms.ModelMultipleChoiceField(queryset=Produit.objects.all(), widget=forms.SelectMultiple(attrs={'class': 'select2'}))
    
    class Meta:
        model = CommandeFournisseur
        fields = ['fournisseur', 'date_commande', 'produits', 'statut', 'reference', 'date_reception']
        widgets = {
            'date_commande': forms.DateInput(attrs={'type': 'date'}),
            'date_reception': forms.DateInput(attrs={'type': 'date'}),
            'reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Réference'}),
            'statut': forms.Select(attrs={'class': 'form-control'}),
            'fournisseur': forms.Select(attrs={'class': 'select2'}),
        }



def creer_commande(request):
    if request.method == 'POST':
        form = CommandeFournisseurForm(request.POST)
        if form.is_valid():
            commande = form.save()  # Enregistre la commande principale
            # À ce stade, la commande principale a été enregistrée, et tu peux ajouter les produits associés.
            for produit_id in request.POST.getlist('produits'):
                quantite = request.POST.get(f'quantite_{produit_id}')
                prix_unitaire = request.POST.get(f'prix_unitaire_{produit_id}')
                montant = request.POST.get(f'montant_{produit_id}')
                
                # Crée la ligne de commande associée au produit
                LigneCommande.objects.create(commande=commande, produit_id=produit_id, quantite=quantite, prix_unitaire=prix_unitaire, montant=montant)
                
            return redirect('page_de_confirmation')  # Redirige vers une page de confirmation ou une autre vue
    else:
        form = CommandeFournisseurForm()

 
    return render(request, 'creer_commande.html', {'form': form})

#formulaire en ligne      
#CommandeFournisseurFormSet = formset_factory(CommandeFournisseurForm, LigneCommandeForm, extra=2)
#CommandeFournisseurFormSet = forms.formset_factory(CommandeFournisseurForm, LigneCommandeForm, extra=2)
LigneCommandeFormSet = forms.inlineformset_factory(CommandeFournisseur, LigneCommande, fields=['produit', 'quantite', 'prix_unitaire', 'montant'], extra=1)

# def commande_fournisseur_view(request):
#     if request.method == 'POST':
#         form = CommandeFournisseurForm(request.POST)
#         if form.is_valid():
#             commande = form.save()  # Enregistre la commande principale
#             # À ce stade, la commande principale a été enregistrée, et tu peux ajouter les produits associés.
#             for produit_id in request.POST.getlist('produits'):
#                 quantite = request.POST.get(f'quantite_{produit_id}')
#                 prix_unitaire = request.POST.get(f'prix_unitaire_{produit_id}')
#                 montant = request.POST.get(f'montant_{produit_id}')
                
#                 # Crée la ligne de commande associée au produit
#                 LigneCommande.objects.create(commande=commande, produit_id=produit_id, quantite=quantite, prix_unitaire=prix_unitaire, montant=montant)
             
#             form = CommandeFournisseurForm()
#             commande_fournisseur = CommandeFournisseur.objects.all()
#             nbr = commande_fournisseur.count()
#             return render(request, 'gstock/commande-fournisseur.html', {'form': form,'commande_fournisseur':commande_fournisseur,'nbr':nbr})


#     else:
#         form = CommandeFournisseurForm()
#         commande_fournisseur = CommandeFournisseur.objects.all()
#         nbr = commande_fournisseur.count()
     
#     return render(request, 'gstock/commande-fournisseur.html', {'form': form,'commande_fournisseur':commande_fournisseur,'nbr':nbr})

#  try:
#   pass
# except Exception as e:
#              print(f"Une erreur est survenue lors de l'enregistrement : {str(e)}")
#              form.add_error(None, f"Une erreur est survenue lors de l'enregistrement : {str(e)}")
       
# 'type': forms.RadioSelect(attrs={'class': 'form-check-input radio-inline'}, choices=[('Particulier', 'Particulier'), ('Societe', 'Société')]),
# 'categorie': forms.RadioSelect(attrs={'class': 'form-check-input radio-inline'}, choices=[('Client', 'Client'), ('Prospect', 'Prospect'), ('Fournisseur', 'Fournisseur')]),


# def clean_date_commande(self):
    #     date_commande = self.cleaned_data['date_commande']
    #     # Convertir la date au format correct (YYYY-MM-DD)
    #     formatted_date_commande = date_commande.strftime('%Y-%m-%d')
    #     return formatted_date_commande
    
    
     {% load django_bootstrap5 %}
    {% bootstrap_css %}
    {% bootstrap_javascript %}