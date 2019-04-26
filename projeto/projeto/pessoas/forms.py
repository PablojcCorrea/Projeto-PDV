from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import User

# Importação dos modelos necessários para gerar os formulários
from .models import Funcionario, Endereco, PessoaFisica, PessoaJuridica

# Formulários relacionadosio
class FormFuncionario(forms.ModelForm):
	password1 = forms.CharField(label='Senha',widget=forms.PasswordInput(attrs={'class' : 'w3-input'}))
	password2 = forms.CharField(label='Confirme a senha', widget=forms.PasswordInput(attrs={'class' : 'w3-input'}))

	class Meta:
		model = Funcionario
		fields = '__all__'
		exclude = ('tipo_pessoa', 'user', 'is_funcionario', 'is_fornecedor', 'is_empresa', 'is_cliente')

	def clean_email(self):
		email = self.cleaned_data.get('email')
		qs = Funcionario.objects.filter(email=email)
		if qs.exists():
			raise forms.ValidationError("E-mail já utilizado")
		return email

	def clean_password2(self):
		# Check that the two password entries match
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")

		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Senhas diferentes")
		return password2

	def save(self, **kwargs):
		funcionario = super().save(commit=False)
		user = User.objects.create(username=self.cleaned_data['email'])
		password = self.cleaned_data['password1']
		user.set_password(password)
		user.email = self.cleaned_data['email']
		user.save()
		funcionario.user = user
		funcionario.save()
		return funcionario

	def __init__(self, *args, **kwargs):
		super(FormFuncionario, self).__init__(*args, **kwargs)
		self.fields['nome_pf'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['CPF_CNPJ'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['CPF_CNPJ'].label = "CPF"
		self.fields['sobrenome_pf'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['telefone'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['email'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['documento'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['uf_documento'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['data_nascimento'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['tipo_funcionario'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['salario'].widget.attrs.update({'class' : 'w3-input'})


class FormEditaFuncionario(forms.ModelForm):
	class Meta:
		model = Funcionario
		fields = '__all__'
		exclude = ('tipo_pessoa', 'user', 'is_funcionario', 'is_fornecedor', 'is_empresa', 'is_cliente')

	def __init__(self, *args, **kwargs):
		super(FormEditaFuncionario, self).__init__(*args, **kwargs)
		self.fields['nome_pf'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['CPF_CNPJ'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['CPF_CNPJ'].label = "CPF"
		self.fields['sobrenome_pf'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['telefone'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['email'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['documento'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['uf_documento'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['data_nascimento'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['tipo_funcionario'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['salario'].widget.attrs.update({'class' : 'w3-input'})


# Fomulário para pessoa física (Funcionario ou Fornecedor)
class FormPessoaFisica(forms.ModelForm):
	class Meta:
		model = PessoaFisica
		fields = '__all__'
		exclude = ('CPF_CNPJ', 'email', 'telefone', 'is_funcionario', 'is_fornecedor', 'is_empresa', 'is_cliente')

	def __init__(self, *args, **kwargs):
		super(FormPessoaFisica, self).__init__(*args, **kwargs)
		self.fields['nome_pf'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['sobrenome_pf'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['documento'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['uf_documento'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['data_nascimento'].widget.attrs.update({'class' : 'w3-input'})

class FormEditaPessoaFisica(forms.ModelForm):
	class Meta:
		model = PessoaFisica
		fields = '__all__'
		exclude = ('is_funcionario', 'is_fornecedor', 'is_empresa', 'is_cliente')

	def __init__(self, *args, **kwargs):
		super(FormEditaPessoaFisica, self).__init__(*args, **kwargs)
		self.fields['nome_pf'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['sobrenome_pf'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['documento'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['uf_documento'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['data_nascimento'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['CPF_CNPJ'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['telefone'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['email'].widget.attrs.update({'class' : 'w3-input'})


# Formulário para pessoa jurídica (Funcionário ou Fornecedor)
class FormPessoaJuridica(forms.ModelForm):
	class Meta:
		model = PessoaJuridica
		fields = '__all__'
		exclude = ('CPF_CNPJ', 'email', 'telefone', 'is_funcionario', 'is_fornecedor', 'is_empresa', 'is_cliente')

	def __init__(self, *args, **kwargs):
		super(FormPessoaJuridica, self).__init__(*args, **kwargs)
		self.fields['razao_social'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['nome_fantasia'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['insc_estadual'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['contato'].widget.attrs.update({'class' : 'w3-input'})

class FormEmpresa(forms.ModelForm):
	class Meta:
		model = PessoaJuridica
		fields = '__all__'
		exclude = ('is_funcionario', 'is_fornecedor', 'is_empresa', 'is_cliente')

	def __init__(self, *args, **kwargs):
		super(FormEmpresa, self).__init__(*args, **kwargs)
		self.fields['razao_social'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['nome_fantasia'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['insc_estadual'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['contato'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['CPF_CNPJ'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['CPF_CNPJ'].label = "CNPJ"
		self.fields['telefone'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['email'].widget.attrs.update({'class' : 'w3-input'})

class FormEditaPessoaJuridica(forms.ModelForm):
	class Meta:
		model = PessoaJuridica
		fields = '__all__'
		exclude = ('is_funcionario', 'is_fornecedor', 'is_empresa', 'is_cliente')

	def __init__(self, *args, **kwargs):
		super(FormEditaPessoaJuridica, self).__init__(*args, **kwargs)
		self.fields['razao_social'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['nome_fantasia'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['insc_estadual'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['contato'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['CPF_CNPJ'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['CPF_CNPJ'].label = "CNPJ"
		self.fields['telefone'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['email'].widget.attrs.update({'class' : 'w3-input'})

# Formulário para Endereços
class FormEndereco(forms.ModelForm):
	
	class Meta:
		model = Endereco
		fields = '__all__'
		exclude = ('empresa', 'morador',)


	def __init__(self, *args, **kwargs):
		super(FormEndereco, self).__init__(*args, **kwargs)
		self.fields['logradouro'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['cidade'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['estado'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['cep'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['bairro'].widget.attrs.update({'class' : 'w3-input'})
		self.fields['numero'].widget.attrs.update({'class' : 'w3-input'})