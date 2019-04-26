from django.urls import path, re_path

from . import views

urlpatterns = [
	path('painel_funcionarios', views.painel_funcionarios, name='painel_funcionarios'),
	path('novo_funcionario', views.novo_funcionario, name='novo_funcionario'),
	re_path(r'^edita_funcionario/(?P<cpf_cnpj>[\d\-\.\/]+)/$', views.edita_funcionario, name='edita_funcionario'),

	path('novo_cliente', views.novo_cliente, name='novo_cliente'),
	path('painel_clientes', views.painel_clientes, name='painel_clientes'),
	re_path(r'^edita_cliente/(?P<cpf_cnpj>[\d\-\.\/]+)/$', views.edita_cliente, name='edita_cliente'),

	path('novo_fornecedor', views.novo_fornecedor, name='novo_fornecedor'),
	path('painel_fornecedores', views.painel_fornecedores, name='painel_fornecedores'),
	re_path(r'^edita_fornecedor/(?P<cpf_cnpj>[\d\-\.\/]+)/$', views.edita_fornecedor, name='edita_fornecedor'),
]