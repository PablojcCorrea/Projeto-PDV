from django.shortcuts import render, redirect, resolve_url
from django.http import HttpResponse

from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, update_session_auth_hash, login as auth_login, authenticate, settings
)
from django.contrib.auth.forms import (
    AuthenticationForm,
)
from django.contrib.sites.shortcuts import get_current_site
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.http import HttpResponseRedirect, QueryDict
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from projeto.pessoas.models import Endereco, PessoaJuridica, Funcionario
from projeto.pessoas.forms import FormEndereco, FormEmpresa, FormFuncionario
from django.contrib.auth.forms import UserCreationForm
# Decorator do django para requisição de login
from django.contrib.auth.decorators import login_required

from projeto.vendas.models import Venda, ProdutoVendido
from projeto.produtos.models import Produto, Aquisicao

@login_required
def index(request):
	funcionario = Funcionario.objects.filter(user=request.user)
	if funcionario[0].tipo_funcionario == 'GER':
		produtos = Produto.objects.all()
		id_produto = []
		for prod in produtos:
			if prod.quantidade <= prod.estoque_minimo:
				id_produto.append(prod.pk)

		produtos = Produto.objects.filter(id__in=id_produto)
		aquisicoes = Aquisicao.objects.all().order_by('data_aquisicao')[:5][::-1]
		ultimas_vendas = Venda.objects.filter()[:5][::-1]

		context = {
			'funcionario': funcionario,
			'produtos': produtos,
			'aquisicoes': aquisicoes,
			'vendas': ultimas_vendas,
		}
		return render(request, 'painel_gerente.html', context)

	if funcionario[0].tipo_funcionario == 'EST':
		produtos = Produto.objects.all()
		id_produto = []
		for prod in produtos:
			if prod.quantidade <= prod.estoque_minimo:
				id_produto.append(prod.pk)

		produtos = Produto.objects.filter(id__in=id_produto)
		aquisicoes = Aquisicao.objects.filter(funcionario=funcionario[0]).order_by('data_aquisicao')[:5][::-1]
		context = {
			'funcionario': funcionario,
			'aquisicoes': aquisicoes,
			'produtos': produtos,
		}
		return render(request, 'painel_estoquista.html', context)

	if funcionario[0].tipo_funcionario == 'VEN':
		vendas = Venda.objects.filter(vendedor=funcionario[0])
		quantidade_vendas = 0
		valor_total_vendas = 0
		produtos_vendidos = 0
		id_vendas = []
		for v in vendas:
			id_vendas.append(v.id)
			valor_total_vendas += v.valor_total
			quantidade_vendas += 1
			prod_vendidos = ProdutoVendido.objects.filter(venda=v)
			for prod in prod_vendidos:
				produtos_vendidos += 1

		ultimas_vendas = Venda.objects.filter(vendedor=funcionario[0])[:5][::-1]

		context = {
			'vendedor': funcionario,
			'valor_total_vendas': valor_total_vendas,
			'quantidade_vendas': quantidade_vendas,
			'produtos_vendidos': produtos_vendidos,
			'vendas': ultimas_vendas,
		}
		return render(request, 'painel_vendedor.html', context)

def registra_empresa(request):
	empresa = PessoaJuridica.objects.filter(is_empresa=True)

	if empresa:
		return redirect('index')
	else:
		if request.method == 'POST':
			formEmp = FormEmpresa(request.POST, request.FILES)
			formEnd = FormEndereco(request.POST, request.FILES)

			if formEmp.is_valid() and formEnd.is_valid():
				empresa = formEmp.save(commit=False)
				empresa.is_empresa = True
				empresa.save()
				endereco = formEnd.save(commit=False)
				endereco.empresa = empresa
				endereco.save()
				return redirect('index')

		formEnd = FormEndereco()
		formEmp	= FormEmpresa()

		template_name = 'registra_empresa.html'
		context = {
			'form': formEmp,
			'form2': formEnd
		}

		return render(request, template_name, context)

def registra_primeiro_funcionario(request):
	empresa = PessoaJuridica.objects.filter(is_empresa=True)

	if empresa:
		return redirect('index')
	else:
		if request.method == 'POST':
			formFunc = FormFuncionario(request.POST, request.FILES)
			formEnd = FormEndereco(request.POST, request.FILES)
			if formFunc.is_valid() and formEnd.is_valid():
				funcionario = formFunc.save(commit=False)
				funcionario.is_funcionario = True
				funcionario.tipo_funcionario = 'GER'
				funcionario.save()
				endereco = formEnd.save(commit=False)
				endereco.morador = funcionario
				endereco.save()
				auth_login(request, funcionario.user)
				return redirect('registra_empresa')

		formFunc = FormFuncionario()
		formEnd = FormEndereco()

		template_name = 'registra_empresa.html'
		context = {
			'form': formFunc,
			'form2': formEnd
		}
		return render(request, template_name, context)

@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
	      current_app=None, extra_context=None):
	
	empresa = PessoaJuridica.objects.filter(is_empresa=True)

	if empresa:
		"""
		Displays the login form and handles the login action.
		"""
		redirect_to = request.POST.get(redirect_field_name, request.GET.get(redirect_field_name, ''))

		if request.method == "POST":
			form = authentication_form(request, data=request.POST)
			if form.is_valid():

		        # Ensure the user-originating redirection url is safe.
				if not is_safe_url(url=redirect_to, host=request.get_host()):
					redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

		        # Okay, security check complete. Log the user in.
				auth_login(request, form.get_user())

				return HttpResponseRedirect(redirect_to)
		else:
			form = authentication_form(request)

		current_site = get_current_site(request)

		context = {
			'form': form,
			redirect_field_name: redirect_to,
		 	'site': current_site,
		 	'site_name': current_site.name,
		}
		if extra_context is not None:
		 	context.update(extra_context)

		if current_app is not None:
		 	request.current_app = current_app

		return TemplateResponse(request, template_name, context)
	else:
		return redirect('registra_primeiro_funcionario')