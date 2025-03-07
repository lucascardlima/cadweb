# Generated by Django 4.2.16 on 2025-02-22 10:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_pagamento'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotaFiscal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chave_acesso', models.CharField(max_length=44, unique=True)),
                ('data_emissao', models.DateTimeField(auto_now_add=True)),
                ('total_pedido', models.DecimalField(decimal_places=2, max_digits=10)),
                ('icms', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ipi', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pis', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cofins', models.DecimalField(decimal_places=2, max_digits=10)),
                ('impostos_totais', models.DecimalField(decimal_places=2, max_digits=10)),
                ('valor_final', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pedido', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='home.pedido')),
            ],
        ),
    ]
