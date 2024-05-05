from django.db import models
from django.utils import timezone
from companies.models import *
from django.conf import settings
# Create your models here.

class Asset(models.Model):
    label       = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    asset_no    = models.CharField(max_length=255)
    added_by    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='asset_added_by', null=True, blank=True)
    company     =  models.ForeignKey(Company, on_delete=models.CASCADE, related_name='asset_company')
    updated_by  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='asset_updated_by', null=True, blank=True)
    date_added  = models.DateTimeField(default = timezone.now)
    last_updated = models.DateTimeField(null=True)

    class Meta:
        db_table = 'public\".\"asset'

class AssetTracker(models.Model):
    label = models.CharField(max_length=255)
    code  = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    added_by     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='asset_tracker_added_by', null=True, blank=True)
    company      =  models.ForeignKey(Company, on_delete=models.CASCADE, related_name='asset_tracker_company')
    updated_by   = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='asset_tracker_updated_by', null=True, blank=True)
    date_added   = models.DateTimeField(default = timezone.now)
    last_updated = models.DateTimeField(null=True)
    
    class Meta:
        db_table = 'public\".\"asset_tracker'

class TrackedAsset(models.Model):
    asset        = models.OneToOneField(Asset,on_delete=models.CASCADE, related_name='tracked_asset_asset')
    tracker      = models.OneToOneField(Asset,on_delete=models.CASCADE, related_name='tracked_asset_asset_tracker')
    status       = models.BooleanField(default=False)
    added_by     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tracked_asset_added_by', null=True, blank=True)
    updated_by   = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tracked_asset_updated_by', null=True, blank=True)
    date_added   = models.DateTimeField(default = timezone.now)
    last_updated = models.DateTimeField(null=True)
    
    class Meta:
        db_table = 'public\".\"tracked_asset'

class GPSData(models.Model):
    assigned_tracker = models.ForeignKey(TrackedAsset,on_delete=models.CASCADE, related_name='gps_tracked_asset')
    latitude   = models.FloatField()
    longitude  = models.FloatField()
    speed      = models.FloatField()
    date_added = models.DateTimeField(default = timezone.now)

class NotificationType(models.Model):
    title         = models.CharField(max_length=255)
    description   = models.CharField(max_length=255, null=True, blank=True)
    type_added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='not_type_added_by', null=True, blank=True)
    updated_by    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='not_type_updated_by', null=True, blank=True)
    date_added    = models.DateTimeField(default = timezone.now)
    last_updated  = models.DateTimeField(null=True)
    
    class Meta:
        db_table = 'public\".\"notification_type'

class Notification(models.Model):
    message = models.TextField()
    status  = models.BooleanField(default=False)
    assigned_tracker  = models.ForeignKey(TrackedAsset,on_delete=models.CASCADE, related_name='tracked_asset_tracker')
    notification_type = models.ForeignKey(NotificationType,on_delete=models.CASCADE, related_name='tracked_asset_not_type')
    added_by     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='not_added_by', null=True, blank=True)
    updated_by   = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='not_updated_by', null=True, blank=True)
    date_added   = models.DateTimeField(default = timezone.now)
    last_updated = models.DateTimeField(null=True)
    
    class Meta:
        db_table = 'public\".\"notification'

class NotificationSubscriber(models.Model):
    message      = models.TextField()
    user_email   = models.TextField(null=True)
    send_sms     =  models.BooleanField(default=False)
    send_eamil   =  models.BooleanField(default=False)
    status       = models.BooleanField(default=False)
    notification = models.ForeignKey(Notification,on_delete=models.CASCADE, related_name='not_sub_notification')
    subscriber   = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='not_sub_subscriber', null=True, blank=True)
    
    class Meta:
        db_table = 'public\".\"notification_subscriber' 