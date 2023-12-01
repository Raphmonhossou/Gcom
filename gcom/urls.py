from django.urls import include, path
from gcom.views import index,fonctionalite_view,temoignage_view,apropos_view

app_name='gcom'
urlpatterns = [
    path('',index,name='index'),
    path('fonctionalite/',fonctionalite_view,name="fonctionalite"),
    path('temoignages/',temoignage_view,name="temoignage"),
    path('Apropos/',apropos_view,name="apropos"),
    
]