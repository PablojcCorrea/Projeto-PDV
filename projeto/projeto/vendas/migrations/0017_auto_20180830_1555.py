# Generated by Django 2.0.3 on 2018-08-30 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendas', '0016_despesa_data_pagamento_despesa'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimentacao',
            name='dia',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='venda',
            name='dia',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
