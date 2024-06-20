# Create your models here.
from django.db import models
from companies.models import Company, CompanyBranch
from django.conf import settings
from django.utils import timezone
from users.models import User


class SmsRequest(models.Model):

    PAYMENT_OPTIONS = (
        ('mm', 'Mobile Money'),
        ('bank', 'Bank'),
        ('cash', 'Cash'),
    )

    SMS_STATUSES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('canceled', 'Canceled'),
    )

    requested_amount = models.FloatField()
    approved_amount = models.FloatField(default=0)
    sms_cost = models.FloatField(default=0.0)
    status = models.CharField(
        max_length=50, choices=SMS_STATUSES, default='pending')
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='company_sms_purchase')
    payment_method = models.CharField(
        max_length=255, choices=PAYMENT_OPTIONS, default='cash')
    requested_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='requester', blank=False, null=False)
    approved_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='approver', blank=True, null=True)
    date_added = models.DateTimeField(default=timezone.now)
    last_added = models.DateTimeField(default=timezone.now)
    comment = models.CharField(max_length=255, blank=True, null=True)
    reason = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'public\".\"sms_request'


class CompanyFreeSmsAward(models.Model):
    SMS_STATUSES = (
        ('approved', 'Approved'),
        ('canceled', 'Canceled'),
    )
    sms_cost = models.FloatField(default=0.0)
    status = models.CharField(
        max_length=50, choices=SMS_STATUSES, default='approved')
    company = models.ForeignKey(Company, on_delete=models.CASCADE,
                                related_name='free_sms_company', blank=False, null=False)
    heading = models.TextField(null=False, blank=False, default=False)
    reason = models.CharField(max_length=255, blank=True, null=True)
    amount = models.FloatField()
    added_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name='company_free_sms_added_by', blank=False, null=False)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='company_free_sms_last_updated_by', blank=True, null=True)
    date_added = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'public\".\"company_free_sms_award'


class UserSms(models.Model):
    sms_cost = models.FloatField(default=0.0)
    message = models.CharField(max_length=5555)
    provider = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    sending_mode = models.CharField(max_length=50, default='api')
    status = models.CharField(max_length=50, default='pending')
    is_scheduled = models.BooleanField(default=False)
    scheduled_time = models.DateTimeField(default=timezone.now)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='company_user_sms')
    sent_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sms_sent_by')
    recieved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recieved_by')
    date_added = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'public\".\"user_sms'

# for all roles belonging to an company.


class ContactGroup(models.Model):
    name = models.CharField(max_length=255)
    desc = models.TextField(blank=True)
    deleted = models.CharField(max_length=5, default='0')
    date_added = models.DateTimeField(default=timezone.now)
    last_added = models.DateTimeField(default=timezone.now)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contact_group_added_by')
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='contact_group_company')

    class Meta:
        db_table = 'public\".\"contact_group'


class ContactAssignedGroup(models.Model):
    contact_group = models.ForeignKey(
        ContactGroup, on_delete=models.CASCADE, related_name='contact_assigned_group_group')
    contact = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='contact_assigned_group_contact')
    date_added = models.DateTimeField(default=timezone.now)
    last_added = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contact_assigned_group_added_by')

    class Meta:
        db_table = 'public\".\"contact_assigned_group'


class FileObject(models.Model):
    FILE_TyPE = (('image-to-text', 'image-to-text'),
                 ('text-to-doc', 'text-to-doc')
                 )
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    url_path = models.TextField()
    attachment_type = models.CharField(
        max_length=255, choices=FILE_TyPE, default='pending')
    sign_status = models.CharField(
        max_length=255, default='pending')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='doc_user')
    date_added = models.DateTimeField(default=timezone.now)
    tran_doc_id = models.TextField(blank=True, null=True)
    sign_doc_id = models.TextField(blank=True, null=True)
    signed_doc_url = models.TextField(blank=True, null=True)
    is_signing = models.BooleanField(default=False)

    class Meta:
        db_table = 'public\".\"file_object'
