from django.urls import path, re_path

from . import views

urlpatterns = [
	path('nova_categoria', views.nova_categoria, name='nova_categoria'),
	path('painel_categorias', views.painel_categorias, name='painel_categorias'),
	re_path(r'^edita_categoria/(?P<pk>.+)/$', views.edita_categoria, name='edita_categoria'),

	path('novo_produto', views.novo_produto, name='novo_produto'),
	path('painel_produtos', views.painel_produtos, name='painel_produtos'),
	re_path(r'^edita_produto/(?P<pk>.+)/$', views.edita_produto, name='edita_produto'),

	re_path(r'^reposicao/(?P<pk>.+)/$', views.reposicao, name='reposicao'),

]
