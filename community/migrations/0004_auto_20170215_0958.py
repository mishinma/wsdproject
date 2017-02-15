# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-15 09:58
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0003_auto_20170214_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='rating',
            field=models.DecimalField(decimal_places=1, max_digits=2, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)]),
        ),
    ]