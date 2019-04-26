from django.db import models
from projeto.pessoas.models import PessoaJuridica, Funcionario
from datetime import datetime


class Categoria(models.Model):
	nome_categoria = models.CharField('Categoria', max_length=50)
	descricao_categoria = models.TextField('Descrição', max_length=150)

	def __str__(self):
		return '%s' % self.nome_categoria


class Produto(models.Model):
	fornecedor = models.ForeignKey(
		PessoaJuridica, 
		limit_choices_to={'is_fornecedor': True},
		on_delete=models.CASCADE,
		null=True,
		blank=True
	)
	categoria = models.ForeignKey('Categoria', Categoria)

	nome_produto = models.CharField('Produto', max_length=60)
	descricao_produto = models.TextField('Descrição', max_length=150)

	quantidade = models.IntegerField('Quantidade')
	estoque_minimo = models.IntegerField('Estoque mínimo')

	tamanho = models.CharField('Tamanho', max_length=4, null=True, blank=True,)

	preco_custo = models.DecimalField('Preço de custo', decimal_places=2, default=0, max_digits=8)
	porcentagem_lucro = models.DecimalField('Porcentagem de Lucro', decimal_places=2, default=100, max_digits=8)
	preco_venda = models.DecimalField('Preço de venda', decimal_places=2, default=0, max_digits=8)

class Aquisicao(models.Model):
	produto_adquirido = models.ForeignKey(
		Produto, 
		on_delete=models.CASCADE,
	)

	funcionario = models.ForeignKey(
		Funcionario,
		on_delete=models.CASCADE,
	)

	is_primeira_aquisicao = models.BooleanField(default=False)

	data_aquisicao = models.DateTimeField(auto_now_add=True)
	data_pagamento = models.DateField('Data de pagamento', blank=True, null=True)
	valor_total_aquisicao = models.DecimalField('Valor total da aquisição', decimal_places=2, default=0, max_digits=8)
	
	preco_custo = models.DecimalField('Preço de custo', decimal_places=2, default=0, max_digits=8)
	porcentagem_lucro = models.DecimalField('Porcentagem de Lucro', decimal_places=2, default=100, max_digits=8)
	preco_venda = models.DecimalField('Preço de venda', decimal_places=2, default=0, max_digits=8)
	
	quantidade_produto = models.IntegerField('Quantidade adquirida')
