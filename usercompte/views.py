import datetime
from email import message
import hashlib
from urllib.parse import urlparse
from urllib.parse import urlencode, urljoin

from django import forms
from gcommercial import settings
from django.shortcuts import render ,redirect
from django.contrib.auth import get_user_model, login,logout,authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render,redirect
#from usercompte.form import InscriptionForm
from django.core.mail import send_mail
from django.urls import reverse, reverse_lazy
from usercompte.models import Utilisateur
from django.contrib.auth.models import User

#from django.contrib.auth.models import UserManager


#Utilisateur = get_user_model()


def signup(request):
     if request.method == "POST":
            print("niveau 2")
            username = request.POST["username"]
            email = request.POST["email"]
            password1 = request.POST["password1"]
            password2 = request.POST["password2"]
            
            if password1:
                if password1 != password2:
                    context = {'message': "les mots de passe ne correspondent pas"}
                    return render(request,'usercompte/signup.html',context)
                else:
                    utilisateur = User.objects.create_user(username=username,email=email,password=password1)
                    utilisateur.save()
                return redirect('inscription-succes')
            else:
                context = {'message': "choissisez un mot de passe"}
                return render(request,'usercompte/signup.html',context)
     return render(request,'usercompte/signup.html')


"""
def signup(request):
     if request.method == "POST":
         form = InscriptionForm(request.POST)
       
         if form.is_valid():
            print("niveau 2")
            username = request.POST["username"]
            #username = form.cleaned_data['username']
            email = request.POST["email"]
            #email = form.cleaned_data['email']
            #password = clean_password2(request.POST["password1"],request.POST["password2"])
            password = request.POST.get(form.clean_password2)
           
            print(f"niveau 3")
            utilisateur = User.objects.create_user(username=username,email=email,password=password)
            utilisateur.is_active = False
            utilisateur.save()
            token = generate_email_verification_token(utilisateur)
            utilisateur.email_verification_token = token
           
            print(f"niveau 4 {utilisateur}")
            print(f"niveau 5 {token}")
            send_email(request,token, email)
            print("niveau 6 apres send mail")
            context = {'message': "un email vous est envoyé"}
            return render(request,'usercompte/signup.html',context)
        
         else:
                context = {'message': "une erreur est survenu"}
                return render(request,'usercompte/signup.html',context)
     return render(request,'usercompte/signup.html')
 """

# def signup(request):
#      if request.method == "POST":
#          form = InscriptionForm(request.POST)
#          print("niveau 1")
#          if form.is_valid():
#             print("niveau 2")
#             username = request.POST["username"]
#             email = request.POST["email"]
#              #username = form.cleaned_data['username']
#             # email = request.POST.get("email")
#              #email = form.cleaned_data['email']
#             password = request.POST.get(form.clean_password2)
#             print(f"niveau 3")
#             utilisateur = Utilisateur.objects.create_user(username=username,email=email,password=password)
#             utilisateur.is_active = False
#             token = generate_email_verification_token(utilisateur)
#             utilisateur.email_verification_token = token
#             utilisateur.save()
#             print(f"niveau 4 {utilisateur}")
#             print(f"niveau 5 {token}")
#             send_email(request,token, email)
#             print("niveau 6 apres send mail")
#             context = {'message': "un email vous est envoyé"}
#             return render(request,'usercompte/signup.html',context)
#          else:
#              context = {'message': "une erreur est survenu"}
#              return render(request,'usercompte/signup.html',context)
#      return render(request,'usercompte/signup.html')
    


# def signup(request):
#     if request.method == "POST":
#         form = InscriptionForm(request.POST)
#         print("niveau 1")
#         if form.is_valid():
#             print("niveau 2")
#             username = request.POST["username"]
#             email = request.POST["email"]
#             password = request.POST.get(form.clean_password2)
           
#             print(f"niveau 3")
#             utilisateur = Utilisateur.objects.create_user(username=username,email=email,password=password)
#             utilisateur.save()
#             return redirect('inscription-succes')
#         else:
#             context = {'message': "une erreur est survenu"}
#             return render(request,'usercompte/signup.html',context)
#     return render(request,'usercompte/signup.html')
    




def generate_email_verification_token(user):
    token = hashlib.sha256( f"{user.id}  {user.email.encode('utf-8')}  {user.username.encode('utf-8')}  {datetime.datetime.now()}".encode('utf-8') ).hexdigest()
    return token

def send_email(request,token, email):
    subject = "Confirmez votre inscription sur Gcom"
    #message = f"Cliquez sur ce lien pour confirmer votre inscription : {reverse('verify', kwargs={'token': token})}"
    #message = f"Cliquez sur ce lien pour confirmer votre inscription :{urljoin(request.META['HTTP_HOST'], reverse('verify', kwargs={'token': urlencode(token)}))}"  # encode doit recevoir un dictionnaire 
   # link = f"{request.META['HTTP_HOST']}{reverse('verify', kwargs={'token': urlencode(token)})}"
    #message = f"Cliquez sur ce lien pour confirmer votre inscription : {urljoin(request.META['HTTP_HOST'], reverse('verify', kwargs={'token':token}))}"
    message = f"Cliquez sur ce lien pour confirmer votre inscription :{urljoin(request.scheme + '://' + request.get_host(), reverse('verify', kwargs={'token': token}))}"

    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
   

# def verify(request,token):
#     if Utilisateur.objects.filter(email_verification_token=token).exists():
#        utilisateur = Utilisateur.objects.get(email_verification_token=token)      
#        utilisateur = Utilisateur.objects.filter(email_verification_token=token).first()
#     else:
#         print("token invalid")   
#     if utilisateur is not None:
#         utilisateur.is_active = True
#         utilisateur.email_verification_token = None
#         utilisateur.save()
#         print('compte activé')
#         return redirect('inscription-succes')


def verify(request,token):
        if Utilisateur.objects.filter(email_verification_token=token).exists():
            utilisateur = Utilisateur.objects.get(email_verification_token=token)
            print(f"voici l'utilisateur {utilisateur}")
            print(token)
            if utilisateur is not None:
                utilisateur.is_active = True
                utilisateur.email_verification_token = None
               # utilisateur.pk = None
                utilisateur.save()
                print('Compte activé')
                return redirect('inscription-succes')
        context = {'message': "l'utilisateur n'existe pas"}
        return render(request,'usercompte/inscriptionrefuse.html',context)
        


def login_user(request):
     if request.method == 'POST':
        username = request.POST['username']
        #email = request.POST['email']
        password = request.POST['password']

        print(password)
        print(username)
      
        user = authenticate(request,username=username,password=password)
        print(user)
        if user is not None and user.is_active:
            login(request, user)
            
            return redirect("gestionnaire:dashbord")
            #return redirect("{% url 'dashbord' user %}")
            #return render(request,'gestionnaire/dashbord.html',{"user":user})
           
        else:
              context = {'message': "identifiants incorects"}
              return render(request, 'usercompte/login.html',context)
              
     return render(request, 'usercompte/login.html')




# def login_u(request, username, password):
#     # Get the user object
#     user = UserManager.get_user_by_username(username)
    
#     if user is not None and user.check_password(password):
#         # Login the user
#         request.user = user
#         return True

#     return False



# def logout_user(request):
#      logout(request)     
#      return redirect('index')

  
# def login_user(request):
     
#     return LoginView.as_view(template_name='usercompte/login.html',
#                               success_url='gcom/dashbord.html',
#                               extra_context={'user':"user"}
#                               )(request)

     

def logout_user(request):
       return LogoutView.as_view(next_page=reverse_lazy('gcom:index'))(request)


def inscription_succes(request):
    reponse="votre inscription est validée"
    return render(request,"usercompte/inscriptionsucces.html", context={"reponse":reponse})

def inscription_refuse(request):
    reponse="votre inscription n'est pas validée"
    return render(request,"usercompte/inscriptionrefuse.html", context={"reponse":reponse})

def clean_password2(password1,password2):
         if password1 != password2:
            # raise forms.ValidationError('Les mots de passe ne correspondent pas.')
             context = {'message': "Les mots de passe ne correspondent pas."}
             
         return password2