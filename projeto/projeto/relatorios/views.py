from django.shortcuts import render, redirect, get_object_or_404

# Decorator do django para requisição de login
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Ferramenta para união de duas tabelas diferentes
from itertools import chain

# Ferramenta para mandar uma lista para o template
import json as simplejson

from datetime import datetime

# Ferramenta para agregações e uso de datas
from django.db.models import Max, Min, Sum, Count
from itertools import chain
import datetime

# Importação dos modelos e formulários
from projeto.pessoas.models import Funcionario, PessoaFisica, PessoaJuridica
from projeto.produtos.models import Produto, Aquisicao
from projeto.vendas.models import ProdutoVendido, Caixa, Venda, Pagamento, Movimentacao, Despesa

# Create your views here.
@login_required
def relatorios_vendas(request):
	if request.method == 'POST':
		if request.POST.get('data_inicial') and request.POST.get('data_final'):
			data_inicial = request.POST.get('data_inicial')
			data_final = request.POST.get('data_final')
			vendas = Venda.objects.filter(venda_finalizada=True, criado_em__date__range=[data_inicial, data_final]).order_by('caixa')
			id_produtos = []
			for venda in vendas:
				produtos_vendidos = ProdutoVendido.objects.filter(venda=venda)
				for prod in produtos_vendidos:
					id_produtos.append(prod.id)
			produtos = ProdutoVendido.objects.filter(id__in=id_produtos)
			context = {
				'vendas': vendas,
				'produtos': produtos,
			}
			return render(request, 'relatorios_vendas.html', context)
	return render(request, 'relatorios_vendas.html')

@login_required
def relatorios_financeiros(request):
	if request.method == 'POST':
		if request.POST.get('data_inicial') and request.POST.get('data_final'):
			data_inicial = request.POST.get('data_inicial')
			data_final = request.POST.get('data_final') 
			start = datetime.datetime.strptime(data_inicial, '%Y-%m-%d')
			end = datetime.datetime.strptime(data_final, '%Y-%m-%d')
			step = datetime.timedelta(days=1)

			dados = []
			dados_mensais = []
			atual = start.month
			while start <= end:

				vnd = Venda.objects.filter(venda_finalizada=True, dia=start).values('dia').annotate(soma=Sum('valor_total'), total=Count('valor_total'))
				for v in vnd:
					dados_mensais.append(v)
				dsp = Despesa.objects.filter(data_pagamento_despesa=start)
				for d in dsp:
					dados_mensais.append(d)
				aqs = Aquisicao.objects.filter(data_pagamento=start)
				for a in aqs:
					dados_mensais.append(a)
				mvt = Movimentacao.objects.filter(dia=start)
				for m in mvt:
					dados_mensais.append(m)

				start += step
				if start.month == (atual + 1):
					dados.append(dados_mensais)
					dados_mensais = []
					atual = start.month
			dados.append(dados_mensais)
			dados_mensais = []
			#dados = list(chain(vnd, dsp, aqs, mvt))
			
			json_list = simplejson.dumps(dados, default=str)
			context = {
				'metricas_mensais': dados,
				'json_list': json_list,
			}
			return render(request, 'relatorios_financeiros.html', context)
	return render(request, 'relatorios_financeiros.html')

@login_required
def relatorios_produtos(request):
	if request.method == 'POST':
		if request.POST.get("tipo_relatorio") == "todos_produtos":
			produtos_vendidos = ProdutoVendido.objects.all().order_by('produto')
			produtos = []
			for prod in produtos_vendidos:
				tem = False
				for p in produtos:
					if p.produto == prod.produto:
						p.quantidade_produto = int(p.quantidade_produto) + int(prod.quantidade_produto)
						p.subtotal_venda = float(p.subtotal_venda) + float(prod.subtotal_venda)
						tem = True
				if tem == False:
					produtos.append(prod)
			context = {
				'produtos': produtos,
			}
			return render(request, 'relatorios_produtos.html', context)
		if request.POST.get("tipo_relatorio") == "todas_aquisicoes":
			aquisicoes = Aquisicao.objects.all().order_by('data_aquisicao')
			context = {
				'aquisicoes': aquisicoes,
			}
			return render(request, 'relatorios_produtos.html', context)
	return render(request, 'relatorios_produtos.html')