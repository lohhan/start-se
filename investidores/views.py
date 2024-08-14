from django.shortcuts import render, redirect
from empresarios.models import Empresas, Documento, Metricas
from .models import PropostaInvestimento
from django.http import HttpResponse, Http404
from django.contrib import messages
from django.contrib.messages import constants

# Create your views here.
def sugestao(request):
   if not request.user.is_authenticated:
      return redirect('/usuarios/logar')

   areas = Empresas.area_choices

   if request.method == "GET":
      return render(request, 'sugestao.html', {"areas": areas})
   elif request.method == "POST":
      tipo = request.POST.get('tipo')
      area = request.POST.getlist('area')
      valor = request.POST.get('valor')

      if tipo == "C":
         empresas = Empresas.objects.filter(tempo_existencia="+5").filter(estagio="E")
      elif tipo == "D":
         empresas = Empresas.objects.filter(tempo_existencia__in=["-6", "+6", "+1"]).exclude(estagio="E")
      elif tipo == "V":
         empresas = Empresas.objects.filter(estagio__in=["I", "MVP"])
      elif tipo == "A":
         empresas = Empresas.objects.filter(estagio="MVPP").filter(tempo_existencia__in=["+6", "+1", "+5"])
      elif tipo == "JE":
         empresas = Empresas.objects.filter(tempo_existencia__in=["-6", "+6", "+1"])


      empresas = empresas.filter(area__in=area)
      
      empresas_selecionadas = []
      for empresa in empresas:
         percentual = ((float(valor) * 100)/float(empresa.valuation))
         if percentual >= 1:
            empresas_selecionadas.append(empresa)

      return render(request, 'sugestao.html', {"areas": areas, "empresas": empresas_selecionadas})

def ver_empresa(request, id):
   if not request.user.is_authenticated:
      return redirect('/usuarios/logar')

   empresa = Empresas.objects.get(id=id)
   documentos = Documento.objects.filter(empresa=empresa)
   metricas = Metricas.objects.filter(empresa=empresa)
   
   percentual_vendido = sum(PropostaInvestimento.objects.filter(empresa=empresa).filter(status="PA").values_list("percentual", flat=True))
   percentual_disponivel = empresa.percentual_equity - percentual_vendido

   limiar = (80 * empresa.percentual_equity) / 100
   concretizado = False
   if percentual_vendido >= limiar:
      concretizado = True

   return render(request, 'ver_empresa.html', {"empresa": empresa, "documentos": documentos, "metricas": metricas,"percentual_vendido": int(percentual_vendido), "percentual_disponivel": int(percentual_disponivel), "concretizado": concretizado})

def realizar_proposta(request, id):
   valor = request.POST.get('valor')
   percentual = request.POST.get('percentual')
   empresa = Empresas.objects.get(id=id)

   propostas_aceitas = PropostaInvestimento.objects.filter(empresa=empresa).filter(status="PA")
   
   total = 0
   for pa in propostas_aceitas:
      total += pa.percentual

   if (total + float(percentual)) > empresa.percentual_equity:
      messages.add_message(request, constants.WARNING, 'O percentual solicitado ultrapassa o percentual máximo.')
      return redirect(f'/investidores/ver_empresa/{empresa.id}')
   
   valuation = (100 * int(valor)) / int(percentual)
   valuation_necessario = (int(empresa.valuation / 2))

   if valuation < valuation_necessario:
      messages.add_message(request, constants.WARNING, f'O valuation proposto foi R$ {valuation}, e deve ser no mínimo R$ {valuation_necessario}.')
      return redirect(f'/investidores/ver_empresa/{empresa.id}')

   try:
      pi = PropostaInvestimento(
         valor=valor,
         percentual=percentual,  
         empresa=empresa,
         investidor=request.user
      )
      pi.save()
   except:
      messages.add_message(request, constants.ERROR, 'Erro interno do servidor.')
      return redirect(f'/investidores/ver_empresa/{empresa.id}')
   
   return redirect(f'/investidores/assinar_contrato/{pi.id}')

def assinar_contrato(request, id):
   pi = PropostaInvestimento.objects.get(id=id)

   if request.user != pi.investidor:
      return redirect('/usuarios/logar')
   
   if pi.status != "AS":
      raise Http404()

   if request.method == "GET":
      return render(request, 'assinar_contrato.html', {"proposta_investimento": pi})
   elif request.method == "POST":
      selfie = request.FILES.get('selfie')
      rg = request.FILES.get('rg')

      pi.selfie = selfie
      pi.rg = rg
      pi.status = "PE"
      pi.save()

      messages.add_message(request, constants.SUCCESS, f'Contrato assinado com sucesso, sua proposta foi enviada a empresa.')
      return redirect(f'/investidores/ver_empresa/{pi.empresa.id}')
   
   