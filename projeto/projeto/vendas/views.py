from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

# bibliotecas e aplicações necessárias para criar listviews.
import operator
from django.db.models import Q
from django.views.generic import ListView

from django.http import JsonResponse

# Ferramenta para união de duas tabelas diferentes
from itertools import chain

# Decorator do django para requisição de login
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Importação dos modelos e formulários
from projeto.pessoas.models import Funcionario, PessoaFisica, PessoaJuridica
from projeto.produtos.models import Produto
from .models import ProdutoVendido, Caixa, Venda, Pagamento, Movimentacao, Troca
from .forms import FormCaixa, FormMovimentacao, FormTroca

from datetime import datetime, date

@login_required
def adicionar_produtos(request, pk):
	
	v = Venda.objects.filter(pk=pk)
	if v[0].venda_finalizada:
		return redirect('comprovante_venda', v[0].pk)
	else:
		venda = Venda(pk=pk)
		valor_total = 0
		valor_pago = 0

		if request.is_ajax():
			param = request.GET.get('produto')
			if param:
				produto = Produto.objects.filter(nome_produto__icontains=param).order_by("nome_produto").values_list('nome_produto', flat=True)
				produtos = list(produto)
				return JsonResponse(produtos, safe=False)

		if request.method == 'POST':
			if request.POST.get('quantidade') != "" and request.POST.get('quantidade') > "0":
				produto_selecionado = Produto.objects.filter(nome_produto=request.POST.get('produto'))
				if int(produto_selecionado[0].quantidade) > 0 and int(produto_selecionado[0].quantidade) > int(request.POST.get('quantidade')):
					produto_vendido = ProdutoVendido.objects.filter(produto=produto_selecionado[0], venda=venda)
					if produto_vendido:
						qtd = produto_vendido[0].quantidade_produto
						produto_vendido[0].quantidade_produto = qtd + int(request.POST.get('quantidade'))
						produto_vendido.subtotal_venda = float(produto_selecionado[0].preco_venda) * float(produto_vendido.quantidade_produto)
						produto_vendido[0].save()
					else:
						produto_vendido = ProdutoVendido()
						produto_vendido.produto = produto_selecionado[0]
						produto_vendido.quantidade_produto = request.POST.get('quantidade')
						produto_vendido.valor_produto = produto_selecionado[0].preco_venda
						produto_vendido.subtotal_venda = float(produto_selecionado[0].preco_venda) * float(produto_vendido.quantidade_produto)
						produto_vendido.venda = venda
						produto_vendido.save()
					
					prod = Produto(pk=produto_selecionado[0].pk)
					prod.quantidade = int(produto_selecionado[0].quantidade) - int(request.POST.get('quantidade'))
					prod.save(update_fields=['quantidade'])


			if request.POST.get('aumenta'):
				id_prod = request.POST.get('aumenta')
				produto_vendido = ProdutoVendido.objects.filter(pk=id_prod, venda=venda)
				prod = ProdutoVendido(pk=id_prod,venda=venda)
				prod_selecionado = produto_vendido[0].produto

				qtd = produto_vendido[0].quantidade_produto
				prod.quantidade_produto = qtd + 1
				prod.save(update_fields=['quantidade_produto'])

				prod_selecionado.quantidade = int(prod_selecionado.quantidade) - 1
				prod_selecionado.save(update_fields=['quantidade'])

			elif request.POST.get('diminui'):
				id_prod = request.POST.get('diminui')
				produto_vendido = ProdutoVendido.objects.filter(pk=id_prod,venda=venda)
				prod = ProdutoVendido(pk=id_prod,venda=venda)
				prod_selecionado = produto_vendido[0].produto

				qtd = produto_vendido[0].quantidade_produto
				prod.quantidade_produto = qtd - 1

				prod_selecionado.quantidade = int(prod_selecionado.quantidade) + 1
				prod_selecionado.save(update_fields=['quantidade'])				
				if prod.quantidade_produto == 0:
					prod.delete()
				else:
					prod.save(update_fields=['quantidade_produto'])

			if request.POST.get('adicionar_pagamento') and request.POST.get('pagamentos') != "0":
				produtos_venda = ProdutoVendido.objects.filter(venda=venda)
				pagamentos_venda = Pagamento.objects.filter(venda=venda)
				
				valor_total = 0
				for prod in produtos_venda:
					valor_total += (float(prod.valor_produto) * float(prod.quantidade_produto))
				venda.valor_total = valor_total
				venda.save(update_fields=["valor_total"])


				valor_pago = 0
				for pagamento in pagamentos_venda:
					valor_pago += (float(pagamento.valor_total))

				falta_pagar = valor_total - valor_pago

				pagamento_selecionado = Pagamento.objects.filter(tipo_pagamento=request.POST.get('pagamentos'), venda=venda)
				if pagamento_selecionado:
					if request.POST.get('pagamentos') == "DI" or float(request.POST.get('valor_pago')) <= falta_pagar:
						pagamento_selecionado[0].valor_total = int(pagamento_selecionado[0].valor_total) + int(request.POST.get('valor_pago'))
						pagamento_selecionado[0].save()
					else:
						print("Valor maior que o da venda!")
				elif request.POST.get('pagamentos') == "DI" or float(request.POST.get('valor_pago')) <= falta_pagar:
					pagamento_realizado = Pagamento()
					pagamento_realizado.valor_total = request.POST.get('valor_pago')
					pagamento_realizado.tipo_pagamento = request.POST.get('pagamentos')
					pagamento_realizado.venda = venda
					pagamento_realizado.save()
				else:
					print("Valor maior que o da venda!")

			if request.POST.get('remover_pagamento'):
				id_pag = request.POST.get('remover_pagamento')
				pagamento_selecionado = Pagamento(pk=id_pag, venda=venda)
				pagamento_selecionado.delete()

		produtos_venda = ProdutoVendido.objects.filter(venda=venda)
		pagamentos_venda = Pagamento.objects.filter(venda=venda)
		valor_total = 0
		valor_pago = 0

		for prod in produtos_venda:
			valor_total += (float(prod.valor_produto) * float(prod.quantidade_produto))
		venda.valor_total = valor_total
		venda.save(update_fields=["valor_total"])

		for pagamento in pagamentos_venda:
			valor_pago += (float(pagamento.valor_total))

		falta_pagar = valor_total - valor_pago

		if request.method == 'POST' and request.POST.get('finalizar_venda'):
			for pagamento in pagamentos_venda:
				if pagamento.tipo_pagamento == "DI" and falta_pagar < 0:
					pagamento.valor_total = float(pagamento.valor_total) - (falta_pagar * - 1)
					pagamento.save()
					valor_total = 0
					valor_pago = 0
					for prod in produtos_venda:
						valor_total += (float(prod.valor_produto) * float(prod.quantidade_produto))
					venda.valor_total = valor_total
					venda.save(update_fields=["valor_total"])

					for pagamento in pagamentos_venda:
						valor_pago += (float(pagamento.valor_total))

					falta_pagar = valor_total - valor_pago
				
				if falta_pagar == 0:
					venda.venda_finalizada = True
					venda.ultima_atualizacao = timezone.now()
					venda.save(update_fields=["venda_finalizada", "ultima_atualizacao"])
					return redirect('comprovante_venda', venda.pk)
		
		context = {
				'valor_pago': valor_pago,
				'falta_pagar': falta_pagar,
				'produtos': produtos_venda,
				'pagamentos': pagamentos_venda,
				'venda': venda,
			}
		return render(request, 'adicionar_produtos.html', context)

@login_required
def fechamento_caixa(request, pk):
	caixa = Caixa(pk=pk)
	empresa = PessoaJuridica.objects.filter(is_empresa=True)

	vendas = Venda.objects.filter(caixa=caixa)
	total_caixa = 0
	total_credito = 0
	total_debito = 0
	total_dinheiro = 0
	produtos_vendidos = 0
	id_produtos = []
	for venda in vendas:
		total_caixa = total_caixa + float(venda.valor_total)
		pagamentos = Pagamento.objects.filter(venda=venda)
		for pagamento in pagamentos:
			if pagamento.tipo_pagamento == "DI":
				total_dinheiro = total_dinheiro + float(pagamento.valor_total)
			elif pagamento.tipo_pagamento == "CD":
				total_debito = total_debito + float(pagamento.valor_total)
			elif pagamento.tipo_pagamento == "CC":
				total_credito = total_credito + float(pagamento.valor_total)

		produtos_vendidos = ProdutoVendido.objects.filter(venda=venda)
		for prod in produtos_vendidos:
			id_produtos.append(prod.id)


	movimentacoes = Movimentacao.objects.filter(caixa=caixa)
	sangria = 0
	despesa = 0
	for movimentacao in movimentacoes:
		if movimentacao.tipo_movimentacao == 'S':
			sangria = sangria + float(movimentacao.valor_movimentacao)
		elif movimentacao.tipo_movimentacao == 'D':
			despesa = despesa + float(movimentacao.valor_movimentacao)

	dinheiro_caixa = float(caixa.fundo_caixa) + total_dinheiro - sangria - despesa
	c = Caixa.objects.filter(pk=pk)
	produtos_vendidos = ProdutoVendido.objects.filter(id__in=id_produtos).order_by('produto')
	produtos = []
	for prod in produtos_vendidos:
		tem = False
		for p in produtos:
			if p.produto == prod.produto:
				p.quantidade_produto = int(p.quantidade_produto) + int(prod.quantidade_produto)
				tem = True
		if tem == False:
			produtos.append(prod)



	context = {
		'empresa': empresa,
		'caixa': c,
		'total_caixa': total_caixa,
		'total_dinheiro': total_dinheiro,
		'total_debito': total_debito,
		'total_credito': total_credito,
		'sangria': sangria,
		'despesa': despesa,
		'dinheiro_caixa': dinheiro_caixa,
		'vendas': vendas,
		'produtos': produtos,
	}
	return render(request, 'fechamento_caixa.html', context)

@login_required
def caixa(request):
	caixas = Caixa.objects.filter(dia=date.today(), caixa_aberto=True)
	if caixas:
		continuar = False
		for c in caixas:
			if c.caixa_unico == False:
				caixa = c
				vendedor = Funcionario.objects.filter(user=request.user)
				continuar = True
			elif c.caixa_unico == True:
				if c.aberto_por == Funcionario.objects.filter(user=request.user):
					continuar = True
					caixa = c
					vendedor = c.aberto_por
					break
			else:
				continuar = False

		if continuar:
			if request.method == 'POST':
				caixa.fechado_por = vendedor[0]
				caixa.fechado_em = timezone.now()
				caixa.caixa_aberto = False
				caixa.save(update_fields=['fechado_por', 'fechado_em', 'caixa_aberto'])
				return redirect('fechamento_caixa', pk=caixa.pk)
			
			vendas = Venda.objects.filter(caixa=caixa)
			total_caixa = 0
			total_credito = 0
			total_debito = 0
			total_dinheiro = 0
			produtos_vendidos = 0
			for venda in vendas:
				total_caixa = total_caixa + float(venda.valor_total)
				pagamentos = Pagamento.objects.filter(venda=venda)
				produtos = ProdutoVendido.objects.filter(venda=venda)
				for pagamento in pagamentos:
					if pagamento.tipo_pagamento == "DI":
						total_dinheiro = total_dinheiro + float(pagamento.valor_total)
					elif pagamento.tipo_pagamento == "CD":
						total_debito = total_debito + float(pagamento.valor_total)
					elif pagamento.tipo_pagamento == "CC":
						total_credito = total_credito + float(pagamento.valor_total)
				for produto in produtos:
					produtos_vendidos = produtos_vendidos + int(produto.quantidade_produto)

			movimentacoes = Movimentacao.objects.filter(caixa=caixa)
			sangria = 0
			despesa = 0
			for movimentacao in movimentacoes:
				if movimentacao.tipo_movimentacao == 'S':
					sangria = sangria + float(movimentacao.valor_movimentacao)
				elif movimentacao.tipo_movimentacao == 'D':
					despesa = despesa + float(movimentacao.valor_movimentacao)

			dinheiro_caixa = float(caixa.fundo_caixa) + total_dinheiro - sangria - despesa

			context = {
				'vendedor': vendedor,
				'caixa': caixa,
				'total_caixa': total_caixa,
				'total_dinheiro': total_dinheiro,
				'total_debito': total_debito,
				'total_credito': total_credito,
				'produtos_vendidos': produtos_vendidos,
				'sangria': sangria,
				'despesa': despesa,
				'dinheiro_caixa': dinheiro_caixa,
			}
			template_name = "caixa.html"
			return render(request, template_name, context)
		else:
			return redirect('novo_caixa')
	else:
		return redirect('novo_caixa')

@login_required
def comprovante_venda(request, pk):
	venda = Venda.objects.filter(pk=pk)
	empresa = PessoaJuridica.objects.filter(is_empresa=True)
	produtos = ProdutoVendido.objects.filter(venda=venda[0])

	context = {
		'venda': venda,
		'empresa': empresa,
		'produtos': produtos,
	}
	template_name = "comprovante_venda.html"
	return render(request, template_name, context)

@login_required
def novo_caixa(request):
	if request.method == 'POST':
			form = FormCaixa(request.POST, request.FILES)
			if form.is_valid():
				caixa = form.save(commit=False)
				funcionario = Funcionario.objects.filter(user=request.user)
				caixa.aberto_por = funcionario[0]
				caixa.save()
				return redirect('caixa')

	form = FormCaixa()
	context = {
		'form': form,
	}
	template_name = 'novo_caixa.html'
	return render(request, template_name, context)

@login_required
def nova_venda(request):
	vendedor = Funcionario.objects.filter(user=request.user)
	caixa = Caixa.objects.filter(dia=date.today(), caixa_aberto=True)
	if caixa:
		if request.POST.get('remover') or request.method == 'GET':
			cliente = []

		if request.is_ajax():
			param = request.GET.get('cliente')
			if param:
				pf = PessoaFisica.objects.filter(is_cliente=True, CPF_CNPJ__icontains=param).order_by("nome_pf").values_list('CPF_CNPJ', flat=True)
				pj = PessoaJuridica.objects.filter(is_cliente=True, CPF_CNPJ__icontains=param).order_by("nome_fantasia").values_list('CPF_CNPJ', flat=True)
				clientes = list(chain(pf, pj))
				return JsonResponse(clientes, safe=False)

		if request.method == 'POST':
			cliente = []
			if request.POST.get('adicionar_cliente'):
				cliente_pj = PessoaJuridica.objects.filter(is_cliente=True, CPF_CNPJ=request.POST.get('cliente'))
				cliente_pf = PessoaFisica.objects.filter(is_cliente=True, CPF_CNPJ=request.POST.get('cliente'))
				if cliente_pf:
					cliente.append(cliente_pf[0])
				elif cliente_pj:
					cliente.append(cliente_pj[0])
				else:
					cliente = []

			if request.POST.get('continuar'):
				venda = Venda()
				cliente_pj = PessoaJuridica.objects.filter(is_cliente=True, CPF_CNPJ=request.POST.get('continuar'))
				cliente_pf = PessoaFisica.objects.filter(is_cliente=True, CPF_CNPJ=request.POST.get('continuar'))

				if cliente_pf:
					venda.cliente_pf = cliente_pf[0]
				elif cliente_pj:
					venda.cliente_pj = cliente_pj[0]

				venda.vendedor = vendedor[0]
				venda.caixa = caixa[0]

				venda.save()
				return redirect('adicionar_produtos', pk=venda.id)

		context = {
				'vendedor': vendedor,
				'cliente': cliente,
			}
		return render(request, 'venda.html', context)
	else:
		return redirect('caixa')

def nova_despesa(request, pk):
	form = FormMovimentacao()
	if request.method == 'POST':
		form = FormMovimentacao(request.POST, request.FILES)
		if form.is_valid():
			despesa = form.save(commit=False)
			if despesa.valor_movimentacao > 0:
					caixa = Caixa(pk=pk)
					despesa.caixa = caixa
					despesa.tipo_movimentacao = "D"
					funcionario = Funcionario.objects.filter(user=request.user)
					despesa.funcionario = funcionario[0]
					despesa.save()
					return redirect('caixa')
	context = {
				'form': form,
		}
	return render(request, 'nova_movimentacao.html', context)

def nova_sangria(request, pk):
	form = FormMovimentacao()
	if request.method == 'POST':
		form = FormMovimentacao(request.POST, request.FILES)
		if form.is_valid():
			sangria = form.save(commit=False)
			if sangria.valor_movimentacao > 0:
					caixa = Caixa(pk=pk)
					sangria.caixa = caixa
					sangria.tipo_movimentacao = "S"
					funcionario = Funcionario.objects.filter(user=request.user)
					sangria.funcionario = funcionario[0]
					sangria.save()
					return redirect('caixa')
	context = {
				'form': form,
		}
	return render(request, 'nova_movimentacao.html', context)

def edita_movimentacao(request, pk, id_caixa):
	instance = get_object_or_404(Movimentacao, id=pk)

	form = FormMovimentacao(request.POST or None, instance=instance)
	if request.method == 'POST':
		if form.is_valid():
			movimentacao = form.save(commit=False)
			if movimentacao.valor_movimentacao > 0:
				movimentacao.caixa_id = id_caixa
				movimentacao.save()
				return redirect('painel_movimentacoes', pk=id_caixa)
	context = {
				'form': form,
		}
	return render(request, 'nova_movimentacao.html', context)


class MovListView(ListView):
	template_name = 'movimentacoes.html'
	paginate_by = 10

	def get_queryset(self):
		caixa = Caixa(pk=self.kwargs['pk'])
		queryset = Movimentacao.objects.filter(caixa=caixa).order_by('tipo_movimentacao')
		query = self.request.GET.get('q')
		if query:
			queryset = Movimentacao.objects.filter(caixa=caixa).order_by('tipo_movimentacao')
			query_list = query.split()
			querysets = queryset
			for q in query_list:
				queryset = queryset.filter(Q(descricao_movimentacao__icontains=q) | Q(horario_movimentacao__icontains=q))
		
		return queryset

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super(MovListView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(MovListView, self).get_context_data(**kwargs)
		context['caixa'] = Caixa(pk=self.kwargs['pk'])
		return context

def vendas_do_caixa(request, pk):
	caixa = Caixa(pk=pk)
	vendas = Venda.objects.filter(caixa=caixa, venda_finalizada=True)
	funcionario = Funcionario(user=request.user)
	if request.method == 'GET' and request.GET.get('q'):
		query = request.GET.get('q')
		queryset = Venda.objects.filter(caixa=caixa)
		query_list = query.split()
		for q in query_list:
			vendedor = Funcionario.objects.filter(Q(CPF_CNPJ__icontains=q) | Q(nome_pf__icontains=q))
			cliente_pf = PessoaFisica.objects.filter(Q(CPF_CNPJ__icontains=q) | Q(nome_pf__icontains=q))
			cliente_pj = PessoaJuridica.objects.filter(Q(CPF_CNPJ__icontains=q) | Q(razao_social__icontains=q))
		if vendedor:
			for v in vendedor:
				vendas = queryset.filter(vendedor=v)
		elif cliente_pf:
			for pf in cliente_pf:
				vendas = queryset.filter(cliente_pf=pf)
		elif cliente_pj:
			for pj in cliente_pj:
				vendas = queryset.filter(cliente_pj=pj)

	context = {
				'vendas': vendas,
				'caixa': caixa,
				'funcionario': funcionario,
		}
	return render(request, 'vendas_do_caixa.html', context)

def painel_vendas(request):
	vendas = Venda.objects.none()
	funcionario = Funcionario(user=request.user)

	if request.method == 'GET' and request.GET.get('q'):
		query = request.GET.get('q')
		queryset = Venda.objects.filter(venda_finalizada=True)
		query_list = query.split()
		for q in query_list:
			vendedor = Funcionario.objects.filter(Q(CPF_CNPJ__icontains=q) | Q(nome_pf__icontains=q))
			cliente_pf = PessoaFisica.objects.filter(Q(CPF_CNPJ__icontains=q) | Q(nome_pf__icontains=q))
			cliente_pj = PessoaJuridica.objects.filter(Q(CPF_CNPJ__icontains=q) | Q(razao_social__icontains=q))
		if vendedor:
			for v in vendedor:
				vendas = queryset.filter(vendedor=v)
		elif cliente_pf:
			for pf in cliente_pf:
				vendas = queryset.filter(cliente_pf=pf)
		elif cliente_pj:
			for pj in cliente_pj:
				vendas = queryset.filter(cliente_pj=pj)

	if request.method == 'POST':
		if request.POST.get('data_inicial') and request.POST.get('data_final'):
			data_inicial = request.POST.get('data_inicial')
			data_final = request.POST.get('data_final')
			vendas = Venda.objects.filter(venda_finalizada=True, criado_em__date__range=[data_inicial, data_final]).order_by('caixa')
	context = {
				'vendas': vendas,
				'funcionario': funcionario,
		}
	return render(request, 'painel_vendas.html', context)

painel_movimentacoes = MovListView.as_view()
