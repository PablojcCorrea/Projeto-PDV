# Generated by Django 2.0.3 on 2018-04-25 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pessoas', '0008_auto_20180420_1839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pessoafisica',
            name='uf_documento',
            field=models.CharField(default='SSP/SP', max_length=6, verbose_name='UF'),
        ),
    ]
