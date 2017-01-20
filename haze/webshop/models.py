from __future__ import unicode_literals
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone

from community.models import Player, Game


class Transaction(models.Model):
    # Should the length be fixed?
    pid = models.fields.CharField(max_length=100, primary_key=True)
    ref = models.fields.CharField(max_length=100)
    amount = models.fields.DecimalField(max_digits=5,
                                        decimal_places=2,
                                        validators=[MinValueValidator(0.0)])
    result = models.fields.CharField(max_length=10)
    timestamp = models.DateTimeField(default=timezone.now)


class Gift(models.Model):
    gift_id = models.AutoField(primary_key=True)
    receiver = models.ForeignKey(Player)
    message = models.fields.TextField(blank=True)


class Purchase(models.Model):
    purchase_id = models.AutoField(primary_key=True)
    pid = models.ForeignKey(Transaction)
    payer = models.ForeignKey(Player)
    game = models.ForeignKey(Game)
    gift_id = models.ForeignKey(Gift, null=True)
