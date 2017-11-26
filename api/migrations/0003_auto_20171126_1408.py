# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-26 13:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_lien_billet_option'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billet',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='billets', to='api.Product'),
        ),
    ]
