from django.urls import path, re_path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	re_path(r'^registra_empresa/$', views.registra_empresa, name='registra_empresa'),	
	re_path(r'^registra_funcionario/$', views.registra_primeiro_funcionario, name='registra_primeiro_funcionario'),	

]
