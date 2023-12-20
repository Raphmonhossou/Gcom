from django.shortcuts import redirect, render

from gstock.models import FamilleProduit, GroupeTaxe, UniteMesure
from gstock.form import FamilleForm, GroupeTaxeForm, UniteMesureForm



def paramettre(request):
    return render (request,'paramettre/base.html')

def famille_produit(request):
    print('fonction appele')
    if request.method == 'POST':
          form = FamilleForm(request.POST)
          if form.is_valid():
               print('post ici2')
               form.save()  
               famille = FamilleProduit.objects.all()
               nbr = famille.count()
               form = FamilleForm() # vider le formulaire
               context = {'ajouter_reussi': True,'famille': famille,'nbr':nbr,'form': form}
               return render (request,'paramettre/famille-produit.html', context)
       
    else:
       
        form = FamilleForm()

    famille = FamilleProduit.objects.all()
    nbr = famille.count()  
    context = {'famille': famille,'nbr':nbr,'form': form} 
    return render (request,'paramettre/famille-produit.html', context)

def unite_mesure(request):
    if request.method == 'POST':
       
          form = UniteMesureForm(request.POST)
          if form.is_valid():
               form.save()  
               unite = UniteMesure.objects.all()
               nbr = unite.count()
               form = UniteMesureForm() #vider
               context = {'ajouter_reussi': True,'unite': unite,'nbr':nbr,'form': form}
               return render (request,'paramettre/unite-mesure.html', context)
               
    

    else:
        form = UniteMesureForm()
    
    unite = UniteMesure.objects.all()
    nbr = unite.count()
    context = {'unite': unite,'nbr':nbr,'form': form}
    return render (request,'paramettre/unite-mesure.html', context)
             


def groupe_taxe(request):
    if request.method == 'POST':
       
          form = GroupeTaxeForm(request.POST)
          if form.is_valid():
                form.save()               
                taxe = GroupeTaxe.objects.all()
                nbr = GroupeTaxe.objects.count()
                form = GroupeTaxeForm()
                context = {'ajouter_reussi': True,'taxe': taxe,'nbr':nbr,'form': form}
                return render (request,'paramettre/groupe-taxe.html',context)
        
    else:

        form = GroupeTaxeForm()

    taxe = GroupeTaxe.objects.all()
    nbr = taxe.count()
    context = {'taxe': taxe,'nbr':nbr,'form': form}
    return render (request,'paramettre/groupe-taxe.html',context)