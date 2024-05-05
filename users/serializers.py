from django.contrib.auth import get_user_model
from rest_framework import serializers
from users.models import *

class StaffSerializer(serializers.ModelSerializer):
    staff_number       = serializers.CharField(required=False)
    staff_added_by     = serializers.CharField(required=False,read_only=True)
    staff_organisation = serializers.CharField(required=False,read_only=True)
    picture_url        = serializers.ImageField(required=False)
    user               = serializers.CharField(required=False,read_only=True)
    class Meta:
        model = Staff
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    user_branch   = serializers.CharField(required=False,read_only=True)
    password      = serializers.CharField(required=False,read_only=True)
    branch_id     = serializers.CharField(required=False,read_only=True,source="user_branch.id")
    group         = serializers.SerializerMethodField()
    group_name    = serializers.SerializerMethodField()
    staff_number  = serializers.SerializerMethodField()

    def get_group(self, obj):
        user_assinged_group = UserAssignedGroup.objects.filter(user=obj).first()
        if user_assinged_group:
            return user_assinged_group.group.id
        return ""
    
    def get_group_name(self, obj):
        user_assinged_group = UserAssignedGroup.objects.filter(user=obj).first()
        if user_assinged_group:
            return user_assinged_group.group.name
        return ""
    
    def get_staff_number(self, obj):
        staff = Staff.objects.filter(user=obj).first()
        if staff:
            return staff.staff_number
        return ""
    
    class Meta:
        model = User
        fields = '__all__'

class UserAssignedGroupSerializer(serializers.ModelSerializer):
    assigned_role_added_by =  serializers.CharField(required=False,read_only=True)
    assigned_role  = serializers.CharField(read_only=True, source="assigned_role.id")
    role_name      = serializers.CharField(read_only=True, source="assigned_role.role_name")
    class Meta:
        model = UserAssignedGroup
        fields = '__all__'

class GetFullUserSerializer(serializers.ModelSerializer):
#     user_system_role = UserSystemRolesSerializer(read_only=True, many=True)
      name  = serializers.SerializerMethodField()

      def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
        
      class Meta:
         model = get_user_model()
         fields = ('id','username','is_superuser','is_active','name')

class UserPermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPermissions
        fields = '__all__'

class UserAPIAppSerializer(serializers.ModelSerializer):
    app_key       = serializers.CharField(read_only=True)
    registered_by = serializers.CharField(read_only=True)

    class Meta:
        model = UserAPIApp
        fields = '__all__'

