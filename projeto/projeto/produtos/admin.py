from django.contrib import admin
from projeto.produtos.models import Produto, Categoria, Aquisicao

class ProdutoAdmin(admin.ModelAdmin):
	list_display = ['nome_produto', 'quantidade', 'preco_venda']
	search_fields = ['nome_produto']

class CategoriaAdmin(admin.ModelAdmin):
	list_display = ['nome_categoria', 'descricao_categoria']
	search_fields = ['nome_categoria']

class AquisicaoAdmin(admin.ModelAdmin):
	list_display = ['produto_adquirido', 'quantidade_produto', 'funcionario', 'data_aquisicao']
	search_fields = ['produto_adquirido', 'data_aquisicao']


# Re-register UserAdmin
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Aquisicao, AquisicaoAdmin)
