from django.db import models



class Contact(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField(max_length=128)
    phone = models.CharField(max_length=15)
    ifu = models.IntegerField()
    categorie = models.CharField(max_length=20, choices=[('Client', 'Client'), ('Prospect', 'Prospect'), ('Fournisseur', 'Fournisseur')], verbose_name='Catégorie')
    type = models.CharField(max_length=20, choices=[('Societe', 'Société'), ('Particulier', 'Particulier')], verbose_name='Type')
    adress = models.CharField(max_length=300)
    
    def __str__(self):
        return self.name
    
    