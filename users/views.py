
from django.shortcuts import render
from django.contrib.auth import logout,get_user_model,authenticate
from rest_framework.permissions import IsAuthenticated
from  users.serializers import *
from rest_framework import viewsets
from rest_framework.views import APIView
from users.models import * 
from users.helper import * 
from companies.models import * 
from rest_framework_jwt.views import ObtainJSONWebToken
from datetime import datetime 
from rest_framework.response import Response
from rest_framework import status
from kwani_api.utils import get_current_user,get_logged_in_user_key,generate_random_string
from django.db.models import Q
from rest_framework.permissions import AllowAny
from .permissions import *

class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        company_id = get_current_user(self.request, 'company_id', 1)
        staffid    = self.request.query_params.get('staffid')
        if staffid:
            queryset = User.objects.filter(user_branch__id=staffid).order_by('first_name')
        else:
            queryset = User.objects.filter(user_branch__company__id = company_id).all().order_by('first_name')
        return queryset
        
    def perform_create(self, serializer):
        branch_id  = self.request.data.get('user_branch')
        company_id = get_current_user(self.request, 'company_id', 1) 
        
        if not branch_id:
            branch_id = get_current_user(self.request, 'branch_id', 1) 
        
        branch     = CompanyBranch.objects.get(id=branch_id)
        company    = Company.objects.get(id=company_id)
        saved_user = serializer.save(user_branch = branch,user_added_by=self.request.user.id)
        if saved_user:
            password     = self.request.data.get('password')
            staff_number = self.request.data.get('staff_number')
            group_id      = self.request.data.get('group')
            saved_user.set_password(password)
            saved_user.save()
            staff_field={"user":saved_user,"staff_number":staff_number,"company":company}
            Staff.objects.create(**staff_field)
            
            ''' user_group = UserGroup.objects.get(id=group_id) 
            if user_group:
                user_assigned_group_field={"group":user_group,"assigned_by":self.request.user,"user":saved_user,"is_active":True}
                UserAssignedGroup.objects.create(**user_assigned_group_field) '''


    def perform_update(self, serializer):
        branchid     = self.request.data.get('user_branch')
        password     = self.request.data.get('password')
        staff_number = self.request.data.get('staff_number')

        saved_user = serializer.save(user_branch_id=branchid,user_added_by=self.request.user.id)
        # user_group  = UserGroup.objects.get(id=self.request.data.get('group'))
       # user_assigned_group = UserAssignedGroup.objects.filter(user=saved_user).first()
        
        staff = Staff.objects.filter(user=saved_user).first()
        if staff:
            staff.staff_number = staff_number
            staff.save()

        reset_password  = self.request.data.get('reset_password')
        if  saved_user and reset_password == True:
            saved_user.set_password(password)
            saved_user.save()
        
        ''' if user_assigned_group:
            user_assigned_group.user        = saved_user
            user_assigned_group.group       = user_group
            user_assigned_group.assigned_by = self.request.user
            user_assigned_group.save()
        else:
            user_assigned_group_field={"group":user_group,"assigned_by":self.request.user,"user":saved_user,"is_active":True}
            UserAssignedGroup.objects.create(**user_assigned_group_field) '''

class ContactsView(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        company_id = get_current_user(self.request, 'company_id', 1)
        search = self.request.query_params.get('search')
        phone_number = self.request.query_params.get('phone_number')
        
        if phone_number:
            return User.objects.filter(phone_number=phone_number,user_branch__company__id = company_id).all().order_by('first_name')
        
        if search:
            return User.objects.filter(Q(first_name__icontains=search) |  Q(last_name__icontains=search) | Q(phone_number__icontains=search),user_branch__company__id = company_id).all().order_by('first_name')
        queryset = User.objects.filter(user_branch__company__id = company_id).all().order_by('first_name')
        return queryset
        
    def perform_create(self, serializer):
        branch_id = get_current_user(self.request, 'branch_id', 1) 
        branch     = CompanyBranch.objects.get(id=branch_id)
        serializer.save(user_branch = branch,user_added_by=self.request.user.id)
        
    def perform_update(self, serializer):
        branchid     = self.request.data.get('branch_id')
        serializer.save(user_branch_id=branchid,user_added_by=self.request.user.id)
       
class RestAPIJWT(ObtainJSONWebToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return response
    
class LogOutUserView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user_sessions = UserSession.objects.filter(user=request.user)
        if user_sessions:
                for user_session in user_sessions:
                    if user_session.session_token == get_logged_in_user_key():
                        user_session.delete()
        logout(request) 
        return Response({"message":"successfully logged out"}, status=status.HTTP_200_OK)

class SMSAPIAppsView(viewsets.ModelViewSet):
    serializer_class = UserAPIAppSerializer

    def get_queryset(self):
        company_id = get_current_user(self.request, 'company_id', 1)
        search = self.request.query_params.get('search')
        if search:
            return UserAPIApp.objects.filter(Q(app_name__icontains=search),registered_by__user_branch__company__id = company_id).all().order_by('app_name')
        queryset = UserAPIApp.objects.filter(registered_by__user_branch__company__id = company_id).all().order_by('app_name')
        return queryset
        
    def perform_create(self, serializer):
        app_key = generate_random_string(30)
        serializer.save(app_key = app_key, registered_by = self.request.user)
        
    def perform_update(self, serializer):
        action  = self.request.data.get('action','update')
        if action == 'generate':
            app_key = generate_random_string(30)
            serializer.save(app_key = app_key)
        else:
            serializer.save()
       

class ObtainAPITokenView(APIView):
    permission_classes = [AllowAny, IsPostOnly]
    def post(self, request):
        api_key = request.data.get('api_key')
        user = None
        # Auth app
        user_api_app = UserAPIApp.objects.filter(app_key=api_key).first()
        if user_api_app:
            user = authenticate(username=user_api_app.registered_by.username, password=user_api_app.registered_by.username)
        
        if user is not None:
            # Generate JWT manually
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler  = api_settings.JWT_ENCODE_HANDLER
            payload             = jwt_payload_handler(user)
            access_token        = jwt_encode_handler(payload)
            UserSession.objects.create(user=user, session_token = access_token, data={"company_id":user.user_branch.company.id, "branch_id":user.user_branch.id})
            return Response({'message':'success','access_token': str(access_token)}, status=status.HTTP_200_OK)
        else:
            return Response({'message':'Invalid API key'}, status=status.HTTP_401_UNAUTHORIZED)