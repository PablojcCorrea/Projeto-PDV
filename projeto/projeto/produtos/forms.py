from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import User

# Importação dos modelos necessários para gerar os formulários
from .models import Produto, Categoria, Aquisicao

class FormProduto(forms.ModelForm):
	class Meta:
		model = Produto
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super(FormProduto, self).__init__(*args, **kwargs)
		self.fields['categoria'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['fornecedor'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['nome_produto'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['descricao_produto'].widget.attrs.update({'class' : 'w3-input', 'style' : 'height: 80px;'})
		self.fields['quantidade'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['estoque_minimo'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['preco_custo'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['preco_venda'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['tamanho'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['porcentagem_lucro'].widget.attrs.update({'class' : 'w3-input'})

class FormCategoria(forms.ModelForm):
	class Meta:
		model = Categoria
		fields = '__all__'



	def __init__(self, *args, **kwargs):
		super(FormCategoria, self).__init__(*args, **kwargs)
		self.fields['nome_categoria'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['descricao_categoria'].widget.attrs.update({'class' : 'w3-input'})

		
class DateInput(forms.DateInput):
	input_type = 'date'

class FormAquisicao(forms.ModelForm):
	class Meta:
		model = Aquisicao
		fields = '__all__'
		exclude = ('produto_adquirido', 'funcionario', 'is_primeira_aquisicao', 'data_aquisicao')
		widgets = {
			'data_pagamento': DateInput()
			}

	def __init__(self, *args, **kwargs):
		super(FormAquisicao, self).__init__(*args, **kwargs)
		self.fields['quantidade_produto'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['preco_custo'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['preco_venda'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['porcentagem_lucro'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['data_pagamento'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['valor_total_aquisicao'].widget.attrs.update({'class' : 'w3-input'})