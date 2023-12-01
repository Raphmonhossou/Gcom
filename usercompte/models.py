from django.db import models
from django.contrib.auth.models import AbstractUser

class Utilisateur(AbstractUser):
      is_active = models.BooleanField(default=False)
      email_verification_token = models.CharField(max_length=255, blank=True, null=True)
      #Champ ManyToMany vers le modèle Group
      groups = models.ManyToManyField('auth.Group',related_name="utilisateurs",  ) # Spécifiez le related_name ici

    #   Champ ManyToMany vers le modèle Permission
      user_permissions = models.ManyToManyField('auth.Permission',related_name= "utilisateurs", )# Spécifiez le related_name ici

      def __str__(self):
         return self.username
 
