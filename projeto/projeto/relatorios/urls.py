from django.urls import path, re_path

from . import views

urlpatterns = [
	re_path(r'^relatorios_vendas/$', views.relatorios_vendas, name='relatorios_vendas'),
	re_path(r'^relatorios_produtos/$', views.relatorios_produtos, name='relatorios_produtos'),
	re_path(r'^relatorios_financeiros/$', views.relatorios_financeiros, name='relatorios_financeiros'),
	
]