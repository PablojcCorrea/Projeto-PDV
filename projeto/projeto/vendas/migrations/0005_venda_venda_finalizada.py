# Generated by Django 2.0.3 on 2018-05-27 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendas', '0004_auto_20180523_1943'),
    ]

    operations = [
        migrations.AddField(
            model_name='venda',
            name='venda_finalizada',
            field=models.BooleanField(default=False, verbose_name='Venda finalizada?'),
        ),
    ]
