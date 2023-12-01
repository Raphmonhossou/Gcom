from django.urls import include, path
from gestionnaire.views import dashbord_view

app_name='gestionnaire'

urlpatterns = [
   
    # gestionnaire
    path('',dashbord_view, name='dashbord'),
]