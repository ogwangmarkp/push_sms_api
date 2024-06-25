from django.db import models
from django.utils import timezone
from companies.models import *
from django.conf import settings
# Create your models here.


class UnitType(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 related_name='unit_type_added_by', null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='unit_type_updated_by', null=True, blank=True)
    # company       =  models.ForeignKey(Company, on_delete=models.CASCADE, related_name='unit_company')
    date_added = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(null=True)

    class Meta:
        db_table = 'public\".\"unit_type'


class UnitTypeField(models.Model):
    label = models.CharField(max_length=255)
    value = models.CharField(max_length=255, null=True, blank=True)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 related_name='unit_type_field_added_by', null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='unit_type_field_updated_by', null=True, blank=True)
    unit_type = models.ForeignKey(
        UnitType, on_delete=models.CASCADE, related_name='unit_type_field_type')
    date_added = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(null=True)

    class Meta:
        db_table = 'public\".\"unit_type_field'


class UnitGroup(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 related_name='unit_group_added_by', null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='unit_group_updated_by', null=True, blank=True)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='unit_group_company')
    date_added = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(null=True)

    class Meta:
        db_table = 'public\".\"unit_group'


class MUnit(models.Model):
    label = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    server_addr = models.CharField(max_length=255)
    server_port = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    unit_no = models.CharField(max_length=255,null=True, blank=True)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 related_name='m_unit_added_by', null=True, blank=True)
    user_account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='m_unit_user_account', null=True, blank=True)
    
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='m_unit_company')
    unit_type = models.ForeignKey(
        UnitType, on_delete=models.CASCADE, related_name='m_unit_unit_type')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='m_unit_updated_by', null=True, blank=True)
    date_added = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(null=True)

    class Meta:
        db_table = 'public\".\"m_unit'


class TrackerType(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 related_name='tracker_type_added_by', null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='tracker_type_updated_by', null=True, blank=True)
    date_added = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(null=True)

    class Meta:
        db_table = 'public\".\"tracker_type'


class SensorType(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 related_name='sensor_type_added_by', null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='sensor_type_updated_by', null=True, blank=True)
    date_added = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(null=True)

    class Meta:
        db_table = 'public\".\"sensor_type'


class UnitSensor(models.Model):
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    is_last_message = models.BooleanField(default=False)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 related_name='unit_sensor_added_by', null=True, blank=True)
    sensor_type = models.ForeignKey(
        SensorType, on_delete=models.CASCADE, related_name='unit_sensor_type')
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='unit_sensor_company')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='unit_sensor_updated_by', null=True, blank=True)
    date_added = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(null=True)

    class Meta:
        db_table = 'public\".\"unit_sensor'


class UnitTracker(models.Model):
    label = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 related_name='unit_tracker_added_by', null=True, blank=True)
    tracker_type = models.ForeignKey(
        TrackerType, on_delete=models.CASCADE, related_name='unit_tracker_type')
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='unit_tracker_company')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='unit_tracker_updated_by', null=True, blank=True)
    date_added = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(null=True)

    class Meta:
        db_table = 'public\".\"unit_tracker'


class TrackedUnit(models.Model):
    unit = models.OneToOneField(
        MUnit, on_delete=models.CASCADE, related_name='tracked_unit_unit')
    tracker = models.OneToOneField(
        UnitTracker, on_delete=models.CASCADE, related_name='tracked_unit_unit_tracker')
    status = models.BooleanField(default=False)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 related_name='tracked_unit_added_by', null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='tracked_unit_updated_by', null=True, blank=True)
    date_added = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(null=True)

    class Meta:
        db_table = 'public\".\"tracked_unit'


class GPSData(models.Model):
    assigned_unit = models.ForeignKey(
        TrackedUnit, on_delete=models.CASCADE, related_name='gps_tracked_unit')
    latitude = models.FloatField()
    longitude = models.FloatField()
    speed = models.FloatField()
    date_added = models.DateTimeField(default=timezone.now)


class NotificationType(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    type_added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='not_type_added_by', null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='not_type_updated_by', null=True, blank=True)
    date_added = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(null=True)

    class Meta:
        db_table = 'public\".\"notification_type'


class Notification(models.Model):
    message = models.TextField()
    status = models.BooleanField(default=False)
    assigned_unit = models.ForeignKey(
        TrackedUnit, on_delete=models.CASCADE, related_name='tracked_unit_tracker')
    notification_type = models.ForeignKey(
        NotificationType, on_delete=models.CASCADE, related_name='tracked_unit_not_type')
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 related_name='tracked_unit_not_added_by', null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='tracked_unit_not_updated_by', null=True, blank=True)
    date_added = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(null=True)

    class Meta:
        db_table = 'public\".\"notification'


class NotificationSubscriber(models.Model):
    message = models.TextField()
    user_email = models.TextField(null=True)
    send_sms = models.BooleanField(default=False)
    send_eamil = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    notification = models.ForeignKey(
        Notification, on_delete=models.CASCADE, related_name='tracked_unit_sub_notification')
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='tracked_unit_sub_subscriber', null=True, blank=True)

    class Meta:
        db_table = 'public\".\"notification_subscriber'
