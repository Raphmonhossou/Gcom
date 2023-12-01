from django.urls import include, path
from contact.views import RechercheClientView, RechercheContactView, RechercheFournisseurView, RechercheParticulierView, RechercheProspectView, RechercheSocieteView, afficher_contact_view, ajouter_contact_view,liste_client_view,liste_fournisseur_view,liste_particulier_view,liste_prospect_view,liste_societe_view,modifier_contact_view, recuperer_contact_view,supprimer_contact_view

app_name = 'contact'
urlpatterns = [
   
 #contact
    path('',afficher_contact_view, name='afficher-contact'),
    path('ajouter-contact',ajouter_contact_view, name='ajouter-contact'),
    path('clients/',liste_client_view, name='liste-client'),
    path('prospects/',liste_prospect_view, name='liste-prospect'),
    path('fournisseurs/',liste_fournisseur_view, name='liste-fournisseur'),
    path('societes/',liste_societe_view, name='liste-societe'),
    path('particuliers/',liste_particulier_view, name='liste-particulier'),
    path('recuperer-contact/<int:contact_id>/',recuperer_contact_view, name='recuperer-contact'),
    path('modification/',modifier_contact_view, name='modifier-contact'),
    path('suppresion/<int:contact_id>/',supprimer_contact_view, name='supprimer-contact'),
    path('recherche-contact/',RechercheContactView.as_view(), name='recherche_contact'),
    path('recherche-client/',RechercheClientView.as_view(), name='recherche_client'),
    path('recherche-prospect/',RechercheProspectView.as_view(), name='recherche_prospect'),
    path('recherche-fournisseur/',RechercheFournisseurView.as_view(), name='recherche_fournisseur'),
    path('recherche-societe/',RechercheSocieteView.as_view(), name='recherche_societe'),
    path('recherche-particulier/',RechercheParticulierView.as_view(), name='recherche_particulier'),
    
]