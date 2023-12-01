from django.shortcuts import render


def dashbord_view(request):
    return render(request,'gestionnaire/dashbord.html')
