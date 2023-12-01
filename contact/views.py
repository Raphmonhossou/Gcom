from multiprocessing import context
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.db import models
from contact.form import ContactForm

from contact.models import Contact

    
    # affichage et ajout de contact
    
def afficher_contact_view(request, **kwargs):
      form = ContactForm()
      contacts = Contact.objects.all()
      nbr = Contact.objects.count()
      context = {'contacts': contacts,'nbr':nbr, 'form': form, **kwargs}
      return render(request,'contact/liste-contact.html',context)
       
       
       
def ajouter_contact_view(request):
     calling_page = request.GET.get('calling_page', '/')
     print('page apellant recuperer :'+calling_page)
     
     context = {}
     if request.method == 'POST':
          form = ContactForm(request.POST)
          if form.is_valid():
              form.save()  
                  
              if calling_page=="/contact/":
                contacts = Contact.objects.all()
                nbr = contacts.count()
                context = {'ajout_reussi': True,'contacts': contacts,'nbr':nbr,'form': form}
                return render(request,'contact/liste-contact.html',context)
                
              elif calling_page=="/contact/clients/":
                contacts_clients = Contact.objects.filter(categorie='Client')
                nbr = contacts_clients.count()
                context = {'ajout_reussi': True,'contacts_clients': contacts_clients,'nbr':nbr,'form': form}
                return render(request,'contact/liste-client.html',context)
                
              elif calling_page=="/contact/prospects/":
                contacts_prospects = Contact.objects.filter(categorie='Prospect')
                nbr = contacts_prospects.count()
                context = {'ajout_reussi': True,'contacts_prospects': contacts_prospects,'nbr':nbr,'form': form}
                return render(request,'contact/liste-prospect.html',context)
                
                
              elif calling_page=="/contact/fournisseurs/":
                contacts_fournisseurs = Contact.objects.filter(categorie='Fournisseur')
                nbr = contacts_fournisseurs.count()
                context = {'ajout_reussi': True,'contacts_fournisseurs': contacts_fournisseurs,'nbr':nbr,'form': form}
                return render(request,'contact/liste-fournisseur.html',context)
                
                
              elif calling_page=="/contact/societes/":
                contacts_societes = Contact.objects.filter(type='Societe')
                nbr = contacts_societes.count()
                context = {'ajout_reussi': True,'contacts_societes': contacts_societes,'nbr':nbr,'form': form}
                return render(request,'contact/liste-societe.html',context)
                  
              elif calling_page=="/contact/particuliers/":
                contacts_particuliers = Contact.objects.filter(type='Particulier')
                nbr = contacts_particuliers.count()
                context = {'ajout_reussi': True,'contacts_particuliers': contacts_particuliers,'nbr':nbr,'form': form}
                return render(request,'contact/liste-particulier.html',context)
                
               
          else:
              reponse="formulaire invalide"
              afficherModal=True
             
              contacts = Contact.objects.all()
              nbr = contacts.count()
              context = {'ajout_reussi':False,'contacts': contacts,'nbr':nbr,'form': form,'reponse':reponse,'afficherModal':afficherModal}
              return render(request,'contact/liste-contact.html',context)
        
     else: 
          contacts = Contact.objects.all()
          nbr = contacts.count()
          context = {'contacts': contacts,'nbr':nbr,'form': form}
     return render(request,'contact/liste-contact.html',context)
     
     


def liste_client_view(request):
     
     if request.method == 'POST':
        
          form = ContactForm(request.POST)
          if form.is_valid():
                form.save()  
                contacts_clients = Contact.objects.filter(categorie='Client')
                nbr =  Contact.objects.filter(categorie='Client').count()
                context = {'traitement_reussi': True,'contacts_clients': contacts_clients,'nbr':nbr,'form': form}
                return render(request,'contact/liste-contact.html',context)
          else:
             
             contacts_clients = Contact.objects.filter(categorie='Client')
             nbr =  Contact.objects.filter(categorie='Client').count()
             reponse="formulaire invalide"
             afficherModal=True
             context = {'afficherModal':afficherModal,'reponse':reponse,'traitement_reussi': False,'contacts_clients': contacts_clients,'nbr':nbr,'form': form}
             return render(request,'contact/liste-client.html',context) 
        
     else:

        form = ContactForm()
        contacts_clients = Contact.objects.filter(categorie='Client')
        nbr =  Contact.objects.filter(categorie='Client').count()
        context = {'contacts_clients': contacts_clients,'nbr':nbr,'form': form}
     
     return render(request,'contact/liste-client.html',context)   



def liste_prospect_view(request):
     if request.method == 'POST':
        

          form = ContactForm(request.POST)
          if form.is_valid():
                form.save()  
                contacts_prospects = Contact.objects.filter(categorie='Prospect')
                nbr = Contact.objects.filter(categorie='Prospect').count()
                context = {'traitement_reussi': True,'contacts_clients': contacts_prospects,'nbr':nbr,'form': form}
                return render(request,'contact/liste-prospect.html',context)
          else:
              
              contacts_prospects = Contact.objects.filter(categorie='Prospect')
              nbr = contacts_prospects.count()     
              reponse="formulaire invalide"
              afficherModal=True
              context = {'afficherModal':afficherModal,'reponse':reponse,'traitement_reussi': False,'contacts_prospects': contacts_prospects,'nbr':nbr,'form': form}
              return render(request,'contact/liste-prospect.html',context)
        
        
     else:
     
        form = ContactForm()
        contacts_prospects = Contact.objects.filter(categorie='Prospect')
        nbr = Contact.objects.filter(categorie='Prospect').count()
        context = {'contacts_prospects': contacts_prospects,'nbr':nbr,'form': form}
     
     return render(request,'contact/liste-prospect.html',context)

   
def liste_fournisseur_view(request):
     if request.method == 'POST':
        
       
          form = ContactForm(request.POST)
          if form.is_valid():
                form.save()  
                contacts_fournisseurs = Contact.objects.filter(categorie='Fournisseur')
                nbr = Contact.objects.filter(categorie='Fournisseur').count()
                context = {'traitement_reussi': True,'contacts_clients': contacts_fournisseurs,'nbr':nbr,'form': form}
                return render(request,'contact/liste-fournisseur.html',context)
          else:
             
             contacts_fournisseurs = Contact.objects.filter(categorie='Fournisseur')
             nbr = Contact.objects.filter(categorie='Fournisseur').count()
             reponse="formulaire invalide"
             afficherModal=True
             context = {'afficherModal':afficherModal,'reponse':reponse,'traitement_reussi': False,'contacts_fournisseurs': contacts_fournisseurs,'nbr':nbr,'form': form}
             return render(request,'contact/liste-fournisseur.html',context)
        
        
     else:


        form = ContactForm()
        contacts_fournisseurs = Contact.objects.filter(categorie='Fournisseur')
        nbr = Contact.objects.filter(categorie='Fournisseur').count()
        context = {'contacts_fournisseurs': contacts_fournisseurs,'nbr':nbr,'form': form}
     
     return render(request,'contact/liste-fournisseur.html',context)

   
def liste_societe_view(request):
     if request.method == 'POST':
       
          form = ContactForm(request.POST)
          if form.is_valid():
                form.save()  
                contacts_societes = Contact.objects.filter(type='Societe')
                nbr =  Contact.objects.filter(type='Societe').count()
                context = {'traitement_reussi': True,'contacts_societes': contacts_societes,'nbr':nbr,'form': form}
                return render(request,'contact/liste-societe.html',context)
          else:
            
             contacts_societes = Contact.objects.filter(type='Societe')
             nbr = contacts_societes.count()
             reponse="formulaire invalide"
             afficherModal=True
             context = {'afficherModal':afficherModal,'reponse':reponse,'traitement_reussi': False,'contacts_societes': contacts_societes,'nbr':nbr,'form': form}
             return render(request,'contact/liste-societe.html',context)
        
        
     else:
        form = ContactForm()
        contacts_societes = Contact.objects.filter(type='Societe')
        nbr =  Contact.objects.filter(type='Societe').count()
        context = {'contacts_societes': contacts_societes,'nbr':nbr,'form': form}
     
     return render(request,'contact/liste-societe.html',context)

   
def liste_particulier_view(request):
     if request.method == 'POST':
        
        
          form = ContactForm(request.POST)
          if form.is_valid():
                form.save()  
                contacts_particuliers = Contact.objects.filter(type='Particulier')
                nbr = Contact.objects.filter(type='Particulier').count()
                context = {'contacts_particuliers': contacts_particuliers,'nbr':nbr,'form': form}
                return render(request,'contact/liste-particulier.html',context)
          else:
               
                contacts_particuliers = Contact.objects.filter(type='Particulier')
                nbr = contacts_particuliers.count()
                reponse="formulaire invalide"
                afficherModal=True
                context = {'afficherModal':afficherModal,'reponse':reponse,'traitement_reussi': False,'contacts_particuliers': contacts_particuliers,'nbr':nbr,'form': form}
                return render(request,'contact/liste-particulier.html',context)
        
     else:

        form = ContactForm()
        contacts_particuliers = Contact.objects.filter(type='Particulier')
        nbr = Contact.objects.filter(type='Particulier').count()
        context = {'contacts_particuliers': contacts_particuliers,'nbr':nbr,'form': form}
     
     return render(request,'contact/liste-particulier.html',context)




def recuperer_contact_view(request, contact_id):
     
     calling_page = request.GET.get('calling_page', '/')
     print('page apellant recuperer :'+calling_page)
     contact = get_object_or_404(Contact, id=contact_id)
     context = {}
     
     if calling_page=="/contact/":
         form = ContactForm(instance=contact)
         print("page recuperer contact "+calling_page)
         contacts = Contact.objects.all()
         nbr = Contact.objects.count()
         afficherModalModification=True
         context = {'contact_modif':contact,'contacts': contacts,'nbr':nbr, 'form': form,'afficherModalModification':afficherModalModification,'calling_page':calling_page}
         return render(request, 'contact/liste-contact.html',context)
         
         
    
     elif calling_page == "/contact/clients/" :
          
          form = ContactForm(instance=contact)
          contacts_clients = Contact.objects.filter(categorie='Client')
          nbr = contacts_clients.count()
          afficherModalModification=True
          context = {'contact_modif':contact,'contacts_clients': contacts_clients,'nbr':nbr, 'form': form,'afficherModalModification':afficherModalModification,'calling_page':calling_page}
          return render(request, 'contact/liste-client.html',context)
    
     
     elif calling_page=="/contact/prospects/":
          
          form = ContactForm(instance=contact)
          contacts_prospects = Contact.objects.filter(categorie='Prospect')
          nbr = contacts_prospects.count()
          afficherModalModification=True
          context = {'contact_modif':contact,'contacts_prospects': contacts_prospects,'nbr':nbr, 'form': form,'afficherModalModification':afficherModalModification,'calling_page':calling_page}
          return render(request, 'contact/liste-prospect.html',context)
     
     elif calling_page=="/contact/fournisseurs/":
          form = ContactForm(instance=contact)
          contacts_fournisseurs = Contact.objects.filter(categorie='Fournisseur')
          nbr = contacts_fournisseurs.count()
          afficherModalModification=True
          context = {'contact_modif':contact,'contacts_fournisseurs': contacts_fournisseurs,'nbr':nbr, 'form': form,'afficherModalModification':afficherModalModification,'calling_page':calling_page}
          return render(request, 'contact/liste-fournisseur.html',context)
     
     elif calling_page=="/contact/particuliers/":
          form = ContactForm(instance=contact)
          contacts_particuliers = Contact.objects.filter(type='Particulier')
          nbr = contacts_particuliers.count()
          afficherModalModification=True
          context = {'contact_modif':contact,'contacts_particuliers': contacts_particuliers,'nbr':nbr, 'form': form,'afficherModalModification':afficherModalModification,'calling_page':calling_page}
          return render(request, 'contact/liste-particulier.html',context)
     
     elif calling_page=="/contact/societes/":
          form = ContactForm(instance=contact)
          contacts_societes = Contact.objects.filter(type='Societe')
          nbr = contacts_societes.count()
          afficherModalModification=True
          context = {'contact_modif':contact,'contacts_societes': contacts_societes,'nbr':nbr, 'form': form,'afficherModalModification':afficherModalModification,'calling_page':calling_page}
          return render(request, 'contact/liste-societe.html',context)
  
     return afficher_contact_view(request)

def modifier_contact_view(request):
    
    calling_page = request.GET.get('calling_page', '/')
    print(' page call modifier : '+calling_page)
    context = {}
    if request.method == 'POST':
        contact_id = request.POST.get('contact_id',None)
        identifiant=str(contact_id)
        contact = get_object_or_404(Contact, id=contact_id)
        form = ContactForm(request.POST, instance=contact)
        
        if form.is_valid():
             form.save()
             print(calling_page)
           
             if calling_page=="/contact/":
                  print("rediretion contact")
                  contacts = Contact.objects.all()
                  nbr = contacts.count()
                  context = {'modification_reussi': True,'contacts': contacts,'nbr':nbr,'form': form}
                  return render(request,'contact/liste-contact.html',context)
               
             elif calling_page=="/contact/clients/":
                  print("rediretion client")
                  contacts_clients = Contact.objects.filter(categorie='Client')
                  nbr = contacts_clients.count()
                  context = {'modification_reussi': True,'contacts_clients': contacts_clients,'nbr':nbr,'form': form}
                  return render(request,'contact/liste-client.html',context)
               
             elif calling_page=="/contact/prospects/":
                  contacts_prospects = Contact.objects.filter(categorie='Prospect')
                  nbr = contacts_prospects.count()
                  context = {'modification_reussi': True,'contacts_prospects': contacts_prospects,'nbr':nbr,'form': form}
                  return render(request,'contact/liste-prospect.html',context)
               
               
             elif calling_page=="/contact/fournisseurs/":
                  contacts_fournisseurs = Contact.objects.filter(categorie='Fournisseur')
                  nbr = contacts_fournisseurs.count()
                  context = {'modification_reussi': True,'contacts_fournisseurs': contacts_fournisseurs,'nbr':nbr,'form': form}
                  return render(request,'contact/liste-fournisseur.html',context)
               
               
             elif calling_page=="/contact/societes/":
                  contacts_societes = Contact.objects.filter(type='Societe')
                  nbr = contacts_societes.count()
                  context = {'modification_reussi': True,'contacts_societes': contacts_societes,'nbr':nbr,'form': form}
                  return render(request,'contact/liste-societe.html',context)
                 
             elif calling_page=="/contact/particuliers/":
                  contacts_particuliers = Contact.objects.filter(type='Particulier')
                  nbr = contacts_particuliers.count()
                  context = {'modification_reussi': True,'contacts_particuliers': contacts_particuliers,'nbr':nbr,'form': form}
                  return render(request,'contact/liste-particulier.html',context)
               
        else:
             form = ContactForm(instance=contact)
             if calling_page=="/contact/":
                contacts = Contact.objects.all()
                nbr = contacts.count()
                reponse="formulaire invalide"
                afficherModalModification=True
                context = {'contact_modif':contact,'contacts': contacts,'nbr':nbr, 'form': form,'afficherModalModification':afficherModalModification,'reponse':reponse}
                return render(request, 'contact/liste-contact.html',context)
 
             elif calling_page=="/contact/clients/":
                  contacts_clients = Contact.objects.filter(categorie='Client')
                  nbr = contacts_clients.count()
                  reponse="formulaire invalide"
                  afficherModalModification=True
                  context = {'contact_modif':contact,'contacts_clients': contacts_clients,'nbr':nbr, 'form': form,'afficherModalModification':afficherModalModification,'reponse':reponse}
                  return render(request, 'contact/liste-client.html',context)
 
             elif calling_page==f"/contact/prospects/":
                  contacts_prospects = Contact.objects.filter(categorie='Prospect')
                  nbr = contacts_prospects.count()
                  reponse="formulaire invalide"
                  afficherModalModification=True
                  context = {'contact_modif':contact,'contacts_prospects': contacts_prospects,'nbr':nbr, 'form': form,'afficherModalModification':afficherModalModification,'reponse':reponse}
                  return render(request, 'contact/liste-prospect.html',context)
 
             elif calling_page==f"/contact/fournisseurs/":
                  contacts_fournisseurs = Contact.objects.filter(categorie='Fournisseur')
                  nbr = contacts_fournisseurs.count()
                  reponse="formulaire invalide"
                  afficherModalModification=True
                  context = {'contact_modif':contact,'contacts_fournisseurs': contacts_fournisseurs,'nbr':nbr, 'form': form,'afficherModalModification':afficherModalModification,'reponse':reponse}
                  return render(request, 'contact/liste-fournisseur.html',context)
             
             elif calling_page==f"/contact/societes/":
                  contacts_societes = Contact.objects.filter(type='Societe')
                  nbr = contacts_societes.count()
                  reponse="formulaire invalide"
                  afficherModalModification=True
                  context = {'contact_modif':contact,'contacts_societes': contacts_societes,'nbr':nbr, 'form': form,'afficherModalModification':afficherModalModification,'reponse':reponse}
                  return render(request, 'contact/liste-societe.html',context)
            
             elif calling_page==f"/contact/particuliers/":
                  contacts_particuliers = Contact.objects.filter(type='Societe')
                  nbr = contacts_particuliers.count()
                  reponse="formulaire invalide"
                  afficherModalModification=True
                  context = {'contact_modif':contact,'contacts_particuliers': contacts_particuliers,'nbr':nbr, 'form': form,'afficherModalModification':afficherModalModification,'reponse':reponse}
                  return render(request, 'contact/liste-particulier.html',context)
 

    else:
       
        form = ContactForm()
        contacts = Contact.objects.all()
        nbr = contacts.count()
        afficherModalModification=True
        context = {'contact_modif':contact,'contacts': contacts,'nbr':nbr, 'form': form,}
    return render(request, 'contact/liste-contact.html',context)


def supprimer_contact_view(request,contact_id):
   
      calling_page = request.GET.get('calling_page', '/')
      print(calling_page)
      context = {}
      contact = get_object_or_404(Contact, id=contact_id)
      contact.delete()
      form = ContactForm(request.POST)
      if calling_page=="/contact/":
               contacts = Contact.objects.all()
               nbr = contacts.count()
               context = {'suppression_reussi': True,'contacts': contacts,'nbr':nbr,'form': form}
               return render(request,'contact/liste-contact.html',context)
               
      elif calling_page=="/contact/clients/":
               contacts_clients = Contact.objects.filter(categorie='Client')
               nbr = contacts_clients.count()
               context = {'suppression_reussi': True,'contacts_clients': contacts_clients,'nbr':nbr,'form': form}
               return render(request,'contact/liste-client.html',context)
               
      elif calling_page=="/contact/prospects/":
               contacts_prospects = Contact.objects.filter(categorie='Prospect')
               nbr = contacts_prospects.count()
               context = {'suppression_reussi': True,'contacts_prospects': contacts_prospects,'nbr':nbr,'form': form}
               return render(request,'contact/liste-prospect.html',context)
               
               
      elif calling_page=="/contact/fournisseurs/":
               contacts_fournisseurs = Contact.objects.filter(categorie='Fournisseur')
               nbr = contacts_fournisseurs.count()
               context = {'suppression_reussi': True,'contacts_fournisseurs': contacts_fournisseurs,'nbr':nbr,'form': form}
               return render(request,'contact/liste-fournisseur.html',context)
              
               
      elif calling_page=="/contact/societes/":
               contacts_societes = Contact.objects.filter(type='Societe')
               nbr = contacts_societes.count()
               context = {'suppression_reussi': True,'contacts_societes': contacts_societes,'nbr':nbr,'form': form}
               return render(request,'contact/liste-societe.html',context)
                 
      elif calling_page=="/contact/particuliers/":
               contacts_particuliers = Contact.objects.filter(type='Particulier')
               nbr = contacts_particuliers.count()
               context = {'suppression_reussi': True,'contacts_particuliers': contacts_particuliers,'nbr':nbr,'form': form}
               return render(request,'contact/liste-particulier.html',context)
               
       
      return redirect('contact:afficher-contact')


# def supprimer_contact_view(request):
#     contact_id = request.POST.get("contact_id")
#     Contact.objects.filter(pk=contact_id).delete()
#     return redirect('liste_contact')
 
 
 # implementation de la recherche de contact
class RechercheContactView(View):
    template_name = 'contact/recherche_contact.html'

    def get(self, request):
        term_recherche = request.GET.get('term_recherche', '')

        # Filtrer les contacts en fonction du terme de recherche
        #contacts = Contact.objects.filter(name__icontains=term_recherche)
        contacts = Contact.objects.filter(models.Q(name__icontains=term_recherche) | models.Q(email__icontains=term_recherche))
        nombre = contacts.count()
        context = {'nombre':nombre,'contacts': contacts, 'term_recherche': term_recherche}
        
        # Si la requête est une requête AJAX, renvoyer le fragment HTML
     #    if request.is_ajax():
     #        return render(request, 'contact/resultats_recherche.html', context)
         
        if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return render(request, 'contact/resultats_recherche.html', context)


        return render(request, self.template_name, context)
   
    # implementation de la recherche de client
class RechercheClientView(View):
    template_name = 'contact/recherche_client.html'

    def get(self, request):
        term_recherche = request.GET.get('term_recherche', '')

        # Filtrer les contacts en fonction du terme de recherche
        #contacts = Contact.objects.filter(name__icontains=term_recherche)
        contacts_clients = Contact.objects.filter(models.Q(name__icontains=term_recherche) | models.Q(email__icontains=term_recherche),categorie='Client')
        nombre = contacts_clients.count()
        context = {'nombre':nombre,'contacts_clients': contacts_clients, 'term_recherche': term_recherche}
        
        # Si la requête est une requête AJAX, renvoyer le fragment HTML
        #    if request.is_ajax():
        #        return render(request, 'contact/resultats_recherche.html', context)
         
        if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return render(request, 'contact/resultats_recherche.html', context)


        return render(request, self.template_name, context)
   
   
class RechercheProspectView(View):
    template_name = 'contact/recherche_prospect.html'

    def get(self, request):
        term_recherche = request.GET.get('term_recherche', '')

        # Filtrer les contacts en fonction du terme de recherche
        #contacts = Contact.objects.filter(name__icontains=term_recherche)
        contacts_prospects = Contact.objects.filter(models.Q(name__icontains=term_recherche) | models.Q(email__icontains=term_recherche),categorie='Prospect')
        nombre = contacts_prospects.count()
        context = {'nombre':nombre,'contacts_prospects': contacts_prospects, 'term_recherche': term_recherche}
        
        # Si la requête est une requête AJAX, renvoyer le fragment HTML
        #    if request.is_ajax():
        #        return render(request, 'contact/resultats_recherche.html', context)
         
        if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return render(request, 'contact/resultats_recherche.html', context)


        return render(request, self.template_name, context)
   
class RechercheFournisseurView(View):
    template_name = 'contact/recherche_fournisseur.html'

    def get(self, request):
        term_recherche = request.GET.get('term_recherche', '')

        # Filtrer les contacts en fonction du terme de recherche
        #contacts = Contact.objects.filter(name__icontains=term_recherche)
        contacts_fournisseurs = Contact.objects.filter(models.Q(name__icontains=term_recherche) | models.Q(email__icontains=term_recherche),categorie='Fournisseur')
        nombre = contacts_fournisseurs.count()
        context = {'nombre':nombre,'contacts_fournisseurs': contacts_fournisseurs, 'term_recherche': term_recherche}
        
        # Si la requête est une requête AJAX, renvoyer le fragment HTML
        #    if request.is_ajax():
        #        return render(request, 'contact/resultats_recherche.html', context)
         
        if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return render(request, 'contact/resultats_recherche.html', context)


        return render(request, self.template_name, context)
   
   
class RechercheSocieteView(View):
    template_name = 'contact/recherche_societe.html'

    def get(self, request):
        term_recherche = request.GET.get('term_recherche', '')

        # Filtrer les contacts en fonction du terme de recherche
        #contacts = Contact.objects.filter(name__icontains=term_recherche)
        contacts_societes = Contact.objects.filter(models.Q(name__icontains=term_recherche) | models.Q(email__icontains=term_recherche),type='Societe')
        nombre = contacts_societes.count()
        context = {'nombre':nombre,'contacts_societes': contacts_societes, 'term_recherche': term_recherche}
        
        # Si la requête est une requête AJAX, renvoyer le fragment HTML
        #    if request.is_ajax():
        #        return render(request, 'contact/resultats_recherche.html', context)
         
        if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return render(request, 'contact/resultats_recherche.html', context)


        return render(request, self.template_name, context)
   
class RechercheParticulierView(View):
    template_name = 'contact/recherche_particulier.html'

    def get(self, request):
        term_recherche = request.GET.get('term_recherche', '')

        # Filtrer les contacts en fonction du terme de recherche
        #contacts = Contact.objects.filter(name__icontains=term_recherche)
        contacts_particuliers = Contact.objects.filter(models.Q(name__icontains=term_recherche) | models.Q(email__icontains=term_recherche),type='Particulier')
        nombre = contacts_particuliers.count()
        context = {'nombre':nombre,'contacts_particuliers': contacts_particuliers, 'term_recherche': term_recherche}
        
        # Si la requête est une requête AJAX, renvoyer le fragment HTML
        #    if request.is_ajax():
        #        return render(request, 'contact/resultats_recherche.html', context)
         
        if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return render(request, 'contact/resultats_recherche.html', context)


        return render(request, self.template_name, context)