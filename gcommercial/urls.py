
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gcom.urls', namespace='gcom')),
    path('connexion/', include('usercompte.urls', namespace='usercompte')),
    path('dashbord/', include('gestionnaire.urls', namespace='gestionnaire')),
    path('contact/', include('contact.urls', namespace='contact')),
    path('gstock/', include('gstock.urls', namespace='gstock')),
    path('parametre/', include('paramettre.urls', namespace='paramettre')),
]


# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('',index,name="index"),
#     path('fonctionalite/',fonctionalite_view,name="fonctionalite"),
#     path('temoignages/',temoignage_view,name="temoignage"),
#     path('Apropos/',apropos_view,name="apropos"),
          
#     #usercompte
#     path('connexion/', login_user,name="connexion"),
#     path('deconnexion/', logout_user,name="deconnexion"),
#     path('inscription/', signup,name="inscription"),
#     path('verify/<token>',verify, name='verify'),
#     path('inscriptionvalide/', inscription_succes, name='inscription-succes'),
#     path('inscriptioninvalide/',inscription_refuse, name='inscription-refuse'),

#     # gestionnaire
#     path('dashbord/',dashbord_view, name='dashbord'),

#     #contact
#     path('contact/',gestionnaire_contact_view, name='gestionnaire-contact'),
#     path('clients/',liste_client_view, name='liste-client'),
#     path('prospects/',liste_prospect_view, name='liste-prospect'),
#     path('fournisseurs/',liste_fournisseur_view, name='liste-fournisseur'),
#     path('societes/',liste_societe_view, name='liste-societe'),
#     path('particuliers/',liste_particulier_view, name='liste-particulier'),
#     path('recuperer-contact/<int:contact_id>/',recuperer_contact_view, name='recuperer-contact'),
#     path('modification/',modifier_contact_view, name='modifier-contact'),
#     path('suppresion/<int:contact_id>/',supprimer_contact_view, name='supprimer-contact'),
#     path('recherche-contact/',RechercheContactView.as_view(), name='recherche_contact'),
#     path('recherche-client/',RechercheClientView.as_view(), name='recherche_client'),
#     path('recherche-prospect/',RechercheProspectView.as_view(), name='recherche_prospect'),
#     path('recherche-fournisseur/',RechercheFournisseurView.as_view(), name='recherche_fournisseur'),
#     path('recherche-societe/',RechercheSocieteView.as_view(), name='recherche_societe'),
#     path('recherche-particulier/',RechercheParticulierView.as_view(), name='recherche_particulier'),
    
#     # stock
#     path('article/',liste_article_view, name='liste-article'),
#     path('ajouter/',ajouter_article, name='ajouter-article'),
#     path('stock/',stock_view, name='stock'),
#     path('commande/',commande_fournisseur_view, name='commande'),
#     path('vente/',commande_client_view, name='vente'),
#     path('recuperer-article/<int:article_id>/',recuperer_article_view, name='recuperer-article'),
#     path('modification-article/',modifier_article_view, name='modifier-article'),
#     path('suppresion-article/<int:article_id>/',supprimer_article_view, name='supprimer-article'),
#     path('recherche-article/',RechercheArticleView.as_view(), name='recherche_article'),


#    #paramettre
#     path('parametre/',paramettre, name='parametre'),
#     path('famille-de-produit/',famille_produit, name='famille-de-produit'),
#     path('unite-de-mesure/',unite_mesure, name='unite-de-mesure'),
#     path('groupe-de-taxe/',groupe_taxe, name='groupe-de-taxe'),
# ]