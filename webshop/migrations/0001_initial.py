# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-17 09:22
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('community', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Gift',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(blank=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PendingTransaction',
            fields=[
                ('pid', models.IntegerField(primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(999.0)])),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='community.Game')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='community.Game')),
                ('gift', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webshop.Gift')),
                ('payer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('pid', models.IntegerField(primary_key=True, serialize=False)),
                ('ref', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(999.0)])),
                ('result', models.CharField(max_length=10)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='purchase',
            name='transaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webshop.Transaction'),
        ),
    ]
