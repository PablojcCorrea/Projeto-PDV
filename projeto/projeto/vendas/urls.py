from django.urls import path, re_path

from . import views

urlpatterns = [
	path('nova_venda/', views.nova_venda, name='nova_venda'),
	path('novo_caixa/', views.novo_caixa, name='novo_caixa'),
	path('caixa/', views.caixa, name='caixa'),
	re_path(r'^(?P<pk>.+)/nova_despesa/$', views.nova_despesa, name='nova_despesa'),
	re_path(r'^(?P<pk>.+)/nova_sangria/$', views.nova_sangria, name='nova_sangria'),
	re_path(r'^(?P<pk>.+)/painel_movimentacoes/$', views.painel_movimentacoes, name='painel_movimentacoes'),
	re_path(r'^(?P<pk>.+)/vendas_do_caixa/$', views.vendas_do_caixa, name='vendas_do_caixa'),
	re_path(r'^painel_vendas/$', views.painel_vendas, name='painel_vendas'),
	re_path(r'^(?P<id_caixa>.+)/edita_movimentacao/(?P<pk>.+)/$', views.edita_movimentacao, name='edita_movimentacao'),
	re_path(r'^comprovante_venda/(?P<pk>.+)/$', views.comprovante_venda, name='comprovante_venda'),
	re_path(r'^fechamento_caixa/(?P<pk>.+)/$', views.fechamento_caixa, name='fechamento_caixa'),
	#re_path(r'^(?P<pk>.+)/cadastrar_troca/$', views.cadastrar_troca, name='cadastrar_troca'),
	re_path(r'^(?P<pk>.+)/adicionar_produtos/$', views.adicionar_produtos, name='adicionar_produtos'),
]