from django.urls import include, path
from paramettre.views import paramettre, famille_produit,unite_mesure,groupe_taxe

app_name='paramettre'
urlpatterns = [
   
  #paramettre
    path('',paramettre, name='parametre'),
    path('famille-de-produit/',famille_produit, name='famille-de-produit'),
    path('unite-de-mesure/',unite_mesure, name='unite-de-mesure'),
    path('groupe-de-taxe/',groupe_taxe, name='groupe-de-taxe'),
]