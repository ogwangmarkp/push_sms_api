from rest_framework import serializers
from .models import *


class UnitTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = UnitType
        fields = '__all__'


class UnitTypeFieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = UnitTypeField
        fields = '__all__'


class TrackerTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrackerType
        fields = '__all__'


class UnitGroupSerializer(serializers.ModelSerializer):
    company = serializers.CharField(read_only=True)

    class Meta:
        model = UnitGroup
        fields = '__all__'


class UnitTrackerSerializer(serializers.ModelSerializer):
    company = serializers.CharField(read_only=True)

    class Meta:
        model = UnitTracker
        fields = '__all__'


class SensorTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = SensorType
        fields = '__all__'


'''
class AssetSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    added_by     = serializers.CharField(read_only=True)
    added_by_name  = serializers.CharField(read_only=True)
    company      = serializers.CharField(read_only=True)
    company_name = serializers.CharField(read_only=True,source="company.name")
    
    def get_added_by_name(self, obj):
        if obj.added_by:
            return f'{obj.added_by.first_name} {obj.added_by.last_name}'
        return ""
    
    class Meta:
        model = Asset
        fields = '__all__'

class AssetTrackerSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    added_by     = serializers.CharField(read_only=True)
    added_by_name  = serializers.CharField(read_only=True)
    company      = serializers.CharField(read_only=True)
    company_name = serializers.CharField(read_only=True,source="company.name")
    
    def get_added_by_name(self, obj):
        if obj.added_by:
            return f'{obj.added_by.first_name} {obj.added_by.last_name}'
        return ""
    
    class Meta:
        model = AssetTracker
        fields = '__all__'

class TrackedAssetSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    added_by      = serializers.CharField(read_only=True)
    added_by_name = serializers.CharField(read_only=True)
    asset_label   = serializers.CharField(read_only=True,source="asset.label")
    tracker_code  = serializers.CharField(read_only=True,source="tracker.code")
    
    def get_added_by_name(self, obj):
        if obj.tracker.added_by:
            return f'{obj.tracker.added_by.first_name} {obj.tracker.added_by.last_name}'
        return ""
    
    class Meta:
        model = TrackedAsset
        fields = '__all__'
'''