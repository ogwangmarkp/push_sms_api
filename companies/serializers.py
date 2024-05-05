
from rest_framework import serializers
from companies.models import *

class CompanyTypeSerializer(serializers.ModelSerializer):
    
    def __str__(self):
        return self.company_type 
     
    class Meta:
        model = CompanyType
        fields = '__all__'

class CompanyBranchSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    date_added = serializers.DateTimeField(read_only=True)
    added_by = serializers.IntegerField(read_only=True)
    branch_organisation = serializers.PrimaryKeyRelatedField(read_only=True, required=False)
    
    class Meta:
        model = CompanyBranch
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    date_added = serializers.DateTimeField(read_only=True)
    added_by   = serializers.IntegerField(read_only=True)
    company_type = CompanyTypeSerializer(read_only=True)
    company_branches = CompanyBranchSerializer(many=True, read_only=True)
    company_rights_count = serializers.SerializerMethodField()
    
    def get_company_rights_count(self, obj):
        return 0
    
    class Meta:
        model = Company
        fields = '__all__' 
        
class CompanySettingSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    date_added = serializers.DateTimeField(read_only=True)
    setting_added_by = serializers.CharField(read_only=True)
    company_setting = serializers.CharField(read_only=True)

    class Meta:
        model = CompanySetting
        fields = '__all__'

