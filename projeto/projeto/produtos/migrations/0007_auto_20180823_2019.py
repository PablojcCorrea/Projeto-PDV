# Generated by Django 2.0.3 on 2018-08-23 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0006_auto_20180601_1907'),
    ]

    operations = [
        migrations.AddField(
            model_name='aquisicao',
            name='data_pagamento',
            field=models.DateField(blank=True, null=True, verbose_name='Data de pagamento'),
        ),
        migrations.AddField(
            model_name='aquisicao',
            name='porcentagem_lucro',
            field=models.DecimalField(decimal_places=2, default=100, max_digits=8, verbose_name='Porcentagem de Lucro'),
        ),
        migrations.AddField(
            model_name='aquisicao',
            name='preco_custo',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Preço de custo'),
        ),
        migrations.AddField(
            model_name='aquisicao',
            name='preco_venda',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Preço de venda'),
        ),
        migrations.AddField(
            model_name='aquisicao',
            name='valor_total_aquisicao',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Valor total da aquisição'),
        ),
        migrations.AddField(
            model_name='produto',
            name='porcentagem_lucro',
            field=models.DecimalField(decimal_places=2, default=100, max_digits=8, verbose_name='Porcentagem de Lucro'),
        ),
    ]