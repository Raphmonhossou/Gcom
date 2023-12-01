from django.contrib import admin

from usercompte.models import Utilisateur

# # Register your models here.

class UtilisateurAdmin(admin.ModelAdmin):
     list_display = ("username", "email", "password","is_active")

#admin.site.register(Utilisateur,UtilisateurAdmin)