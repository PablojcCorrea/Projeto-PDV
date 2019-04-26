from django.db import models
from datetime import datetime

from projeto.pessoas.models import PessoaJuridica, PessoaFisica, Funcionario
from projeto.produtos.models import Produto

class Caixa(models.Model):
	fundo_caixa = models.DecimalField('Fundo do Caixa', decimal_places=2, default=0, max_digits=8)
	caixa_unico = models.BooleanField('Possuí um único vendedor?', default=False)

	aberto_por = models.ForeignKey(
		Funcionario, 
		on_delete=models.CASCADE,
		related_name='aberto_por',
	)
	fechado_por = models.ForeignKey(
		Funcionario, 
		on_delete=models.CASCADE,
		related_name='fechado_por',
		blank=True,
		null=True,
	)

	aberto_em = models.DateTimeField(auto_now_add=True)
	dia = models.DateField(auto_now_add=True)
	caixa_aberto = models.BooleanField(default=True)
	fechado_em = models.DateTimeField(auto_now=True, null=True)

class Venda(models.Model):
	cliente_pf = models.ForeignKey(
		PessoaFisica, 
		related_name='cliente_pf',
		on_delete=models.CASCADE,
		null=True,
		blank=True
	)
	cliente_pj = models.ForeignKey(
		PessoaJuridica, 
		related_name='cliente_pj',
		on_delete=models.CASCADE,
		null=True,
		blank=True
	)
	vendedor = models.ForeignKey(
		Funcionario, 
		related_name='vendedor',
		on_delete=models.CASCADE,
	)

	caixa = models.ForeignKey(
		Caixa,
		on_delete=models.CASCADE,
	)

	valor_total = models.DecimalField('Valor Total', decimal_places=2, default=0, max_digits=8)
	venda_finalizada = models.BooleanField('Venda finalizada?', default=False)
	dia = models.DateField(auto_now_add=True)

	criado_em = models.DateTimeField(auto_now_add=True)
	ultima_atualizacao = models.DateTimeField(auto_now=True)


class ProdutoVendido(models.Model):
	produto = models.ForeignKey(
		Produto,
		on_delete=models.CASCADE,
	)

	quantidade_produto = models.IntegerField('Quantidade de Produtos')
	valor_produto = models.DecimalField('Valor do Produto', decimal_places=2, default=0, max_digits=8)
	subtotal_venda = models.DecimalField('SubTotal', decimal_places=2, default=0, max_digits=8)

	venda = models.ForeignKey(
		Venda,
		on_delete=models.CASCADE,
	)

class Pagamento(models.Model):
	valor_total = models.DecimalField('Valor pago', decimal_places=2, default=0, max_digits=8)
	CARTAO_CREDITO = 'CC'
	CARTAO_DEBITO = 'CD'
	DINHEIRO = 'DI'

	TIPO_PAGAMENTO = (
		(CARTAO_DEBITO, 'Débito'),
		(CARTAO_CREDITO, 'Crédito'),
		(DINHEIRO, 'Dinheiro'),
		)

	tipo_pagamento = models.CharField('Tipo de Pagamento', max_length=3, choices=TIPO_PAGAMENTO, default=DINHEIRO)

	venda = models.ForeignKey(
		Venda,
		on_delete=models.CASCADE,
	)

class CategoriaMovimentacao(models.Model):
	nome_categoria = models.CharField('Categoria', max_length=80)
	descricao_categoria = models.TextField('Descrição', max_length=150)


class Movimentacao(models.Model):
	valor_movimentacao = models.DecimalField('Valor', decimal_places=2, default=0, max_digits=8)
	descricao_movimentacao = models.TextField('Descrição', max_length=150)

	categoria = models.ForeignKey(
		CategoriaMovimentacao,
		on_delete=models.CASCADE,
	)

	funcionario = models.ForeignKey(
		Funcionario, 
		on_delete=models.CASCADE,
	)
	horario_movimentacao = models.DateTimeField(auto_now_add=True)
	dia = models.DateField(auto_now_add=True)

	SANGRIA = "S"
	DESPESA = "D"
	TIPO_MOVIMENTACAO = (
		(SANGRIA, 'Sangria'),
		(DESPESA, 'Despesa'),
		)

	tipo_movimentacao = models.CharField('Tipo de Movimentação', max_length=1, choices=TIPO_MOVIMENTACAO, default=DESPESA)
	caixa = models.ForeignKey(
		Caixa,
		on_delete=models.CASCADE,
	)

class Despesa(models.Model):
	valor_despesa = models.DecimalField('Valor', decimal_places=2, default=0, max_digits=8)
	descricao_despesa = models.TextField('Descrição', max_length=150)

	categoria = models.ForeignKey(
		CategoriaMovimentacao,
		on_delete=models.CASCADE,
	)

	funcionario = models.ForeignKey(
		Funcionario, 
		on_delete=models.CASCADE,
	)

	horario_despesa = models.DateTimeField(auto_now_add=True)
	data_pagamento_despesa = models.DateField('Data de pagamento', blank=True, null=True)

class Troca(models.Model):
	produto_devolvido = models.ForeignKey(
		Produto, 
		on_delete=models.CASCADE,
		related_name='produto_devolvido',
	)
	produto_trocado = models.ForeignKey(
		Funcionario, 
		on_delete=models.CASCADE,
		related_name='produto_trocado',
		blank=True,
		null=True,
	)

	valor_troca = models.DecimalField('Diferença de valor', decimal_places=2, default=0, max_digits=8)
	motivo_troca = models.TextField('Motivo', max_length=150, null=True, blank=True)

	tem_defeito = models.BooleanField(default=False)
	devolucao = models.BooleanField(default=False)

	horario_troca = models.DateTimeField(auto_now_add=True)

	caixa = models.ForeignKey(
		Caixa,
		on_delete=models.CASCADE,
	)
