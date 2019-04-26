# Generated by Django 2.0.3 on 2018-04-24 01:28

from django.db import migrations, models
import django.db.models.deletion
import projeto.produtos.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pessoas', '0008_auto_20180420_1839'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_categoria', models.CharField(max_length=50, verbose_name='Categoria')),
                ('descricao_categoria', models.TextField(max_length=150, verbose_name='Descrição')),
            ],
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_produto', models.CharField(max_length=60, verbose_name='Produto')),
                ('descricao_produto', models.TextField(max_length=150, verbose_name='Descrição')),
                ('quantidade', models.IntegerField(verbose_name='Quantidade')),
                ('estoque_minimo', models.IntegerField(verbose_name='Estoque mínimo')),
                ('preco_custo', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Preço de custo')),
                ('preco_venda', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Preço de venda')),
                ('categoria', models.ForeignKey(on_delete=projeto.produtos.models.Categoria, to='produtos.Categoria')),
                ('fornecedor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pessoas.PessoaJuridica')),
            ],
        ),
    ]
