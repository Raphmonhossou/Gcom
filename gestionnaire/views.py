from django.shortcuts import render

from contact.models import Contact
from gstock.models import CommandeFournisseur, Produit


def dashbord_view(request):
     contacts = Contact.objects.all()
     nbr_contact = Contact.objects.count()
     produits = Produit.objects.all()
     nbr_article = produits.count()
     commande_fournisseurs = CommandeFournisseur.objects.all()
     nbr_commande = commande_fournisseurs.count()
     return render(request,'gestionnaire/dashbord.html',{'nbr_contact':nbr_contact,'nbr_article':nbr_article,'nbr_commande':nbr_commande})
