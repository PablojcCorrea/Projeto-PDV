# Generated by Django 2.0.3 on 2018-04-20 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pessoas', '0006_auto_20180420_0111'),
    ]

    operations = [
        migrations.AddField(
            model_name='pessoafisica',
            name='id',
            field=models.AutoField(auto_created=True, default=0, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pessoajuridica',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pessoafisica',
            name='CPF_CNPJ',
            field=models.CharField(max_length=18, unique=True, verbose_name='CPF/CNPJ'),
        ),
        migrations.AlterField(
            model_name='pessoajuridica',
            name='CPF_CNPJ',
            field=models.CharField(max_length=18, unique=True, verbose_name='CPF/CNPJ'),
        ),
    ]
