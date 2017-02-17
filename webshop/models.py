from __future__ import unicode_literals
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from hashlib import md5
from community.models import Game
from django.contrib.auth.models import User
import time


class TransactionManager(models.Manager):

    def create_from_pending(self, pending_transaction, ref, result):
        finished_transaction = Transaction(
            user=pending_transaction.user,
            pid=pending_transaction.pid,
            ref=ref,
            amount=pending_transaction.amount,
            result=result
        )
        finished_transaction.save()
        PendingTransaction.objects.get(pid=pending_transaction.pid).delete()
        purchase = None
        if result == 'success':
            purchase = Purchase.objects.create(pid=finished_transaction,
                                               payer=finished_transaction.user,
                                               game=pending_transaction.game)
        return finished_transaction, purchase


class Transaction(models.Model):
    # Should the length be fixed?
    pid = models.fields.CharField(max_length=100, primary_key=True)
    user = models.ForeignKey(User)
    ref = models.fields.CharField(max_length=100)
    amount = models.fields.DecimalField(max_digits=5,
                                        decimal_places=2,
                                        validators=[MinValueValidator(0.0),
                                                    MaxValueValidator(999.00)])
    result = models.fields.CharField(max_length=10)
    timestamp = models.DateTimeField(default=timezone.now)

    objects = TransactionManager()

    @staticmethod
    def generate_new_pid(game, user):
        return '{}{}{}'.format(game.id, user.username, int(time.time()))

    @staticmethod
    def generate_checksum(pid, sid, amount, token):
        checksum_str = "pid={}&sid={}&amount={}&token={}".format(pid, sid, amount, token)
        return md5(checksum_str.encode('ascii')).hexdigest()

    @staticmethod
    def validate_received_checksum(checksum, pid, ref, result, token):
        checksum_str = "pid={}&ref={}&result={}&token={}".format(pid, ref, result, token)
        checksum_computed = md5(checksum_str.encode('ascii')).hexdigest()
        return checksum_computed == checksum


class Gift(models.Model):
    receiver = models.ForeignKey(User)
    message = models.fields.TextField(blank=True)


class Purchase(models.Model):
    transaction = models.ForeignKey(Transaction)
    payer = models.ForeignKey(User)
    game = models.ForeignKey(Game)
    gift = models.ForeignKey(Gift, null=True, blank=True)


class PendingTransaction(models.Model):
    user = models.ForeignKey(User)
    pid = models.fields.CharField(max_length=100, primary_key=True)
    game = models.ForeignKey(Game)
    amount = models.fields.DecimalField(max_digits=5,
                                        decimal_places=2,
                                        validators=[MinValueValidator(0.0),
                                                    MaxValueValidator(999.00)])
    timestamp = models.DateTimeField(default=timezone.now)
