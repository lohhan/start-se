from django.shortcuts import render # pega o html e renderiza ele
from django.http import HttpResponse

def cadastro(request):
   return render(request, 'cadastro.html') 