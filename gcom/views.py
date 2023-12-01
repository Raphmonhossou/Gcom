from django.shortcuts import render

def index(request):
    return render(request,'gcom/index.html')

def fonctionalite_view(request):
    return render(request,'gcom/fonctionalite.html')

def temoignage_view(request):
    return render(request,'gcom/temoignage.html')

def apropos_view(request):
    return render(request,'gcom/apropos.html')