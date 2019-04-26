from django.db import models
from django.contrib.auth.models import User

class Pessoa(models.Model):
	is_funcionario = models.BooleanField("Funcionário?", default=False)
	is_empresa = models.BooleanField("Empresa?", default=False)
	is_fornecedor = models.BooleanField("Fornecedor?", default=False)
	is_cliente = models.BooleanField("Cliente?", default=False)

	CPF_CNPJ = models.CharField("CPF/CNPJ", max_length=18, unique=True)
	telefone = models.CharField("Telefone/Celular", max_length=15)
	email = models.CharField("E-mail", max_length=70, unique=True)

	class Meta:
		abstract = True


class PessoaFisica(Pessoa):
	nome_pf = models.CharField("Nome", max_length=30)
	sobrenome_pf = models.CharField("Sobrenome", max_length=30)
	documento = models.CharField("R.G.", max_length=15)
	uf_documento = models.CharField("UF", max_length=6, default='SSP/SP')
	data_nascimento = models.DateField('Data de Nascimento', blank=True)


class PessoaJuridica(Pessoa):
	razao_social = models.CharField("Razão Social", max_length=80)
	nome_fantasia = models.CharField("Nome Fantasia", max_length=80)
	insc_estadual = models.CharField("Inscrição Estadual", max_length=15, null=True, blank=True)
	contato = models.CharField("Pessoa para Contato", max_length=60)

	logo = models.ImageField(
		upload_to='projeto/core/static/media', verbose_name='Logo da Empresa',
		null=True, blank=True,
		)

	def __str__(self):
		return '%s' % self.razao_social


class Endereco(models.Model):
	logradouro = models.CharField("Logradouro", max_length=50)
	numero = models.CharField("Número", max_length=6)
	bairro = models.CharField("Bairro", max_length=30)
	estado = models.CharField("Estado", max_length=30)
	cidade = models.CharField("Cidade", max_length=30)
	cep = models.CharField("CEP", max_length=10)
	morador = models.OneToOneField(
		PessoaFisica, 
		on_delete=models.CASCADE,
		null=True,
		blank=True
	)
	empresa = models.OneToOneField(
		PessoaJuridica, 
		on_delete=models.CASCADE,
		null=True,
		blank=True
	)

class Funcionario(PessoaFisica):
	user = models.OneToOneField(
		User, 
		on_delete=models.CASCADE
	)

	salario = models.DecimalField('Salário', decimal_places=2, default=0, max_digits=8)

	GERENTE = 'GER'
	ESTOQUISTA = 'EST'
	VENDEDOR = 'VEN'
	TIPO_FUNCIONARIO = (
		(GERENTE, 'Gerente'),
		(ESTOQUISTA, 'Estoquista'),
		(VENDEDOR, 'Vendedor'),
		)

	tipo_funcionario = models.CharField('Tipo de Funcionário', max_length=3, choices=TIPO_FUNCIONARIO,default=VENDEDOR)
