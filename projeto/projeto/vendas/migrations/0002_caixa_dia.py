# Generated by Django 2.0.3 on 2018-05-23 20:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('vendas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='caixa',
            name='dia',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]