from django.contrib import admin
from contact.models import Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone","ifu","categorie","type","adress")
admin.site.register(Contact,ContactAdmin)

