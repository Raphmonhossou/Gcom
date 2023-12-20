from django.urls import include, path
from gstock.views import ListeCommande, ListeCommandeClient, RechercheArticleView, RechercheCommandeClientView, RechercheCommandeFournisseurView, ajouter_article, delete_commande, delete_commande_vente, delete_produit, delete_produit_vente, delete_produit_vente, detail_commande_client_view, detail_commande_fournisseur_view, liste_article_view, modifier_article_view, modifier_commande_client_view, nouvelle_commande_client_view, nouvelle_commande_fournisseur_view, recuperer_article_view, recuperer_commande_client_view, recuperer_prix_article,stock_view,modifier_commande_fournisseur_view,recuperer_commande_fournisseur_view, supprimer_article_view

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
    path('recuperer-commande_fournisseur/<int:commande_fournisseur_id>/',recuperer_commande_fournisseur_view, name='recuperer-commande-fournisseur'),
    path('modification-commande-fournisseur/',modifier_commande_fournisseur_view, name='modifier-commande-fournisseur'),
    path('detail-commande-fournisseur/<int:commande_fournisseur_id>/',detail_commande_fournisseur_view, name='detail-commande-fournisseur'),
    path('Nouvelle-commande-fournisseur/',nouvelle_commande_fournisseur_view, name='nouvelle-commande-fournisseur'),
    path('commande-fournisseur', ListeCommande.as_view(), name='liste_commande_fournisseur'), 
    path('delete-produit/<int:pk>/', delete_produit, name='delete_produit'),
    path('delete-commande/<int:pk>/', delete_commande, name='delete-commande-fournisseur'),
    path('liste-commande-fournisseur/',RechercheCommandeFournisseurView.as_view(), name='recherche_commande_fournisseur'),

    
    # commande client
    path('recuperer-commande_client/<int:commande_client_id>/',recuperer_commande_client_view, name='recuperer-commande-client'),
    path('modification-commande-client/',modifier_commande_client_view, name='modifier-commande-client'),
    path('detail-commande-client/<int:commande_client_id>/',detail_commande_client_view, name='detail-commande-client'),
    path('Nouvelle-commande-client/',nouvelle_commande_client_view, name='nouvelle-commande-client'),
    path('commande-client', ListeCommandeClient.as_view(), name='liste-commande-client'), 
    path('delete-produit-select/<int:pk>/', delete_produit_vente, name='delete-produit-vente'),
    path('delete-commande-select/<int:pk>/', delete_commande_vente, name='delete-commande-client'),
    path('liste-commande-client/',RechercheCommandeClientView.as_view(), name='recherche_commande_client'),

]