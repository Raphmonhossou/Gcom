from usercompte.views import inscription_succes,inscription_refuse, login_user,logout_user, signup, verify
from django.urls import include, path

app_name = 'usercompte'
urlpatterns = [
    #usercompte
    path('', login_user,name="connexion"),
    path('deconnexion/', logout_user,name="deconnexion"),
    path('inscription/', signup,name="inscription"),
    path('verify/<token>',verify, name='verify'),
    path('inscriptionvalide/', inscription_succes, name='inscription-succes'),
    path('inscriptioninvalide/',inscription_refuse, name='inscription-refuse'),

 
]