from django.shortcuts import render, redirect, get_object_or_404

# bibliotecas e aplicações necessárias para criar listviews.
import operator
from django.db.models import Q
from django.views.generic import ListView

# Ferramenta para união de duas tabelas diferentes
from itertools import chain

# Decorator do django para requisição de login
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# Importação dos modelos e formulários
from .models import Funcionario, Endereco, PessoaJuridica, PessoaFisica
from .forms import FormFuncionario, FormEndereco, FormEditaFuncionario, FormPessoaJuridica, FormPessoaFisica, FormEditaPessoaFisica, FormEditaPessoaJuridica

# Views de Funcionários (Cadastro, Edição e Consulta)
@login_required
def novo_funcionario(request):
	user = Funcionario.objects.filter(user=request.user)
	if user:
		if user[0].tipo_funcionario == 'GER':
			continuar = True
		else:
			continuar = False
	elif request.user.is_superuser or request.user.is_staff:
		continuar = True
	else:
		continuar = False

	if continuar:
		if request.method == 'POST':
			formFunc = FormFuncionario(request.POST, request.FILES)
			formEnd = FormEndereco(request.POST, request.FILES)
			if formFunc.is_valid() and formEnd.is_valid():
				funcionario = formFunc.save(commit=False)
				funcionario.is_funcionario = True
				funcionario.save()
				endereco = formEnd.save(commit=False)
				endereco.morador = funcionario
				endereco.save()

		formFunc = FormFuncionario()
		formEnd = FormEndereco()

		template_name = 'funcionarios/novo_funcionario.html'
		context = {
			'form': formFunc,
			'form2': formEnd
		}

		return render(request, template_name, context)
	else:
		template_name = 'sem_permissao.html'
		return render(request, template_name)

def edita_funcionario(request, cpf_cnpj):
	instance = get_object_or_404(Funcionario, CPF_CNPJ=cpf_cnpj)
	instance2 = get_object_or_404(Endereco, morador=instance)
	
	formFunc = FormEditaFuncionario(request.POST or None, instance=instance)
	formEnd = FormEndereco(request.POST or None, instance=instance2)
	if formFunc.is_valid() and formEnd.is_valid():
		funcionario = formFunc.save(commit=False)
		endereco = formEnd.save(commit=False)
		if request.method == 'POST':
			formFunc.save()
			formEnd.save()
			return redirect(painel_funcionarios)

	template_name = 'funcionarios/edita_funcionario.html'
	context = {
		'form': formFunc,
		'form2': formEnd
	}

	return render(request, template_name, context)


class FuncListView(ListView):
	template_name = 'funcionarios/funcionarios.html'
	paginate_by = 10

	def get_queryset(self):
		queryset = Funcionario.objects.all()
		query = self.request.GET.get('q')
		if query:
			queryset = Funcionario.objects.all()
			query_list = query.split()
			querysets = queryset
			for q in query_list:
				queryset = queryset.filter(Q(nome_pf__icontains=q) | Q(CPF_CNPJ__icontains=q))
		return queryset

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super(FuncListView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(FuncListView, self).get_context_data(**kwargs)
		return context

# Definição das views de clientes
@login_required
def novo_cliente(request):

	template_name = 'clientes/novo_cliente.html'

	if request.method == 'POST':
		formPF = FormPessoaFisica(request.POST, request.FILES)
		formPJ = FormPessoaJuridica(request.POST, request.FILES)
		formEnd = FormEndereco(request.POST, request.FILES)

		if formPF.is_valid() and formEnd.is_valid():
			pf = formPF.save(commit=False)
			pf.CPF_CNPJ = request.POST.get('CPF_CNPJ')
			pf.email = request.POST.get('email')
			pf.telefone = request.POST.get('telefone')
			pf.is_cliente = True
			pf.save()
			endereco = formEnd.save(commit=False)
			endereco.morador = pf
			endereco.save()

		elif formPJ.is_valid() and formEnd.is_valid():
			pj = formPJ.save(commit=False)
			pj.CPF_CNPJ = request.POST.get('CPF_CNPJ')
			pj.email = request.POST.get('email')
			pj.telefone = request.POST.get('telefone')
			pj.is_cliente = True
			pj.save()
			endereco = formEnd.save(commit=False)
			endereco.empresa = pj
			endereco.save()

	formPF = FormPessoaFisica()
	formPJ = FormPessoaJuridica()
	formEnd = FormEndereco()

	context = {
		'formPF': formPF,
		'formPJ': formPJ,
		'formEnd': formEnd
	}

	return render(request, template_name, context)

@login_required
def edita_cliente(request, cpf_cnpj):
	if len(cpf_cnpj) == 14:
		instance = get_object_or_404(PessoaFisica, CPF_CNPJ=cpf_cnpj)
		instance2 = get_object_or_404(Endereco, morador=instance)
		formPes = FormEditaPessoaFisica(request.POST or None, instance=instance)
	elif len(cpf_cnpj) == 18:
		instance = get_object_or_404(PessoaJuridica, CPF_CNPJ=cpf_cnpj)
		instance2 = get_object_or_404(Endereco, empresa=instance)
		formPes = FormEditaPessoaJuridica(request.POST or None, instance=instance)

	formEnd = FormEndereco(request.POST or None, instance=instance2)

	if formPes.is_valid() and formEnd.is_valid():
		pessoa = formPes.save(commit=False)
		endereco = formEnd.save(commit=False)
		if request.method == 'POST':
			formPes.save()
			formEnd.save()
			return redirect(painel_clientes)

	template_name = 'clientes/edita_cliente.html'
	context = {
		'form': formPes,
		'form2': formEnd
	}

	return render(request, template_name, context)

class ClienteListView(ListView):
	template_name = 'clientes/clientes.html'
	paginate_by = 10

	def get_queryset(self):
		pf = PessoaFisica.objects.filter(is_cliente=True).order_by("nome_pf")
		pj = PessoaJuridica.objects.filter(is_cliente=True).order_by("nome_fantasia")
		queryset = list(chain(pf, pj))
		query = self.request.GET.get('q')
		if query:
			query_list = query.split()
			for q in query_list:
				pf = pf.filter(Q(nome_pf__icontains=q) | Q(CPF_CNPJ__icontains=q))
				pf.model_name = pf.model.__name__
				pj = pj.filter(Q(CPF_CNPJ__icontains=q) | Q(nome_fantasia__icontains=q))
				pj.model_name = pj.model.__name__
				queryset = list(chain(pf, pj))
		return queryset

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super(ClienteListView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(ClienteListView, self).get_context_data(**kwargs)
		return context

# Views de Fornecedores
@login_required
def novo_fornecedor(request):

	template_name = 'fornecedores/novo_fornecedor.html'

	if request.method == 'POST':
		formPF = FormPessoaFisica(request.POST, request.FILES)
		formPJ = FormPessoaJuridica(request.POST, request.FILES)
		formEnd = FormEndereco(request.POST, request.FILES)

		if formPF.is_valid() and formEnd.is_valid():
			pf = formPF.save(commit=False)
			pf.CPF_CNPJ = request.POST.get('CPF_CNPJ')
			pf.email = request.POST.get('email')
			pf.telefone = request.POST.get('telefone')
			pf.is_fornecedor = True
			pf.save()
			endereco = formEnd.save(commit=False)
			endereco.morador = pf
			endereco.save()

		elif formPJ.is_valid() and formEnd.is_valid():
			pj = formPJ.save(commit=False)
			pj.CPF_CNPJ = request.POST.get('CPF_CNPJ')
			pj.email = request.POST.get('email')
			pj.telefone = request.POST.get('telefone')
			pj.is_fornecedor = True
			pj.save()
			endereco = formEnd.save(commit=False)
			endereco.empresa = pj
			endereco.save()

	formPF = FormPessoaFisica()
	formPJ = FormPessoaJuridica()
	formEnd = FormEndereco()

	context = {
		'formPF': formPF,
		'formPJ': formPJ,
		'formEnd': formEnd
	}

	return render(request, template_name, context)

@login_required
def edita_fornecedor(request, cpf_cnpj):
	if len(cpf_cnpj) == 14:
		instance = get_object_or_404(PessoaFisica, CPF_CNPJ=cpf_cnpj)
		instance2 = get_object_or_404(Endereco, morador=instance)
		formPes = FormEditaPessoaFisica(request.POST or None, instance=instance)
	elif len(cpf_cnpj) == 18:
		instance = get_object_or_404(PessoaJuridica, CPF_CNPJ=cpf_cnpj)
		instance2 = get_object_or_404(Endereco, empresa=instance)
		formPes = FormEditaPessoaJuridica(request.POST or None, instance=instance)

	formEnd = FormEndereco(request.POST or None, instance=instance2)

	if formPes.is_valid() and formEnd.is_valid():
		pessoa = formPes.save(commit=False)
		endereco = formEnd.save(commit=False)
		if request.method == 'POST':
			formPes.save()
			formEnd.save()
			return redirect(painel_fornecedores)

	template_name = 'fornecedores/edita_fornecedor.html'
	context = {
		'form': formPes,
		'form2': formEnd
	}

	return render(request, template_name, context)

class FornecedorListView(ListView):
	template_name = 'fornecedores/fornecedores.html'
	paginate_by = 10

	def get_queryset(self):
		pf = PessoaFisica.objects.filter(is_fornecedor=True).order_by("nome_pf")
		pj = PessoaJuridica.objects.filter(is_fornecedor=True).order_by("nome_fantasia")
		queryset = list(chain(pf, pj))
		query = self.request.GET.get('q')
		if query:
			query_list = query.split()
			for q in query_list:
				pf = pf.filter(Q(nome_pf__icontains=q) | Q(CPF_CNPJ__icontains=q))
				pf.model_name = pf.model.__name__
				pj = pj.filter(Q(CPF_CNPJ__icontains=q) | Q(nome_fantasia__icontains=q))
				pj.model_name = pj.model.__name__
				queryset = list(chain(pf, pj))
		return queryset


	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super(FornecedorListView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(FornecedorListView, self).get_context_data(**kwargs)
		return context


# Definição de ListViews como views
painel_funcionarios = FuncListView.as_view()
painel_clientes = ClienteListView.as_view()
painel_fornecedores = FornecedorListView.as_view()
