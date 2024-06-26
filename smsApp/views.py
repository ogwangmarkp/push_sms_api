from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import  FileResponse, Http404
from rest_framework.permissions import AllowAny
from .helper import *
from kwani_api.utils import get_current_user
import threading
from users.permissions import *
from users.models import UserAPIApp
from .serializers import *
from .models import *
import os

class SmsRequestView(viewsets.ModelViewSet):
    serializer_class = SmsRequestSerializer

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
            query_filter['company__id'] = company_id
        return SmsRequest.objects.filter(**query_filter).order_by('-id')
    
    
    def perform_create(self, serializer):
        company_id = get_current_user(self.request, 'company_id', None)
        general_setting   = CompanySetting.objects.filter(company_setting__id=company_id,setting_key='sms_unit_cost').first()
        if general_setting:
            saved_request = serializer.save(company=Company.objects.filter(id=company_id).first(),requested_by=self.request.user,sms_cost = general_setting.setting_value)
            if saved_request:
                save_request_order(saved_request)
        else:
            saved_request = serializer.save(company=Company.objects.filter(id=company_id).first(),requested_by=self.request.user,sms_cost = 50)
            if saved_request:
                save_request_order(saved_request)

    
    def perform_update(self, serializer):
        saved_request = serializer.save()
        if saved_request:
            order = Order.objects.filter(ext_ref_no=saved_request.id,trans_type='sms-top-up').first()
            if order:
                order.status = saved_request.status
                order.save()
            else:
                order = Order.objects.create(status=saved_request.status,order_no=generate_invoice_no(saved_request.company.id),ext_ref_no=saved_request.id,company=saved_request.company,trans_type='sms-top-up', customer=saved_request.requested_by)
           
            if order:
                order_payment = OrderPayment.objects.filter(order=order).first()
                if not order_payment:
                    order_payment = OrderPayment.objects.create(payment_method=saved_request.payment_method,naration="Sms top up",amount=saved_request.approved_amount,ref_no=generate_ref_no(saved_request.company.id),order=order,added_by=saved_request.requested_by)
            
            if order_payment:
                order_payment.amount = saved_request.approved_amount
                order_payment.save()
                

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

    def get_queryset(self):
        company_id = get_current_user(self.request, 'company_id', None)
        start        = self.request.GET.get('s', None)
        end          = self.request.GET.get('e', None)
        query_filter = {"company__id":company_id}
        if start:
            query_filter['date_added__date__gte'] = start 
        if end:
            query_filter['date_added__date__lte'] = end 
        return UserSms.objects.filter(**query_filter).order_by('-id')

    def perform_create(self, serializer):
        company_id = get_current_user(self.request, 'company_id', None)
        company = Company.objects.filter(id=company_id).first()
        serializer.save(sent_by=self.request.user, company=company, sms_cost=company.sms_cost )

class ContactGroupsView(viewsets.ModelViewSet):
    serializer_class = ContactGroupSerializer

    def get_queryset(self):
        company_id = get_current_user(self.request, 'company_id', 1)
        search = self.request.query_params.get('search')

        if search:
            return ContactGroup.objects.filter(Q(name__icontains=search) |  Q(desc__icontains=search),company__id = company_id).all().order_by('name')
        queryset = ContactGroup.objects.filter(company__id = company_id).all().order_by('name')
        return queryset
        
    def perform_create(self, serializer):
        company_id = get_current_user(self.request, 'company_id', 1)
        serializer.save(added_by=self.request.user, company_id=company_id)

    def perform_update(self, serializer):
        serializer.save(last_added=timezone.now())

class SendSMSApiView(APIView):
    
    def post(self, request, format=None):
        recipients = self.request.data.get('recipients', None)  
        send_type  = self.request.data.get('send_type','api')         
        message    = self.request.data.get('message', None) 
        is_scheduled  = self.request.data.get('is_scheduled', False) 
        scheduled_time = self.request.data.get('scheduled_time', False) 

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
        send_bulk_sms = threading.Thread(target=sendSMSData, args=(recipients,message,is_scheduled,scheduled_time,self.request.user,send_type,))
        send_bulk_sms.start()
        return Response({"status":"success","message":"successful message"}, status=status.HTTP_200_OK)
    

class SendBulkSMSApiView(APIView):
    
    def post(self, request, format=None):
        recipients = self.request.data.get('recipients', None)  
        send_type  = self.request.data.get('send_type','api')         
        message    = self.request.data.get('message', None) 
        is_scheduled  = self.request.data.get('is_scheduled', False) 
        scheduled_time = self.request.data.get('scheduled_time', False) 

        if not recipients:
            return Response({"status":"failed","message":"Missing sms recipients"}, status=status.HTTP_200_OK)
        
        if not message:
            return Response({"status":"failed","message":"Missing message"}, status=status.HTTP_200_OK)
        
        balance = get_account_sms_balance(self.request.user.user_branch.company)

        sms_cost = 50
        general_setting   = CompanySetting.objects.filter(company_setting=self.request.user.user_branch.company,setting_key='sms_unit_cost').first()
        if general_setting:
             sms_cost = float(general_setting.setting_value)
        
        if balance == 0:
            return Response({"message":"Insufficient balance"}, status=status.HTTP_200_OK)

        if (len(recipients) * float(sms_cost)) > balance:
            return Response({"message":"Insufficient balance to send all messages"}, status=status.HTTP_200_OK) 
        send_bulk_sms = threading.Thread(target=sendBulkSMSData, args=(recipients,message,is_scheduled,scheduled_time,self.request.user,send_type,))
        send_bulk_sms.start()
        return Response({"status":"success","message":"successful message"}, status=status.HTTP_200_OK)
    
class AssignGroupContactApiView(APIView):
    
    def post(self, request, format=None):
        recipients = self.request.data.get('contacts', None)  
        group_id = self.request.data.get('group', None) 
        if not recipients:
            return Response({"status":"failed","message":"No contacts"}, status=status.HTTP_200_OK)
        
        if len(recipients) < 1:
            return Response({"status":"failed","message":"contacts"}, status=status.HTTP_200_OK)
        
        send_bulk_sms = threading.Thread(target=bulk_group_contacts_update, args=(group_id,recipients,self.request.user,))
        send_bulk_sms.start()
        return Response({"status":"success","message":"successful message"}, status=status.HTTP_200_OK)

class ScheduledSMSCronJobView(APIView):
    permission_classes = [AllowAny, IsPostOnly]
    
    def post(self, request, format=None):

        send_bulk_sms = threading.Thread(target=send_schuduled_sms, args=())
        send_bulk_sms.start()

        return Response({"message":"Cron initiated successfully"})

class TrashUpdateOrdersApiView(APIView):
    permission_classes = [AllowAny, IsPostOnly]
    
    def post(self, request, format=None):
        bulk_orders = threading.Thread(target=trash_update_orders, args=())
        bulk_orders.start()

        return Response({"message":"Orders updated successfully"})
    

class smsDashBoardView(APIView):
    def get(self, request, format=None):
        company_id = get_current_user(self.request, 'company_id', None)
        end          = self.request.GET.get('e',None)
        start        =  self.request.GET.get('s',None)
        sms_summary  = {}

        purchases_filter  = {"company__id": company_id,"status":"approved"}
        free_sms_filter   = {"company__id": company_id}
        used_filter       = {"company__id": company_id,"status":"sent"}
        purchases_bf_filter  = {"company__id": company_id,"status":"approved"}
        used_bf_filter       = {"company__id": company_id,"status":"sent"}
        free_bf_sms_filter   = {"company__id": company_id}

        if start:
            purchases_bf_filter['date_added__date__lt'] = start
            purchases_filter['date_added__date__gte']   = start
            free_sms_filter['date_added__date__gte']    = start
            free_bf_sms_filter['date_added__date__lt']  = start
            used_filter['date_added__date__gte']        = start
            used_bf_filter['date_added__date__lt']      = start
        if end:
            purchases_filter['date_added__date__lte']  = end
            free_sms_filter['date_added__date__lte']   = end
            used_filter['date_added__date__lte']       = end
      
        purchases   = SmsRequest.objects.filter(**purchases_filter).aggregate(total_sum=Sum('approved_amount'))['total_sum']
        if not purchases:
            purchases = 0

        purchases_bf = SmsRequest.objects.filter(**purchases_bf_filter).aggregate(total_sum=Sum('approved_amount'))['total_sum']
        if not purchases_bf:
            purchases_bf = 0

        free_sms  = CompanyFreeSmsAward.objects.filter(**free_sms_filter).aggregate(total_sum=Sum('amount'))['total_sum']
        if not free_sms:
            free_sms = 0

        free_bf_sms  = CompanyFreeSmsAward.objects.filter(**free_bf_sms_filter).aggregate(total_sum=Sum('amount'))['total_sum']
        if not free_bf_sms:
            free_bf_sms = 0
            
        used_sms  = UserSms.objects.filter(**used_filter).aggregate(total_sum=Sum('sms_cost'))['total_sum']
        if not used_sms:
            used_sms = 0

        used_bf_sms  = UserSms.objects.filter(**used_bf_filter).aggregate(total_sum=Sum('sms_cost'))['total_sum']
        if not used_bf_sms:
            used_bf_sms = 0

        sms_summary["purchases"] = purchases
        sms_summary["free_sms"] = free_sms
        sms_summary["used_sms"] = used_sms
        sms_summary["remaining"] = (purchases + purchases_bf + free_sms + free_bf_sms) - (used_sms + used_bf_sms)
        
        if sms_summary["remaining"] < 0:
            sms_summary["remaining"] = 0

        sms_summary["purchases"] = purchases + free_sms

        return Response(sms_summary, status=status.HTTP_200_OK)


class FileListView(viewsets.ModelViewSet):
    serializer_class = FileObjectSerializer

    def get_queryset(self):
        user = get_user_model().objects.get(pk=self.request.user.id)
        return FileObject.objects.filter(user=user).order_by('-id')


class DocumentApiView(APIView):
    permission_classes = [AllowAny, IsPostOnly]
    def post(self, request, format=None):
        files = request.FILES.getlist('files')
        #pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        directory_path = settings.FILE_UPLOAD_DIR + f'/files/'
        output_path2 = 'munites.pdf'
        output_path3 = 'munites_final.pdf'
        
        image_paths = []

        if not os.path.exists(directory_path):
                os.makedirs(directory_path, exist_ok=True)

        
        for uploaded_file in files:
            file_path = directory_path + uploaded_file.name
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
                    image_paths.append(uploaded_file.name)
        
        if len(image_paths) > 0:
            image_to_string(directory_path,image_paths,self.request.user) 
        #insert_html_at_position(directory_path,output_path2,output_path3,'The Chairperson thanked members for coming', 'hello world',self.request.user)
        
        return Response({"status":"success","message":"successful message"}, status=status.HTTP_200_OK)
    
class DownloadApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        try:
            id = self.request.GET.get('id', None)  
            directory_path = settings.FILE_UPLOAD_DIR + f'/files/'
            file_obj  = FileObject.objects.filter(id=id).first()
            if file_obj:
                file_path = directory_path + file_obj.title
                response = FileResponse(open(file_path, 'rb'))
                response['Content-Disposition'] = f'attachment; filename="{file_obj.title}"'
                return response
        except:
            raise Http404("File not found")

class SendSMSAPIV2View(APIView):
    
    permission_classes = [AllowAny]

    def get(self, request, format=None):
            return Response({}, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        access_key = self.request.GET.get('access_key', None)  
        recipients = self.request.GET.get('numbers', None)  
        send_type  = 'api'         
        message    = ''
        is_scheduled  = False 
        scheduled_time = False
        user_app_api = UserAPIApp.objects.filter(app_key = access_key).first()
        
        if request.data.items():
            for key, value in request.data.items():
                message = f"{key}={value}"

        if not user_app_api:
            return Response({"status":"failed","message":"Invalid access key"}, status=status.HTTP_200_OK)
        
        if not recipients:
            return Response({"status":"failed","message":"Missing sms recipients"}, status=status.HTTP_200_OK)
        
        if not message:
            return Response({"status":"failed","message":"Missing message"}, status=status.HTTP_200_OK)
       
        recipients = recipients.split(',')
        user = user_app_api.registered_by

        directory_path = settings.FILE_UPLOAD_DIR + f'/files/'
        filename = f'{directory_path}output.txt'
        with open(filename, 'a') as file:
            file.write(message+ "\n")

        balance = get_account_sms_balance(user.user_branch.company)

        sms_cost = 50
        general_setting   = CompanySetting.objects.filter(company_setting=user.user_branch.company,setting_key='sms_unit_cost').first()
        if general_setting:
             sms_cost = float(general_setting.setting_value)
        
        if balance == 0:
            return Response({"message":"Insufficient balance"}, status=status.HTTP_200_OK)

        if (len(recipients) * float(sms_cost)) > balance:
            return Response({"message":"Insufficient balance to send all messages"}, status=status.HTTP_200_OK) 
        
        send_bulk_sms = threading.Thread(target=sendSMSData, args=(recipients,message,is_scheduled,scheduled_time,user,send_type,))
        send_bulk_sms.start()
        return Response({"status":"success","message":"successful message"}, status=status.HTTP_200_OK)
    