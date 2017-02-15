# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-15 15:47
from __future__ import unicode_literals

from django.db import migrations
from django.contrib.auth.models import Group, Permission


def extend_group_permissions(apps, schema_editor):

    # Developer
    group = Group.objects.get(name='developer')
    group.permissions.add(
        Permission.objects.get(codename='test_game'),
    )

    # Player
    group = Group.objects.get(name='player')
    group.permissions.add(
        Permission.objects.get(codename='buy_game'),
    )


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_usermethods')
    ]

    operations = [
        migrations.RunPython(extend_group_permissions)
    ]
