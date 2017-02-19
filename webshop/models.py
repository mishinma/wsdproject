from __future__ import unicode_literals

from collections import OrderedDict
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from hashlib import md5

from django.db import models
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth, Coalesce
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.utils import timezone

from community.models import Game
from haze.settings import PAYMENT_SID, PAYMENT_SECRET_KEY


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
        pending_transaction.delete()
        purchase = None
        if result == 'success':
            purchase = Purchase.objects.create(transaction=finished_transaction,
                                               payer=finished_transaction.user,
                                               game=pending_transaction.game)
        return finished_transaction, purchase


class Transaction(models.Model):
    # Should the length be fixed?
    pid = models.fields.IntegerField(primary_key=True)
    user = models.ForeignKey(User)
    ref = models.fields.CharField(max_length=100)
    amount = models.fields.DecimalField(max_digits=5,
                                        decimal_places=2,
                                        validators=[MinValueValidator(0.0),
                                                    MaxValueValidator(999.00)])
    result = models.fields.CharField(max_length=10)
    timestamp = models.DateTimeField(default=timezone.now)

    objects = TransactionManager()


class Gift(models.Model):
    receiver = models.ForeignKey(User)
    message = models.fields.TextField(blank=True)


class PurchaseManager(models.Manager):

    def get_stats_purchases_per_month(self, developer):
        """ Returns number of purchases per month for all games of the developer """

        # By default take data for the last 6 months

        time_now = timezone.now()
        num_months_back = 6

        first_month = time_now + relativedelta(months=-num_months_back)
        first_month = first_month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        months = [(first_month + relativedelta(months=i)).strftime("%B")
                    for i in range(num_months_back+1)]  # format as month
        sales_stats = OrderedDict.fromkeys(months, 0)

        qry = super(PurchaseManager, self).get_queryset().\
            filter(game__developer=developer).\
            filter(transaction__timestamp__date__gte= first_month).\
            annotate(month=TruncMonth('transaction__timestamp')).values('month').\
            annotate(num_purchases=Count('id'))

        for entry in qry:
            sales_stats[entry['month'].strftime("%B")] = entry['num_purchases']

        return sales_stats

    def get_stats_revenue_per_game(self, developer):

        qry = Game.objects.filter(developer=developer).\
            annotate(revenue=Coalesce(Sum('purchase__transaction__amount'), 0)).\
            order_by('revenue')

        revenue_stats = OrderedDict()
        for game in qry:
            revenue_stats[game.name] = game.revenue

        return revenue_stats

class Purchase(models.Model):
    transaction = models.ForeignKey(Transaction)
    payer = models.ForeignKey(User)
    game = models.ForeignKey(Game)
    gift = models.ForeignKey(Gift, null=True, blank=True)
    objects = PurchaseManager()


class PendingTransactionManager(models.Manager):

    def create_new_pending(self, user, game):
        """ Create new pending transaction and compute checksum """
        amount = game.get_price()
        new_pt = PendingTransaction.objects.create(user=user, game=game, amount=amount)
        checksum = new_pt.generate_checksum()
        new_pt.checksum = checksum
        return new_pt


class PendingTransaction(models.Model):
    pid = models.fields.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    game = models.ForeignKey(Game)
    amount = models.fields.DecimalField(max_digits=5,
                                        decimal_places=2,
                                        validators=[MinValueValidator(0.0),
                                                    MaxValueValidator(999.00)])
    timestamp = models.DateTimeField(default=timezone.now)

    objects = PendingTransactionManager()

    def generate_checksum(self):
        checksum_str = "pid={}&sid={}&amount={}&token={}".format(
            self.pid, PAYMENT_SID, self.amount, PAYMENT_SECRET_KEY)
        return md5(checksum_str.encode('ascii')).hexdigest()

    def validate_checksum(self, checksum, ref, result):
        checksum_str = "pid={}&ref={}&result={}&token={}".format(
            self.pid, ref, result, PAYMENT_SECRET_KEY)
        checksum_computed = md5(checksum_str.encode('ascii')).hexdigest()
        return checksum_computed == checksum
