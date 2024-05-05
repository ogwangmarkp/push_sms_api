from rest_framework import serializers
from .models import *
from companies.models import CompanySetting

class SmsRequestSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    date_added = serializers.CharField(read_only=True)
    last_updated   = serializers.CharField(read_only=True)
    requested_by   = serializers.CharField(read_only=True)
    requested_by_name = serializers.SerializerMethodField()
    approved_by_name  = serializers.SerializerMethodField()
    company           = serializers.CharField(read_only=True)
    sms_count         = serializers.SerializerMethodField()

    def get_requested_by_name(self, obj):
        if obj.requested_by:
            return obj.requested_by.first_name
        return ""
    
    def get_approved_by_name(self, obj):
        if obj.approved_by:
            return obj.approved_by.first_name
        return ""

    def get_sms_count(self, obj):
        if obj.sms_cost > 0:
            if obj.status == 'approved':
                return round(obj.approved_amount/obj.sms_cost)
            else:
                return round(obj.requested_amount/obj.sms_cost)
        return 0
    
    class Meta:
        model = SmsRequest
        fields = '__all__'

class CompanyFreeSmsAwardSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name',read_only=True)
    added_by = serializers.CharField(read_only=True)
    updated_by = serializers.CharField(read_only=True)
    added_by_name  = serializers.CharField(source='added_by.first_name',read_only=True)
    sms_count      = serializers.SerializerMethodField()

    def get_sms_count(self, obj):
        if obj.sms_cost > 0:
            return round(obj.amount/obj.sms_cost)
        return 0
  
    class Meta:
        model = CompanyFreeSmsAward
        fields = '__all__'

class UserSmsSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    date_added = serializers.CharField(read_only=True)
    last_updated = serializers.CharField(read_only=True)
    sent_by      = serializers.CharField(read_only=True)
    recieved_by  = serializers.CharField(read_only=True)
    sent_by_name  = serializers.SerializerMethodField()
    recieved_by_name = serializers.SerializerMethodField()
    company = serializers.CharField(read_only=True)
    sms_cost = serializers.CharField(read_only=True)

    def sent_by_name(self, obj):
        return f'{obj.sent_by.first_name} {obj.sent_by.last_name}'
    
    def get_recieved_by_name(self, obj):
        return f'{obj.recieved_by.first_name} {obj.recieved_by.last_name}'
    

    class Meta:
        model = UserSms
        fields = '__all__'