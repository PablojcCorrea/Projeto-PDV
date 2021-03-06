# Generated by Django 2.0.3 on 2018-05-29 01:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0003_produto_tamanho'),
        ('pessoas', '0012_auto_20180523_1527'),
        ('vendas', '0007_caixa_caixa_unico'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movimentacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor_movimentacao', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Valor')),
                ('descricao_movimentacao', models.TextField(max_length=150, verbose_name='Descrição')),
                ('horario_movimentacao', models.DateTimeField(auto_now_add=True)),
                ('tipo_movimentacao', models.CharField(choices=[('S', 'Sangria'), ('D', 'Despesa')], default='D', max_length=1, verbose_name='Tipo de Movimentação')),
                ('caixa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendas.Caixa')),
            ],
        ),
        migrations.CreateModel(
            name='Troca',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor_troca', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Valor')),
                ('motivo_troca', models.TextField(max_length=150, verbose_name='Motivo')),
                ('tem_defeito', models.BooleanField(default=False)),
                ('devolucao', models.BooleanField(default=False)),
                ('caixa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendas.Caixa')),
                ('produto_devolvido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='produto_devolvido', to='produtos.Produto')),
                ('produto_trocado', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='produto_trocado', to='pessoas.Funcionario')),
            ],
        ),
    ]
