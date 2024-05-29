from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .helper import *
from kwani_api.utils import get_current_user
import threading

from .serializers import SmsRequestSerializer, UserSmsSerializer, CompanyFreeSmsAwardSerializer
from .models import *

class SmsRequestView(viewsets.ModelViewSet):
    serializer_class = SmsRequestSerializer
    queryset = SmsRequest.objects.all()
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend, )
    filterset_fields = ['id', 'status']
    search_fields = ('id')
    ordering_fields = ['id', ]
    
    def get_queryset(self):
        process_type = self.request.GET.get('process_type', None)
        status       = self.request.GET.get('status', None)
        start        = self.request.GET.get('s', None)
        end          = self.request.GET.get('e', None)
        query_filter = {}
        if start:
            query_filter['date_added__date__gte'] = start 
        if end:
            query_filter['date_added__date__lte'] = end 
        if status:
            query_filter['status'] = status
        if process_type == 'fetch-single':
            company_id = get_current_user(self.request, 'company_id', None)
            query_filter['company_id__id'] = company_id
        return SmsRequest.objects.filter(**query_filter).order_by('-id')
    
    def perform_create(self, serializer):
        company_id = get_current_user(self.request, 'company_id', None)
        general_setting   = CompanySetting.objects.filter(company_setting__id=company_id,setting_key='sms_unit_cost').first()
        if general_setting:
            serializer.save(company=Company.objects.filter(id=company_id).first(),requested_by=self.request.user,sms_cost = general_setting.setting_value)
        else:
            serializer.save(company=Company.objects.filter(id=company_id).first(),requested_by=self.request.user,sms_cost = 50)

class CompanyFreeSmsAwardView(viewsets.ModelViewSet):
    serializer_class = CompanyFreeSmsAwardSerializer
    
    def get_queryset(self):
        status       = self.request.GET.get('status', None)
        company_id   = self.request.GET.get('company', None)
        start        = self.request.GET.get('s', None)
        end          = self.request.GET.get('e', None)
        
        query_filter = {}
        
        if company_id:
            query_filter['company__id'] = company_id 
        
        if start:
            query_filter['date_added__date__gte'] = start 
        
        if end:
            query_filter['date_added__date__lte'] = end 
        
        if status:
            query_filter['status'] = status 
        
        return CompanyFreeSmsAward.objects.filter(**query_filter).order_by('-id')
    
    def perform_create(self, serializer):
        company_id = self.request.data.get('company', None)  
        if company_id:
            general_setting = CompanySetting.objects.filter(company_setting__id=company_id,setting_key='sms_unit_cost').first()
            if general_setting:
                serializer.save(added_by=self.request.user,sms_cost = general_setting.setting_value)
            else:
                serializer.save(added_by=self.request.user,sms_cost = 50)

# Create your views here.
class SMSListView(viewsets.ModelViewSet):
    serializer_class = UserSmsSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend, )
    filterset_fields = ['id', 'sending_mode']
    search_fields = ('id')
    ordering_fields = ['id', ]

    def get_queryset(self):
        user = get_user_model().objects.get(pk=self.request.user.id)
        return UserSms.objects.filter(company=user.user_branch.company).order_by('-id')

    def perform_create(self, serializer):
        company = get_user_model().objects.get(pk=self.request.user.id)
        serializer.save(sent_by=self.request.user, company=company.company, sms_cost=company.company.sms_cost )

class SendSMSApiView(APIView):
    
    def post(self, request, format=None):
        recipients = self.request.data.get('recipients', None)  
        send_type  = self.request.data.get('send_type','api')         
        message    = self.request.data.get('message', None) 
        
        if not recipients:
            return Response({"status":"failed","message":"Missing sms recipients"}, status=status.HTTP_200_OK)
        
        if not message:
            return Response({"status":"failed","message":"Missing message"}, status=status.HTTP_200_OK)
       
        recipients = recipients.split(',')
        
        balance = get_account_sms_balance(self.request.user.user_branch.company)

        sms_cost = 50
        general_setting   = CompanySetting.objects.filter(company_setting=self.request.user.user_branch.company,setting_key='sms_unit_cost').first()
        if general_setting:
             sms_cost = float(general_setting.setting_value)
        
        if balance == 0:
            return Response({"message":"Insufficient balance"}, status=status.HTTP_200_OK)

        if (len(recipients) * float(sms_cost)) > balance:
            return Response({"message":"Insufficient balance to send all messages"}, status=status.HTTP_200_OK) 
        send_bulk_sms = threading.Thread(target=sendSMSData, args=(recipients,message,self.request.user,send_type,))
        send_bulk_sms.start()
        return Response({"status":"success","message":"successful message"}, status=status.HTTP_200_OK)
    




