# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-01-18 22:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masterdata', '0004_auto_20190119_0606'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='no',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
