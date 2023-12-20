import datetime
from genericpath import exists
import json
from time import strptime
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.db import models
from gstock.form import CommandeClientForm, CommandeFournisseurForm, LigneCommandeClientForm, LigneCommandeForm, ProduitForm
from gstock.models import CommandeClient, CommandeFournisseur, LigneCommande, LigneCommandeClient, Produit
from django.contrib import messages
from django.views.generic import ListView
from django.views.generic.edit import (CreateView, UpdateView)


# ============================gestion des articles ==================================


def liste_article_view(request):
          form = ProduitForm()
          produits = Produit.objects.all()
          nbr = produits.count()
          return render(request,'gstock/liste-article.html',{'form': form,'produits':produits, 'nbr':nbr})

    

def ajouter_article(request):
    
     if request.method == 'POST':
       
          form = ProduitForm(request.POST, request.FILES)
       
          if form.is_valid():
               form.save()  
               form = ProduitForm()
               produits = Produit.objects.all()
               nbr = produits.count()
               return render(request,'gstock/liste-article.html',{'form': form,'produits':produits, 'nbr':nbr,'ajout_reussi':True})

          else:
               
               produits = Produit.objects.all()
               nbr = produits.count()
               reponse="formulaire invalide"
               afficherModal=True
               context = {'produits': produits,'nbr':nbr, 'form': form,'afficherModal':afficherModal,'reponse':reponse,'ajout_reussi': False}
               return render(request, 'gstock/liste-article.html',context)
 
               
               
     return liste_article_view(request)
     



def recuperer_article_view(request, article_id):
      context = {}
      article = get_object_or_404(Produit, id=article_id)
      
      form = ProduitForm(instance=article)
      produits = Produit.objects.all()
      nbr = produits.count()
      afficherModalModification=True
      context = {'article_modif':article,'produits': produits,'nbr':nbr, 'form': form,'afficherModalModification':afficherModalModification}  
      return render(request, 'gstock/liste-article.html',context)
    


def modifier_article_view(request):
   
    context = {}
    if request.method == 'POST':
        article_id = request.POST.get('article_id',None)
        
        article = get_object_or_404(Produit, id=article_id)
        form = ProduitForm(request.POST, instance=article)
        print(form)
        if form.is_valid():
               form.save()
               form = ProduitForm() #vider le form
               produits = Produit.objects.all()
               nbr = produits.count()
               context = {'modification_reussi': True,'produits': produits,'nbr':nbr,'form': form}
               return render(request,'gstock/liste-article.html',context)
               
             
        else:
               form = ProduitForm(instance=article)
               print(form)
               produits = Produit.objects.all()
               nbr = produits.count()
               reponse="formulaire invalide"
               afficherModalModification=True
               context = {'article_modif':article,'produits': produits,'nbr':nbr, 'form': form,'afficherModalModification':afficherModalModification,'reponse':reponse,'modification_reussi': False}
               return render(request, 'gstock/liste-article.html',context)
 
             
    else:
       
     form = ProduitForm()
     produits = Produit.objects.all()
     nbr = produits.count()
     return render(request,'gstock/liste-article.html',{'form': form,'produits':produits, 'nbr':nbr})
  
    

def supprimer_article_view(request,article_id):
     article = get_object_or_404(Produit, id=article_id)
     article.delete()

     return liste_article_view(request)


def recuperer_prix_article(request):
        produit_id = request.GET.get('produit', None)
        
        if produit_id is not None:
            try:
                produit = Produit.objects.get(pk=produit_id)
                data =  { 
                        'prix_achat': produit.prix_achat,
                        'prix_vente': produit.prix_vente,
                        'libele':produit.libele
                        }
                return JsonResponse(data)
            except Produit.DoesNotExist:
                return JsonResponse({'error': 'Produit non trouvé'}, status=404)
        else:
            return JsonResponse({'error': 'Paramètre produit manquant'}, status=400)
    
        # article = get_object_or_404(Produit, id=produit_id)
        # prix_produit = article.prix
        # return JsonResponse({'prix': prix_produit})



class RechercheArticleView(View):
    template_name = 'gstock/recherche_article.html'

    def get(self, request):
        term_recherche = request.GET.get('term_recherche', '')

        # Filtrer les articles en fonction du terme de recherche
        #contacts = Contact.objects.filter(name__icontains=term_recherche)
        produits = Produit.objects.filter(models.Q(libele__icontains=term_recherche) | models.Q(code__icontains=term_recherche))
        nombre = produits.count()
        context = {'nombre':nombre,'produits': produits, 'term_recherche': term_recherche}
        
        # Si la requête est une requête AJAX, renvoyer le fragment HTML
        #    if request.is_ajax():
        #        return render(request, 'contact/resultats_recherche.html', context)
         
        if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return render(request, 'gstock/resultats_recherche.html', context)

        return render(request, self.template_name, context)




    
    
def stock_view(request):
     produits = Produit.objects.all()
     nbr = produits.count()
     print(produits)
     return render(request,'gstock/stock.html',{'produits':produits, 'nbr':nbr})




   #========================= gestion des commandes fournisseur============================
 

def nouvelle_commande_fournisseur_view(request):
     montant_commande = 0.00
     if request.method == 'POST':
          form = CommandeFournisseurForm(request.POST)
         
           
          ligne_form = LigneCommandeForm()
          if form.is_valid():
            commande = form.save()
            
            lignes_commande_data = form.cleaned_data.get('lignes_commande_data')   # recuperer le champ de ligne de commande qui est dans form         
           
            for ligne_data in lignes_commande_data:
                ligne_data['commande'] = commande.id
                ligne_data['produit'] = ligne_data['id_produit']
               
                try:
                    produit = get_object_or_404(Produit, id=ligne_data['produit']) # obtenir le produit pour augmenter sa quantite
                    nombre_p=produit.quantite
                    nombre_p += int(ligne_data['quantite']) # augmenter la quantite du produit en stock
                    produit.quantite=nombre_p
                    produit.save()
                except Produit.DoesNotExist:
                    print('produit inexistant')
               
                ligne_form = LigneCommandeForm(data=ligne_data)
                montant_commande += float(ligne_data['montant'])
                if ligne_form.is_valid():
                    ligne_form.save()
            
            commande.montant = montant_commande 
            commande.save()
            form = CommandeFournisseurForm()
            commande_fournisseurs = CommandeFournisseur.objects.all()
            nbr = commande_fournisseurs.count()
            context={'form':form,'commande_fournisseurs':commande_fournisseurs,'nbr':nbr ,'ajout_reussi':True}
            return render(request, 'gstock/commande-fournisseur.html',context )
            #return redirect('gstock:liste_commande_fournisseur',context=context )
     else:
           form = CommandeFournisseurForm()
           ligne_form=LigneCommandeForm()
           return render(request, 'gstock/nouvelle_commande_fournisseur.html', {'form':form,'ligne_form':ligne_form,'ajout_reussi':False})



def recuperer_commande_fournisseur_view(request, commande_fournisseur_id):
    
      commande_fournisseur = get_object_or_404(CommandeFournisseur, id=commande_fournisseur_id)
      form = CommandeFournisseurForm(instance=commande_fournisseur)
      ligne_commande = LigneCommande.objects.filter(commande=commande_fournisseur)
      
      
      ligne_form=LigneCommandeForm()
    
      return render(request, 'gstock/modifier_commande_fournisseur.html', {'form':form,'ligne_form':ligne_form,'commande_fournisseur_id':commande_fournisseur_id,'ligne_commande':ligne_commande})

    
    

def modifier_commande_fournisseur_view(request):
    montant_commande = 0.00
    context = {}
    if request.method == 'POST':
        commande_fournisseur_id = request.POST.get('commande_fournisseur_id',None)
        
        commande_fournisseur = get_object_or_404(CommandeFournisseur, id=commande_fournisseur_id)
        form = CommandeFournisseurForm(request.POST, instance=commande_fournisseur)
        print(form)
        if form.is_valid():
               commande =  form.save()
               LigneCommande.objects.filter(commande=commande).delete()
           
               lignes_commande_data = form.cleaned_data.get('lignes_commande_data')   # recuperer le champ de ligne de commande qui est dans form         
               
               print(lignes_commande_data)
               for ligne_data in lignes_commande_data:
                    produit_id = ligne_data['id_produit']
                    produit = get_object_or_404(Produit, id=produit_id)
                    ligne_data['prix_achat'] = ligne_data['prix_achat'].replace(' ', '').replace(',', '.') # supprimer les espaces et remplacer ','  par '.' comme separateur decimal
                    ligne_data['montant'] = ligne_data['montant'].replace(' ', '').replace(',', '.')
                    ligne_commande = LigneCommande()
                    ligne_commande.commande = commande
                    ligne_commande.produit = produit
                    ligne_commande.prix_achat = ligne_data.get('prix_achat')
                    ligne_commande.quantite = ligne_data.get('quantite')
                    ligne_commande.montant = ligne_data.get('montant')
                    montant_commande += float(ligne_data.get('montant'))
                    ligne_commande.save()
                    
               commande.montant = montant_commande
               commande.save()
               form = CommandeFournisseurForm()
               commande_fournisseurs = CommandeFournisseur.objects.all()
               nbr = commande_fournisseurs.count()
               context = {'modification_reussi': True,'commande_fournisseurs': commande_fournisseurs,'nbr':nbr}
               return render(request,'gstock/commande-fournisseur.html',context)
               
             
        else:
               print("une erreur est survenue lors de l'enregistrement d'un produit") 
               form = CommandeFournisseurForm(instance=commande_fournisseur)
               reponse="formulaire invalide, réessayez"
               ligne_commande = LigneCommande.objects.filter(commande=commande_fournisseur)
               ligne_form=LigneCommandeForm()
               return render(request, 'gstock/modifier_commande_fournisseur.html', {'form':form,'ligne_form':ligne_form,'ligne_commande':ligne_commande})

             
    else:
        commande_fournisseur = get_object_or_404(CommandeFournisseur, id=commande_fournisseur_id)
        form = CommandeFournisseurForm(instance=commande_fournisseur)
        ligne_commande = LigneCommande.objects.filter(commande=commande_fournisseur)
        
        ligne_form=LigneCommandeForm()
        
        return render(request, 'gstock/modifier_commande_fournisseur.html', {'form':form,'ligne_form':ligne_form,'ligne_commande':ligne_commande})

    
    
def detail_commande_fournisseur_view(request, commande_fournisseur_id):
      commande_fournisseur = get_object_or_404(CommandeFournisseur, id=commande_fournisseur_id)
      ligne_commande = LigneCommande.objects.filter(commande=commande_fournisseur)
    
      return render(request, 'gstock/details_commande_fournisseur.html', {'commande_fournisseur_id':commande_fournisseur_id,'commande_fournisseur':commande_fournisseur,'ligne_commande':ligne_commande})



class ListeCommande(ListView):
    model = CommandeFournisseur
    template_name = "gstock/commande-fournisseur.html"
    # context_object_name = "commande_fournisseurs"
    
    def get_context_data(self, **kwargs):
        commande_fournisseurs = CommandeFournisseur.objects.all()
        nbr = commande_fournisseurs.count()
        context = super().get_context_data(**kwargs)
        
        context['commande_fournisseurs'] = commande_fournisseurs
        context['nbr'] = nbr

        return context

     



def delete_produit(request, pk):
    try:
        ligne_commande = LigneCommande.objects.get(id=pk)
    except LigneCommande.DoesNotExist:
        messages.success(request, 'ligne inexistante')
        return redirect('stock:modifier_commande', pk=ligne_commande.produit.id)
    ligne_commande.delete()
    messages.success( request, 'ligne de commande  supprimée')
    return redirect('stock:modifier_commande', pk=ligne_commande.produit.id)


def delete_commande(request, pk):
    try:
        commande = CommandeFournisseur.objects.get(id=pk)
    except CommandeFournisseur.DoesNotExist:
        messages.success(request, 'commande déja supprimée ')
        return redirect('stock:liste_commande_fournisseur', pk=commande.id)

    commande.delete()
    messages.success(request, 'commande supprimée')
    return redirect('stock:liste_commande_fournisseur')



class RechercheCommandeFournisseurView(View):
    template_name = 'gstock/liste_commande_fournisseur.html'

    def get(self, request):
        term_recherche = request.GET.get('term_recherche', '')

        # Filtrer les articles en fonction du terme de recherche
        
        commandes = CommandeFournisseur.objects.filter(models.Q(reference__icontains=term_recherche) | models.Q(date_commande__icontains=term_recherche))
        nombre = commandes.count()
        context = {'nombre':nombre,'commandes': commandes, 'term_recherche': term_recherche}
        
        if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return render(request, 'gstock/resultats_recherche.html', context)

        return render(request, self.template_name, context)






# ============================gestion des commande client=======================================
 

def nouvelle_commande_client_view(request):
     montant_commande = 0.00
     if request.method == 'POST':
          form = CommandeClientForm(request.POST)
         
           
          ligne_form = LigneCommandeClientForm()
          if form.is_valid():
            commande = form.save()
            
            lignes_commande_data = form.cleaned_data.get('lignes_commande_data')   # recuperer le champ de ligne de commande qui est dans form         
           
            for ligne_data in lignes_commande_data:
                ligne_data['commande'] = commande.id
                ligne_data['produit'] = ligne_data['id_produit']
               
                try:
                    produit = get_object_or_404(Produit, id=ligne_data['produit']) # obtenir le produit pour augmenter sa quantite
                    nombre_p=produit.quantite
                    nombre_p -= int(ligne_data['quantite']) # augmenter la quantite du produit en stock
                    produit.quantite=nombre_p
                    produit.save()
                except Produit.DoesNotExist:
                    print('produit inexistant')
               
                ligne_form = LigneCommandeClientForm(data=ligne_data)
                montant_commande += float(ligne_data['montant'])
                if ligne_form.is_valid():
                    ligne_form.save()
            
            commande.montant = montant_commande 
            commande.save()
            form = CommandeClientForm()
            commande_clients = CommandeClient.objects.all()
            nbr = commande_clients.count()
            context={'form':form,'commande_clients':commande_clients,'nbr':nbr ,'ajout_reussi':True}
            return render(request, 'gstock/commande-client.html',context )
            
     else:
           form = CommandeClientForm()
           ligne_form=LigneCommandeClientForm()
           return render(request, 'gstock/nouvelle_commande_client.html', {'form':form,'ligne_form':ligne_form,'ajout_reussi':False})



def recuperer_commande_client_view(request, commande_client_id):
    
      commande_client = get_object_or_404(CommandeClient, id=commande_client_id)
      form = CommandeClientForm(instance=commande_client)
      ligne_commande = LigneCommandeClient.objects.filter(commande=commande_client)
      
      
      ligne_form=LigneCommandeClientForm()
    
      return render(request, 'gstock/modifier_commande_client.html', {'form':form,'ligne_form':ligne_form,'commande_client_id':commande_client_id,'ligne_commande':ligne_commande})

    
    

def modifier_commande_client_view(request):
    montant_commande = 0.00
    context = {}
    if request.method == 'POST':
        commande_client_id = request.POST.get('commande_client_id',None)
        
        commande_client = get_object_or_404(CommandeClient, id=commande_client_id)
        form = CommandeClientForm(request.POST, instance=commande_client)
        print(form)
        if form.is_valid():
               commande_client =  form.save()
               LigneCommandeClient.objects.filter(commande=commande_client).delete()
           
               lignes_commande_data = form.cleaned_data.get('lignes_commande_data')   # recuperer le champ de ligne de commande qui est dans form         
               
               print(lignes_commande_data)
               for ligne_data in lignes_commande_data:
                    produit_id = ligne_data['id_produit']
                    produit = get_object_or_404(Produit, id=produit_id)
                    ligne_data['prix_vente'] = ligne_data['prix_vente'].replace(' ', '').replace(',', '.') # supprimer les espaces et remplacer ','  par '.' comme separateur decimal
                    ligne_data['montant'] = ligne_data['montant'].replace(' ', '').replace(',', '.')
                    ligne_commande = LigneCommandeClient()
                    ligne_commande.commande = commande_client
                    ligne_commande.produit = produit
                    ligne_commande.prix_vente = ligne_data.get('prix_vente')
                    ligne_commande.quantite = ligne_data.get('quantite')
                    ligne_commande.montant = ligne_data.get('montant')
                    montant_commande += float(ligne_data.get('montant'))
                    ligne_commande.save()
                    
               commande_client.montant = montant_commande
               commande_client.save()
               form = CommandeClientForm()
               commande_clients = CommandeClient.objects.all()
               nbr = commande_clients.count()
               context = {'modification_reussi': True,'commande_clients': commande_clients,'nbr':nbr}
               return render(request,'gstock/commande-client.html',context)
               
             
        else:
               print("une erreur est survenue lors de l'enregistrement d'un produit") 
               form = CommandeClientForm(instance=commande_client)
               reponse="formulaire invalide, réessayez"
               ligne_commande = LigneCommandeClient.objects.filter(commande=commande_client)
               ligne_form=LigneCommandeClientForm()
               return render(request, 'gstock/modifier_commande_client.html', {'form':form,'ligne_form':ligne_form,'ligne_commande':ligne_commande})

             
    else:
        commande_client = get_object_or_404(CommandeClient, id=commande_client_id)
        form = CommandeClientForm(instance=commande_client)
        ligne_commande = LigneCommandeClient.objects.filter(commande=commande_client)
        
        ligne_form=LigneCommandeClientForm()
        
        return render(request, 'gstock/modifier_commande_client.html', {'form':form,'ligne_form':ligne_form,'ligne_commande':ligne_commande})

    
    
def detail_commande_client_view(request, commande_client_id):
      commande_client = get_object_or_404(CommandeClient, id=commande_client_id)
      ligne_commande = LigneCommandeClient.objects.filter(commande=commande_client)
    
      return render(request, 'gstock/details_commande_client.html', {'commande_client_id':commande_client_id,'commande_client':commande_client,'ligne_commande':ligne_commande})



class ListeCommandeClient(ListView):
    model = CommandeClient
    template_name = "gstock/commande-client.html"
    
    
    def get_context_data(self, **kwargs):
        commande_clients = CommandeClient.objects.all()
        nbr = commande_clients.count()
        context = super().get_context_data(**kwargs)
        
        context['commande_clients'] = commande_clients
        context['nbr'] = nbr

        return context

     



def delete_produit_vente(request, pk):
    try:
        ligne_commande = LigneCommandeClient.objects.get(id=pk)
    except LigneCommandeClient.DoesNotExist:
        messages.success(request, 'commande n\'existe pas')
        return redirect('stock:modifier_commande_client', pk=ligne_commande.produit.id)
    ligne_commande.delete()
    messages.success( request, 'ligne de commande  supprimée')
    return redirect('stock:modifier_commande_client', pk=ligne_commande.produit.id)


def delete_commande_vente(request, pk):
    try:
        commande = CommandeClient.objects.get(id=pk)
    except CommandeClient.DoesNotExist:
        messages.success(request, 'la commande n\'existe pas ')
        return redirect('stock:update_commande_client', pk=commande.id)

    commande.delete()
    messages.success(request, 'commande  supprimée')
    return redirect('stock:liste_commande_client')




class RechercheCommandeClientView(View):
    template_name = 'gstock/liste_commande_client.html'

    def get(self, request):
        term_recherche = request.GET.get('term_recherche', '')

        commandes = CommandeClient.objects.filter(models.Q(reference__icontains=term_recherche) | models.Q(date_commande__icontains=term_recherche))
        nombre = commandes.count()
        context = {'nombre':nombre,'commandes': commandes, 'term_recherche': term_recherche}
        
        if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return render(request, 'gstock/resultats_recherche.html', context)

        return render(request, self.template_name, context)

