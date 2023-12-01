from django.contrib import admin
from gstock.models import CommandeFournisseur, FamilleProduit, GroupeTaxe, LigneCommande, Produit, UniteMesure


class ProduitAdmin(admin.ModelAdmin):
     list_display = ("libele","code", "description","famille","image")

class FamilleProduitAdmin(admin.ModelAdmin):
     list_display = ("libele","description")

class GroupeTaxeAdmin(admin.ModelAdmin):
     list_display = ("libele","taux","description","code_fiscal","exoneration","statut")

class UniteMesureAdmin(admin.ModelAdmin):
     list_display = ("libele","description")

class CommandeFournisseurAdmin(admin.ModelAdmin):
     list_display = ("date_commande","fournisseur","reference","statut","date_reception")
class LigneCommandeAdmin(admin.ModelAdmin):
     list_display = ("commande","produit","quantite","prix_unitaire","montant")



admin.site.register(Produit,ProduitAdmin)
admin.site.register(FamilleProduit,FamilleProduitAdmin)
admin.site.register(GroupeTaxe,GroupeTaxeAdmin)
admin.site.register(UniteMesure,UniteMesureAdmin)
admin.site.register(CommandeFournisseur,CommandeFournisseurAdmin)
admin.site.register(LigneCommande,LigneCommandeAdmin)