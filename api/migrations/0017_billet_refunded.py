# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-16 15:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_auto_20180115_1603'),
    ]

    operations = [
        migrations.AddField(
            model_name='billet',
            name='refunded',
            field=models.BooleanField(default=False),
        ),
    ]