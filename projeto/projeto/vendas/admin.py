from django.contrib import admin
from projeto.vendas.models import Venda, Caixa, ProdutoVendido, Pagamento, Movimentacao, CategoriaMovimentacao, Despesa

class CaixaAdmin(admin.ModelAdmin):
	list_display = ['aberto_por', 'fechado_por', 'aberto_em']
	search_fields = ['aberto_por', 'fechado_por', 'aberto_em']

class VendaAdmin(admin.ModelAdmin):
	list_display = ['id','vendedor', 'caixa', 'valor_total']
	search_fields = ['vendedor', 'caixa', 'valor_total']

class ProdutoVendidoAdmin(admin.ModelAdmin):
	list_display = ['produto', 'quantidade_produto', 'valor_produto']
	search_fields = ['produto']

class PagamentoAdmin(admin.ModelAdmin):
	list_display = ['tipo_pagamento', 'valor_total', 'venda']
	search_fields = ['tipo_pagamento', 'valor_total', 'venda']

class MovimentacaoAdmin(admin.ModelAdmin):
	list_display = ['tipo_movimentacao', 'valor_movimentacao', 'horario_movimentacao']
	search_fields = ['tipo_movimentacao', 'valor_movimentacao', 'horario_movimentacao']

class CategoriaMovimentacaoAdmin(admin.ModelAdmin):
	list_display = ['id', 'nome_categoria', 'descricao_categoria']
	search_fields = ['nome_categoria', 'descricao_categoria']

class DespesaAdmin(admin.ModelAdmin):
	list_display = ['valor_despesa', 'descricao_despesa', 'horario_despesa']
	search_fields = ['valor_despesa', 'descricao_despesa', 'horario_despesa']


# Re-register UserAdmin
admin.site.register(Caixa, CaixaAdmin)
admin.site.register(Venda, VendaAdmin)
admin.site.register(ProdutoVendido, ProdutoVendidoAdmin)
admin.site.register(Pagamento, PagamentoAdmin)
admin.site.register(Movimentacao, MovimentacaoAdmin)
admin.site.register(CategoriaMovimentacao, CategoriaMovimentacaoAdmin)
admin.site.register(Despesa, DespesaAdmin)
