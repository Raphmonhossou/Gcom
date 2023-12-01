# sur la page d'accueil

- temoignage

- video de presentation
- presentation de l'application
- image du tableau de bord



- Mot de pass administrateur user: admin , pass: 999999999
Mot de pass monhossouraphael: 88888888

-----------------------------------
# gestionnaire app model
model:


- Contact(nom, status,  type, email, phone,adresse,ifu)
---------------------------
- Produit()
libele
code 
description 
prix
quantite 
categorie
cout_achat
fournisseur :
niveau_alete_stock
unite_mesure
groupe_taxe 
date_ajout 
date_peremption
image

# gestion de stock

-module : entrée , sortie, inventaire

# achat 
-code produit , libelé, prix d'achat,fournisseur quantite,remise,tva, montantTTC,date
# commande fournisseur
-fournisseur, produit, date_commande, date_reception_prevu,reference,mode de paiement,condition de paiement
# reception pour enregistrer 
commande,date_reception_reel

# facture

# vente 
-code produit , libelé, client,prix de vente, quantite,remise,tva, montantTTC,date

Devis
commande client
livraison
facture

# recouvrement

facture fournisseur et client; paiement fournisseur et client; etat client , etat fournisseur