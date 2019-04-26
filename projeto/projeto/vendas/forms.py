from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import User

# Importação dos modelos necessários para gerar os formulários
from .models import Caixa, Movimentacao, Troca

class FormCaixa(forms.ModelForm):
	class Meta:
		model = Caixa
		fields = '__all__'
		exclude = ('aberto_por','fechado_por','caixa_aberto')

	def __init__(self, *args, **kwargs):
		super(FormCaixa, self).__init__(*args, **kwargs)
		self.fields['fundo_caixa'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['caixa_unico'].widget.attrs.update({'class' : 'w3-radio'})
		self.fields['caixa_unico'].label = "Marque se um único vendedor utiliza o caixa:"

class FormMovimentacao(forms.ModelForm):
	class Meta:
		model = Movimentacao
		fields = '__all__'
		exclude = ('tipo_movimentacao','caixa', 'funcionario')

	def __init__(self, *args, **kwargs):
		super(FormMovimentacao, self).__init__(*args, **kwargs)
		self.fields['valor_movimentacao'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['descricao_movimentacao'].widget.attrs.update({'class' : 'w3-input'})

class FormTroca(forms.ModelForm):
	class Meta:
		model = Troca
		fields = '__all__'
		exclude = ('caixa',)

	def __init__(self, *args, **kwargs):
		super(FormTroca, self).__init__(*args, **kwargs)
		self.fields['valor_troca'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['motivo_troca'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['produto_devolvido'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['produto_trocado'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['tem_defeito'].widget.attrs.update({'class' : 'w3-radio'})
		self.fields['devolucao'].widget.attrs.update({'class' : 'w3-radio'})