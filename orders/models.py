from django.db import models
from unicodedata import name
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from companies.models import *
from django.contrib.postgres.fields import JSONField
from companies.models import *
from systemrights.models import *

# Create your models here.


class Order(models.Model):
    order_no = models.CharField(max_length=255)
    trans_type = models.CharField(max_length=255)
    ext_ref_no = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default='pending')
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='order_company')
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='order_customer')
    date_added = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'public\".\"order'


class OrderPayment(models.Model):
    amount = models.FloatField(default=0.0)
    order_no = models.CharField(max_length=255)
    pay_type = models.CharField(max_length=255, default='normal')
    payment_method = models.CharField(max_length=255, default='normal')
    ref_no = models.CharField(max_length=255)
    naration = models.CharField(max_length=255)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order_payment_order')
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='order_payment_added_by')
    date_added = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'public\".\"order_payment'
