from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from kwani_api.utils import get_current_user
from .models import *
from .serializers import *


class UnitTypesView(viewsets.ModelViewSet):
    serializer_class = UnitTypeSerializer
    queryset = UnitType.objects.all().order_by('-id')

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)


class UnitTypeFieldsView(viewsets.ModelViewSet):
    serializer_class = UnitTypeFieldSerializer
    queryset = UnitTypeField.objects.all().order_by('id')

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)


class TrackerTypesView(viewsets.ModelViewSet):
    serializer_class = TrackerTypeSerializer
    queryset = TrackerType.objects.all().order_by('-id')

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)


class SensorTypesView(viewsets.ModelViewSet):
    serializer_class = SensorTypeSerializer
    queryset = SensorType.objects.all().order_by('-id')

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)


class UnitGroupsView(viewsets.ModelViewSet):
    serializer_class = UnitGroupSerializer

    def get_queryset(self):
        query_filter = {}
        company_id = get_current_user(self.request, 'company_id', None)
        if company_id:
            query_filter['company__id'] = company_id
        return UnitGroup.objects.filter(**query_filter).order_by('-id')
    
    def perform_create(self, serializer):
        company_id = get_current_user(self.request, 'company_id', None)
        serializer.save(company=Company.objects.filter(id=company_id).first(),added_by=self.request.user)


class TrackersView(viewsets.ModelViewSet):
    serializer_class = UnitTrackerSerializer

    def get_queryset(self):
        query_filter = {}
        company_id = get_current_user(self.request, 'company_id', None)
        if company_id:
            query_filter['company__id'] = company_id
        return UnitTracker.objects.filter(**query_filter).order_by('-id')
    
    def perform_create(self, serializer):
        company_id = get_current_user(self.request, 'company_id', None)
        serializer.save(company=Company.objects.filter(id=company_id).first(),added_by=self.request.user)

class MUnitsView(viewsets.ModelViewSet):
    serializer_class = MUnitSerializer

    def get_queryset(self):
        query_filter = {}
        company_id = get_current_user(self.request, 'company_id', None)
        if company_id:
            query_filter['company__id'] = company_id
        return MUnit.objects.filter(**query_filter).order_by('-id')
    
    def perform_create(self, serializer):
        company_id = get_current_user(self.request, 'company_id', None)
        serializer.save(company=Company.objects.filter(id=company_id).first(),added_by=self.request.user)

class UnitSensorsView(viewsets.ModelViewSet):
    serializer_class = UnitSensorSerializer

    def get_queryset(self):
        query_filter = {}
        company_id = get_current_user(self.request, 'company_id', None)
        if company_id:
            query_filter['company__id'] = company_id
        return UnitSensor.objects.filter(**query_filter).order_by('-id')
    
    def perform_create(self, serializer):
        company_id = get_current_user(self.request, 'company_id', None)
        serializer.save(company=Company.objects.filter(id=company_id).first(),added_by=self.request.user)


class GPSDataAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, format=None):
        print("post request-----------------------------")
        print("self.request.data --- raw_data\n",self.request.data)
        return Response({"message":" initiated successfully"})
    
    def get(self,request, format=None):
        print("get request-----------------------------")
        print("self.request.data ----- --- raw_data\n",self.request.data)
        return Response({"message":" initiated successfully"})
    
'''
class AssetView(viewsets.ModelViewSet):
    serializer_class = AssetSerializer

    def get_queryset(self):
        query_filter = {}
        company_id = get_current_user(self.request, 'company_id', None)
        if company_id:
            query_filter['company__id'] = company_id
        return Asset.objects.filter(**query_filter).order_by('-id')
    
    def perform_create(self, serializer):
        company_id = get_current_user(self.request, 'company_id', None)
        serializer.save(company=Company.objects.filter(id=company_id).first(),added_by=self.request.user)

class AssetTrackerView(viewsets.ModelViewSet):
    serializer_class = AssetTrackerSerializer
    def get_queryset(self):
        query_filter = {}
        company_id = get_current_user(self.request, 'company_id', None)
        if company_id:
            query_filter['company__id'] = company_id
        return AssetTracker.objects.filter(**query_filter).order_by('-id')
    
    def perform_create(self, serializer):
        company_id = get_current_user(self.request, 'company_id', None)
        serializer.save(company=Company.objects.filter(id=company_id).first(),added_by=self.request.user)

class TrackedAssetView(viewsets.ModelViewSet):
    serializer_class = TrackedAssetSerializer
    def get_queryset(self):
        query_filter = {}
        company_id = get_current_user(self.request, 'company_id', None)
        if company_id:
            query_filter['tracker__company__id'] = company_id
        return TrackedAsset.objects.filter(**query_filter).order_by('-id')
    
    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)



class UpdateLocationsView(APIView):
    
    def post(self, request):
        request_data = request.data
        asset_id     = request_data.get('asset_id')
        latitude     = request_data.get('latitude')
        longitude    = request_data.get('longitude')
        speed        = request_data.get('speed')

        # Save the data to the database
        asset = Asset.objects.get(id=asset_id)
        GPSData.objects.create(asset=asset, latitude=latitude, longitude=longitude, speed=speed)

        return Response({'status': 'success'}, status=status.HTTP_400_BAD_REQUEST)
'''   

       