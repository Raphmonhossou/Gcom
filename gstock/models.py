from django.db import models
from contact.models import Contact




# famile de produit
class FamilleProduit(models.Model):
    libele = models.CharField(max_length=100, verbose_name='Libéllé de la famille de Produit')
    description = models.TextField(blank=True, null=True, verbose_name='Description')
    
    def __str__(self):
        return self.libele

    class Meta:
        verbose_name_plural = 'Familles de Produit'



class GroupeTaxe(models.Model):
    libele = models.CharField(max_length=100, verbose_name='Libéllé du Groupe de Taxe')
    taux = models.DecimalField(max_digits=5, decimal_places=2,default=0.00, verbose_name='Taux de Taxe')
    description = models.TextField(blank=True, null=True, verbose_name='Description')
    code_fiscal = models.CharField(max_length=20, blank=True, null=True, verbose_name='Code Fiscal')
    exoneration = models.BooleanField(default=False, verbose_name='Exonéré')
    statut = models.CharField(max_length=20, choices=[('actif', 'Actif'), ('inactif', 'Inactif'), ('attente', 'En attente')],default='actif', verbose_name='Statut')

    def __str__(self):
        return self.libele

    class Meta:
        verbose_name_plural = 'Groupes de Taxes'

class UniteMesure(models.Model):
    libele = models.CharField(max_length=100, verbose_name='Libéllé de l\'unité de mesure')
    description = models.TextField(blank=True, null=True, verbose_name='Description')

    class Meta:
        verbose_name_plural = 'Unites de Mesure'


    def __str__(self):
        return self.libele


class Produit(models.Model):
    libele = models.CharField(max_length=255, verbose_name='Libellé')
    code = models.CharField(max_length=50, unique=True, verbose_name='Code')
    description = models.TextField(blank=True, null=True,verbose_name='Description')
    prix = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Prix')
    quantite = models.PositiveIntegerField(verbose_name='Quantité en Stock')
    famille = models.ForeignKey(FamilleProduit, on_delete=models.CASCADE, verbose_name='Famille')
    cout_achat = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Coût d\'Achat')
    fournisseur = models.ForeignKey(Contact, on_delete=models.CASCADE, verbose_name='Fournisseur',limit_choices_to={'categorie': 'Fournisseur'})
    niveau_alerte_stock = models.PositiveIntegerField(verbose_name='Niveau d\'Alerte de Stock')
    unite_mesure = models.ForeignKey(UniteMesure, on_delete=models.CASCADE, verbose_name='Unité de Mesure')
    groupe_taxe = models.ForeignKey(GroupeTaxe, on_delete=models.CASCADE, verbose_name='Groupe de Taxes')
    #date_creation = models.DateField(auto_now_add=True, verbose_name='Date de Création')
    date_peremption = models.DateField(null=True, blank=True, verbose_name='Date de Péremption')
    image = models.ImageField(upload_to='gestionnaire/imgs/', null=True, blank=True, verbose_name='Image du Produit')
   
    def __str__(self):
        return self.libele

    class Meta:
        verbose_name_plural = 'Produits'




class CommandeFournisseur(models.Model):
    
    STATUT_CHOICES = [
        
        ('en_cours', 'En Cours'),
        ('recue', 'Reçue'),
        ('annulee', 'Annulée'),
    ]

    fournisseur = models.ForeignKey(Contact, on_delete=models.CASCADE, verbose_name='Fournisseur',limit_choices_to={'categorie': 'Fournisseur'})
    date_commande = models.DateField(verbose_name='Date de Commande')
    produits = models.ManyToManyField('Produit', through='LigneCommande', verbose_name='Produits')
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='En cours', verbose_name='Statut de la Commande')
    reference = models.CharField(max_length=100, verbose_name='Reference')
    date_reception = models.DateField(null=True, blank=True, verbose_name='Date de Réception')

    def __str__(self):
        return f"Commande #{self.id} - Fournisseur: {self.fournisseur.name}"

    class Meta:
        verbose_name_plural = 'Commandes Fournisseurs'

class LigneCommande(models.Model):
    commande = models.ForeignKey(CommandeFournisseur, on_delete=models.CASCADE, verbose_name='Commande Fournisseur')
    produit = models.ForeignKey('Produit', on_delete=models.CASCADE, verbose_name='Produit')
    quantite = models.PositiveIntegerField(verbose_name='Quantité')
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Prix Unitaire')
    montant = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Montant TTC')

    def __str__(self):
        return f"{self.commande} - {self.produit.libele} ({self.quantite} )"

    class Meta:
        verbose_name_plural = 'Lignes de Commande'




class CommandeClient(models.Model):
    
    STATUT_CHOICES = [
        
        ('en_cours', 'En cours'),
        ('livree', 'Livré'),
        ('annulee', 'Annulée'),
    ]

    client = models.ForeignKey(Contact, on_delete=models.CASCADE, verbose_name='Client',limit_choices_to={'categorie': 'Client'})
    date_commande = models.DateField(verbose_name='Date de Commande')
    produits = models.ManyToManyField('Produit', through='LigneCommandeClient', verbose_name='Produits')
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='En cours', verbose_name='Statut de la Commande')
    reference = models.CharField(max_length=100, verbose_name='Reference')
    date_livraison = models.DateField(null=True, blank=True, verbose_name='Date de Réception')

    def __str__(self):
        return f"Commande #{self.id} - Client: {self.client.name}"

    class Meta:
        verbose_name_plural = 'Commandes Clients'

class LigneCommandeClient(models.Model):
    commande_client = models.ForeignKey(CommandeClient, on_delete=models.CASCADE, verbose_name='Commande Client')
    produit = models.ForeignKey('Produit', on_delete=models.CASCADE, verbose_name='Produit')
    quantite = models.PositiveIntegerField(verbose_name='Quantité')
    prix_vente = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Prix de vente')
    montant = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Montant TTC')

    def __str__(self):
        return f"{self.commande_client} - {self.produit.libele} ({self.quantite})"

    class Meta:
        verbose_name_plural = 'Lignes de commande client'

