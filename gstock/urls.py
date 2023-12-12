from django.urls import include, path
from gstock.views import CommandeClientCreate,CreerCommande, ListeCommande, ListeCommandeClient, ModifierCommande, RechercheArticleView, RechercheCommandeClientView, RechercheCommandeFournisseurView, UpdateCommandeClient, ajouter_article, delete_commande, delete_commande_client, delete_produit, delete_produit_client, liste_article_view, modifier_article_view, recuperer_article_view, recuperer_prix_article,stock_view,commande_client_view, supprimer_article_view

app_name='stock'
urlpatterns = [
   # stock
    path('stock/',stock_view, name='stock'),
    path('article/',liste_article_view, name='liste-article'),
    path('ajouter/',ajouter_article, name='ajouter-article'),
    path('recuperer-article/<int:article_id>/',recuperer_article_view, name='recuperer-article'),
    path('modification-article/',modifier_article_view, name='modifier-article'),
    path('suppresion-article/<int:article_id>/',supprimer_article_view, name='supprimer-article'),
    path('recherche-article/',RechercheArticleView.as_view(), name='recherche_article'),
    path('prix-article/',recuperer_prix_article, name='recuperer-prix-article'),

    # commande fournisseur
    #path('recuperer-commande_fournisseur/<int:commande_fournisseur_id>/',recuperer_commande_fournisseur_view, name='recuperer-commande-fournisseur'),
   # path('modification-commande-fournisseur/',modifier_commande_fournisseur_view, name='modifier-commande-fournisseur'),
    #path('suppresion-commande-fournisseur/<int:commande_fournisseur_id>/',supprimer_commande_fournisseur_view, name='supprimer-commande-fournisseur'),
    #path('commande/',commande_fournisseur_view, name='commande'),
    #path('Nouvelle-commande/',nouvelle_commande_fournisseur_view, name='nouvelle-commande-fournisseur'),
   
    path('commande-fournisseur', ListeCommande.as_view(), name='liste_commande_fournisseur'), 
    path('nouvelle-commande/', CreerCommande.as_view(), name='create_commande'),
    path('modifier-commande/<int:pk>/', ModifierCommande.as_view(), name='modifier_commande'),
    path('delete-produit/<int:pk>/', delete_produit, name='delete_produit'),
    path('delete-commande/<int:pk>/', delete_commande, name='delete-commande-fournisseur'),
    path('liste-commande-fournisseur/',RechercheCommandeFournisseurView.as_view(), name='recherche_commande_fournisseur'),

    
    # commande client
    #path('vente/',commande_client_view, name='vente'),
    path('commande-client', ListeCommandeClient.as_view(), name='liste_commande_client'), 
    path('nouvelle-commande-client/', CommandeClientCreate.as_view(), name='create_commande_client'),
    path('update-commande-client/<int:pk>/', UpdateCommandeClient.as_view(), name='update_commande_client'),
    path('delete-produit-client/<int:pk>/', delete_produit_client, name='delete_produit_client'),
    path('delete-commande-client/<int:pk>/', delete_commande_client, name='delete-commande-client'),
    path('liste-commande-client/',RechercheCommandeClientView.as_view(), name='recherche_commande_client'),
]