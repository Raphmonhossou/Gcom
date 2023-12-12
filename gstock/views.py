import datetime
from time import strptime
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.db import models
from gstock.form import CommandeClientForm, CommandeFournisseurForm, LigneCommandeClientFormSet, LigneCommandeForm, LigneCommandeFormSet, ProduitForm
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


def recuperer_prix_article(request,produit_id):
    
     article = get_object_or_404(Produit, id=produit_id)
     prix_produit = article.prix
     return JsonResponse({'prix': prix_produit})



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
 
"""
def afficher_commande_fournisseur(request):
     form = CommandeFournisseurForm()
     formset = LigneCommandeFormSet(instance=CommandeFournisseur())
     commande_fournisseurs = CommandeFournisseur.objects.all()
     nbr = commande_fournisseurs.count()
     return render(request, 'gstock/commande-fournisseur.html', {'form':form,'formset': formset,'commande_fournisseurs':commande_fournisseurs,'nbr':nbr})

     
def commande_fournisseur_view(request):
     if request.method == 'POST':
          form = CommandeFournisseurForm(request.POST)
          formset = LigneCommandeFormSet(request.POST, instance=CommandeFournisseur())
    
          if form.is_valid() and formset.is_valid():
             
             commande = form.save()
             formset.instance = commande
             formset.save()
             
             form = CommandeFournisseurForm()
             formset = LigneCommandeFormSet(instance=CommandeFournisseur())
             commande_fournisseurs = CommandeFournisseur.objects.all()
             nbr = commande_fournisseurs.count()
     
             return render(request, 'gstock/commande-fournisseur.html', {'form':form,'formset': formset,'commande_fournisseurs':commande_fournisseurs,'nbr':nbr})
     else:
          
           form = CommandeFournisseurForm()
           formset = LigneCommandeFormSet(instance=CommandeFournisseur())
           commande_fournisseurs = CommandeFournisseur.objects.all()
           nbr = commande_fournisseurs.count()
          
           return render(request, 'gstock/commande-fournisseur.html', {'form':form,'formset': formset,'commande_fournisseurs':commande_fournisseurs,'nbr':nbr})

def nouvelle_commande_fournisseur_view(request):
     if request.method == 'POST':
          form = CommandeFournisseurForm(request.POST)
          formset = LigneCommandeFormSet(request.POST, instance=CommandeFournisseur())
    
          if form.is_valid() and formset.is_valid():
             
             commande = form.save()
             formset.instance = commande
             formset.save()
             
             form = CommandeFournisseurForm()
             formset = LigneCommandeFormSet(instance=CommandeFournisseur())
             commande_fournisseurs = CommandeFournisseur.objects.all()
             nbr = commande_fournisseurs.count()
     
             return render(request, 'gstock/commande-fournisseur.html', {'form':form,'formset': formset,'commande_fournisseurs':commande_fournisseurs,'nbr':nbr})
     else:
          
           form = CommandeFournisseurForm()
           formset = LigneCommandeFormSet(instance=CommandeFournisseur())
          
           return render(request, 'gstock/nouvelle_commande_fournisseur.html', {'form':form,'formset': formset})

""" 


class CommandeInline():
    form_class = CommandeFournisseurForm
    model = CommandeFournisseur
    template_name = "gstock/commande-fournisseur.html"

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))
       
        self.object = form.save()

        # for every formset, attempt to find a specific formset save function
        # otherwise, just save.
        for name, formset in named_formsets.items():
           
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('stock:liste_commande_fournisseur')

    def formset_produits_valid(self, formset):
        """
        Hook for custom formset saving.Useful if you have multiple formsets
        """
        produits = formset.save(commit=False)  # self.save_formset(formset, contact)
        # add this 2 lines, if you have can_delete=True parameter 
        # set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
        for produit in produits:
            produit.commande = self.object
            produit.save()

   
            

class CreerCommande(CommandeInline, CreateView):

    def get_context_data(self, **kwargs):
        commande_fournisseurs = CommandeFournisseur.objects.all()
        nbr = commande_fournisseurs.count()
         
        ctx = super(CreerCommande, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        ctx['afficherModaleCommandeFournisseur'] = True
        ctx['commande_fournisseurs'] = commande_fournisseurs
        ctx['nbr'] = nbr
        return ctx

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {'produits': LigneCommandeFormSet(prefix='produits'), }
        else:
            return {'produits': LigneCommandeFormSet(self.request.POST or None, self.request.FILES or None, prefix='produits'),}




class ModifierCommande(CommandeInline, UpdateView):
    
    def get_context_data(self, **kwargs):
        commande_fournisseurs = CommandeFournisseur.objects.all()
        nbr = commande_fournisseurs.count()
        
        ctx = super(ModifierCommande, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        ctx['commande_fournisseurs'] = commande_fournisseurs
        ctx['nbr'] = nbr
        ctx['afficherModaleCommandeFournisseur'] = True
        
        return ctx

    def get_named_formsets(self):
        return {
            'produits': LigneCommandeFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='produits'),
        }
          
        


class ListeCommande(ListView):
    model = CommandeFournisseur
    template_name = "gstock/commande-fournisseur.html"
    context_object_name = "commande_fournisseurs"
    
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
        messages.success(request, 'Object Does not exit')
        return redirect('stock:modifier_commande', pk=ligne_commande.produit.id)
    ligne_commande.delete()
    messages.success( request, 'ligne de commande  supprimée')
    return redirect('stock:modifier_commande', pk=ligne_commande.produit.id)


def delete_commande(request, pk):
    try:
        commande = CommandeFournisseur.objects.get(id=pk)
    except CommandeFournisseur.DoesNotExist:
        messages.success(request, 'Object Does not exit')
        return redirect('stock:update_commande', pk=commande.id)

    commande.delete()
    messages.success(request, 'commande  supprimée')
    return redirect('stock:liste_commande_fournisseur')









# ============================gestion des commande client=======================================

def commande_client_view(request):
     if request.method == 'POST':
        # commande_fournisseur_formset = CommandeFournisseurFormSet(request.POST)
          form = CommandeFournisseurForm(request.POST)
          formset = LigneCommandeFormSet(request.POST, instance=CommandeFournisseur())
        # if commande_fournisseur_formset.is_valid():
          if form.is_valid() and formset.is_valid():
             #commande_fournisseur = commande_fournisseur_formset.save()
             commande = form.save()
             formset.instance = commande
             formset.save()
             
            # commande_fournisseur_formset = CommandeFournisseurFormSet()
             form = CommandeFournisseurForm()
             formset = LigneCommandeFormSet(instance=CommandeFournisseur())
             commande_fournisseur = CommandeFournisseur.objects.all()
             nbr = commande_fournisseur.count()
     
             return render(request, 'gstock/commande-client.html', {'form':form,'formset': formset,'commande_fournisseur':commande_fournisseur,'nbr':nbr})
     else:
          #  commande_fournisseur_formset = CommandeFournisseurFormSet()
          #  print(commande_fournisseur_formset)
           form = CommandeFournisseurForm()
           formset = LigneCommandeFormSet(instance=CommandeFournisseur())
           commande_fournisseur = CommandeFournisseur.objects.all()
           nbr = commande_fournisseur.count()
     return render(request, 'gstock/commande-client.html', {'form':form,'formset': formset,'commande_fournisseur':commande_fournisseur,'nbr':nbr})



def recuperer_commande_fournisseur_view(request, commande_fournisseur_id):
      context = {}
      commande_fournisseur = get_object_or_404(CommandeFournisseur, id=commande_fournisseur_id)
      
      form = CommandeFournisseurForm(instance=commande_fournisseur)
      commande_fournisseurs = CommandeFournisseur.objects.all()
      nbr = commande_fournisseur.count()
      afficherModalModification=True
      context = {'commande_modif':commande_fournisseur,'commande_fournisseurs': commande_fournisseurs,'nbr':nbr, 'form': form,'afficherModalModification':afficherModalModification}  
      return render(request, 'gstock/liste-article.html',context)
    
    

def modifier_commande_fournisseur_view(request):
   
    context = {}
    if request.method == 'POST':
        commande_fournisseur_id = request.POST.get('article_id',None)
        
        commande_fournisseur = get_object_or_404(CommandeFournisseur, id=commande_fournisseur_id)
        form = CommandeFournisseurForm(request.POST, instance=commande_fournisseur)
        print(form)
        if form.is_valid():
               form.save()
               form = CommandeFournisseurForm() #vider le form
               commande_fournisseurs = CommandeFournisseur.objects.all()
               nbr = commande_fournisseurs.count()
               context = {'modification_reussi': True,'commande_fournisseurs': commande_fournisseurs,'nbr':nbr,'form': form}
               return render(request,'gstock/liste-article.html',context)
               
             
        else:
               form = CommandeFournisseurForm(instance=commande_fournisseur)
               print(form)
               commande_fournisseurs = CommandeFournisseur.objects.all()
               nbr = commande_fournisseurs.count()
               reponse="formulaire invalide"
               afficherModalModification=True
               context = {'article_modif':commande_fournisseur,'commande_fournisseurs': commande_fournisseurs,'nbr':nbr, 'form': form,'afficherModalModification':afficherModalModification,'reponse':reponse,'modification_reussi': False}
               return render(request, 'gstock/liste-commande_fournisseur.html',context)
 
             
    else:
       
     form = CommandeFournisseurForm()
     commande_fournisseurs = CommandeFournisseur.objects.all()
     nbr = commande_fournisseurs.count()
     return render(request,'gstock/liste-commande_fournisseur.html',{'form': form,'commande_fournisseurs':commande_fournisseurs, 'nbr':nbr})
  
    

def supprimer_commande_fournisseur_view(request,commande_fournisseur_id):
     commande_fournisseur = get_object_or_404(Produit, id=commande_fournisseur_id)
     commande_fournisseur.delete()

     return redirect('liste-article')    

 
class RechercheCommandeFournisseurView(View):
    template_name = 'gstock/liste_commande_fournisseur.html'

    def get(self, request):
        term_recherche = request.GET.get('term_recherche', '')

        commande_fournisseurs = CommandeFournisseur.objects.filter(models.Q(date_commande__icontains=term_recherche) | models.Q(reference__icontains=term_recherche))
        nombre = commande_fournisseurs.count()
        context = {'nombre':nombre,'commande_fournisseurs': commande_fournisseurs, 'term_recherche': term_recherche}
        print(commande_fournisseurs)
        print(nombre)
        
        # Si la requête est une requête AJAX, renvoyer le fragment HTML
        #    if request.is_ajax():
        #        return render(request, 'contact/resultats_recherche.html', context)
         
        if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return render(request, 'gstock/resultats_recherche.html', context)

        return render(request, self.template_name, context)



class ListeCommandeClient(ListView):
    model = CommandeClient
    template_name = "gstock/commande-client.html"
    context_object_name = "commande_clients"
    
    def get_context_data(self, **kwargs):
        commande_clients = CommandeClient.objects.all()
        nbr = commande_clients.count()
        context = super().get_context_data(**kwargs)
        
        context['commande_clients'] = commande_clients
        context['nbr'] = nbr

        return context




class CommandeClientInline():
    form_class = CommandeClientForm
    model = CommandeClient
    template_name = "gstock/commande-client.html"

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save()

        # for every formset, attempt to find a specific formset save function
        # otherwise, just save.
        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('stock:liste_commande_client')

    def formset_produits_valid(self, formset):
        """
        Hook for custom formset saving.Useful if you have multiple formsets
        """
        produits = formset.save(commit=False)  # self.save_formset(formset, contact)
        # add this 2 lines, if you have can_delete=True parameter 
        # set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
        for produit in produits:
            produit.commande = self.object
            produit.save()


class CommandeClientCreate(CommandeClientInline, CreateView):

    def get_context_data(self, **kwargs):
        commande_clients = CommandeClient.objects.all()
        nbr = commande_clients.count()
         
        ctx = super(CommandeClientCreate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        ctx['afficherModaleCommandeClient'] = True
        ctx['commande_clients'] = commande_clients
        ctx['nbr'] = nbr
        return ctx

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {'produits': LigneCommandeClientFormSet(prefix='produits'), }
        else:
            return {'produits': LigneCommandeClientFormSet(self.request.POST or None, self.request.FILES or None, prefix='produits'),}



class UpdateCommandeClient(CommandeClientInline, UpdateView):
   
    def get_context_data(self, **kwargs):
        commande_clients = CommandeClient.objects.all()
        nbr = commande_clients.count()
        ctx = super(UpdateCommandeClient, self).get_context_data(**kwargs)
        ctx['commande_clients'] = commande_clients
        ctx['nbr'] = nbr
        ctx['afficherModaleCommandeClient'] = True
        return ctx

    def get_named_formsets(self):
        return {
            'produits': LigneCommandeClientFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='produits'),
        }




def delete_produit_client(request, pk):
    try:
        produit = LigneCommandeClient.objects.get(id=pk)
    except LigneCommandeClient.DoesNotExist:
        messages.success(request, 'Object Does not exit')
        return redirect('stock:update_commande_client', pk=produit.produit.id)
    produit.delete()
    messages.success( request, 'ligne de commande  supprimée')
    return redirect('stock:update_commande_client', pk=produit.produit.id)


def delete_commande_client(request, pk):
    try:
        commande = CommandeClient.objects.get(id=pk)
    except CommandeClient.DoesNotExist:
        messages.success(request, 'Object Does not exit')
        return redirect('stock:update_commande_client', pk=commande.id)
    commande.delete()
    messages.success( request, 'commande  supprimée')
    return redirect('stock:update_commande_client', pk=commande.id)




    
class RechercheCommandeClientView(View):
    template_name = 'gstock/liste_commande_Client.html'

    def get(self, request):
        term_recherche = request.GET.get('term_recherche', '')

        # Filtrer les articles en fonction du terme de recherche
        #contacts = Contact.objects.filter(name__icontains=term_recherche)
        commande_clients = CommandeClient.objects.filter(models.Q(date_commande__icontains=term_recherche) | models.Q(reference__icontains=term_recherche))
        nombre = commande_clients.count()
        context = {'nombre':nombre,'commande_clients': commande_clients, 'term_recherche': term_recherche}
        
        # Si la requête est une requête AJAX, renvoyer le fragment HTML
        #    if request.is_ajax():
        #        return render(request, 'contact/resultats_recherche.html', context)
         
        if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return render(request, 'gstock/resultats_recherche.html', context)

        return render(request, self.template_name, context)
