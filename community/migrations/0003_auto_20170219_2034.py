# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-19 20:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0002_auto_20170219_2021'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='game',
            options={'ordering': ['-created'], 'permissions': (('play_game', 'Can play the game'), ('test_game', 'Can test games'), ('buy_game', 'Can buy games'))},
        ),
    ]
