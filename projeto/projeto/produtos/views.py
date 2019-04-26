from django.shortcuts import render, redirect, get_object_or_404

# bibliotecas e aplicações necessárias para criar listviews.
import operator
from django.db.models import Q
from django.views.generic import ListView

# Decorator do django para requisição de login
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Ferramenta para união de duas tabelas diferentes
from itertools import chain

# Importação dos modelos e formulários
from .models import Produto, Categoria, Aquisicao
from projeto.pessoas.models import Funcionario
from .forms import FormProduto, FormCategoria, FormAquisicao

# Create your views here.
@login_required
def nova_categoria(request):
	if request.method == 'POST':
		form = FormCategoria(request.POST, request.FILES)
		if form.is_valid():
			form.save()

	form = FormCategoria()

	template_name = 'nova_categoria.html'
	context = {
		'form': form,
	}

	return render(request, template_name, context)

@login_required
def edita_categoria(request, pk):
	instance = get_object_or_404(Categoria, id=pk)

	form = FormCategoria(request.POST or None, instance=instance)
	if form.is_valid():
		cetegoria = form.save(commit=False)
		if request.method == 'POST':
			categoria.save()
			return redirect(painel_produtos)

	template_name = 'edita_categoria.html'
	context = {
		'form': form,
	}

	return render(request, template_name, context)



class CatListView(ListView):
	template_name = 'categorias.html'
	paginate_by = 10

	def get_queryset(self):
		queryset = Categoria.objects.all()
		query = self.request.GET.get('q')
		if query:
			queryset = Categoria.objects.all()
			query_list = query.split()
			querysets = queryset
			for q in query_list:
				queryset = queryset.filter(Q(nome_categoria__icontains=q) | Q(descricao_categoria__icontains=q))
		
		return queryset

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super(CatListView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(CatListView, self).get_context_data(**kwargs)
		return context


# Views de produtos
@login_required
def novo_produto(request):
	if request.method == 'POST':
		form = FormProduto(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			

	form = FormProduto()

	template_name = 'novo_produto.html'
	context = {
		'form': form,
	}

	return render(request, template_name, context)

@login_required
def edita_produto(request, pk):
	instance = get_object_or_404(Produto, id=pk)

	form = FormProduto(request.POST or None, instance=instance)
	if form.is_valid():
		produto = form.save(commit=False)
		if request.method == 'POST':
			produto.save()
			return redirect(painel_produtos)

	template_name = 'edita_produto.html'
	context = {
		'form': form,
	}

	return render(request, template_name, context)

class ProdListView(ListView):
	template_name = 'produtos.html'
	paginate_by = 10

	def get_queryset(self):
		queryset = Produto.objects.all()
		query = self.request.GET.get('q')
		if query:
			queryset = Produto.objects.all()
			query_list = query.split()
			querysets = queryset
			for q in query_list:
				queryset = queryset.filter(Q(nome_produto__icontains=q) | Q(descricao_produto__icontains=q))
		
		return queryset

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super(ProdListView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(ProdListView, self).get_context_data(**kwargs)
		return context

@login_required
def reposicao(request, pk):
	produto = Produto.objects.filter(pk=pk)
	form = FormAquisicao(request.POST, request.FILES)
	if request.method == 'POST':
		form = FormAquisicao(request.POST, request.FILES)
		if form.is_valid():
			aquisicao = form.save(commit=False)
			funcionario = Funcionario.objects.filter(user=request.user)
			aquisicao.funcionario = funcionario[0]
			aquisicao.produto_adquirido = produto[0]

			qtd = aquisicao.quantidade_produto
			qtd_produto = produto[0].quantidade
			prod = Produto(pk=pk)
			prod.preco_custo = aquisicao.preco_custo
			prod.preco_venda = aquisicao.preco_venda
			prod.porcentagem_lucro = aquisicao.porcentagem_lucro
			prod.quantidade = qtd + qtd_produto
			prod.save(update_fields=['quantidade', 'preco_venda', 'preco_custo', 'porcentagem_lucro'])
			aquisicao.save()

			return redirect('index')

	form = FormAquisicao()
	template_name = "aumenta_quantidade.html"
	context = {
		'produto': produto,
		'form': form
	}
	return render(request, template_name, context)

painel_categorias = CatListView.as_view()
painel_produtos = ProdListView.as_view()
