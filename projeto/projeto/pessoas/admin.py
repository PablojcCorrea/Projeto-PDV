from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from projeto.pessoas.models import Funcionario, Endereco, PessoaFisica, PessoaJuridica

class FuncionarioInline(admin.StackedInline):
	model = Funcionario
	can_delete = False
	verbose_name_plural = 'Funcionarios'

class EnderecoInline(admin.StackedInline):
	model = Endereco
	can_delete = False
	verbose_name_plural = 'Endereços'

class UserAdmin(BaseUserAdmin):
	inlines = (FuncionarioInline, )

class FuncionarioAdmin(admin.ModelAdmin):
	list_display = ['email', 'nome_pf', 'CPF_CNPJ']
	search_fields = ['nome_pf', 'email']
	inlines = (EnderecoInline, )

class EnderecoAdmin(admin.ModelAdmin):
	list_display = ['logradouro']

class PFAdmin(admin.ModelAdmin):
	list_display = ['nome_pf', 'sobrenome_pf', 'CPF_CNPJ']
	inlines = (EnderecoInline, )

class PJAdmin(admin.ModelAdmin):
	list_display = ['nome_fantasia', 'razao_social', 'CPF_CNPJ']
	inlines = (EnderecoInline, )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Funcionario, FuncionarioAdmin)
admin.site.register(Endereco, EnderecoAdmin)
admin.site.register(PessoaFisica, PFAdmin)
admin.site.register(PessoaJuridica, PJAdmin)

