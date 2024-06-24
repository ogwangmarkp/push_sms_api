"""kwani_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from systemrights import views as systemrights_views
from companies import views as companies_views
from users import views as user_views
from curriculum import views as curriculum_views
#from assets import views as asset_views
from smsApp import views as sms_app_views
from monitoring import views as monitoring_views
router = DefaultRouter() 

router.register(r'company-types', companies_views.CompanyTypesView, basename='CompanyTypes')
router.register(r'companies', companies_views.CompaniesView, basename='companies')

router.register(r'system-components',systemrights_views.SystemComponentsView, basename='system-components')
router.register(r'users', user_views.UserView, basename='users')
router.register(r'contacts', user_views.ContactsView, basename='contacts')
router.register(r'sms-apps', user_views.SMSAPIAppsView, basename='sms-apps')
router.register(r'user-groups',systemrights_views.UserGroupView, basename='user-groups')
router.register(r'branches', companies_views.CompanyBranchView, basename='branches')
router.register(r'sms-requests', sms_app_views.SmsRequestView, basename='sms-requests')
router.register(r'sms-list', sms_app_views.SMSListView, basename='send-sms')
router.register(r'contact-groups', sms_app_views.ContactGroupsView, basename='contact-groups')
router.register(r'file-list', sms_app_views.FileListView, basename='file-list')

router.register(r'unit-types', monitoring_views.UnitTypesView, basename='unit-types')
router.register(r'tracker-types', monitoring_views.TrackerTypesView, basename='tracker-types')
router.register(r'unit-groups', monitoring_views.UnitGroupsView, basename='unit-groups')
router.register(r'trackers', monitoring_views.TrackersView, basename='trackers')
router.register(r'sensor-types', monitoring_views.SensorTypesView, basename='sensor-types')
router.register(r'm-units', monitoring_views.MUnitsView, basename='m-units')
router.register(r'unit-sensors', monitoring_views.UnitSensorsView, basename='unit-sensors')

router.register(r'company-free-sms-award', sms_app_views.CompanyFreeSmsAwardView, basename='company-free-sms-award')
'''router.register(r'assets', asset_views.AssetView, basename='assets')
router.register(r'asset-trackers', asset_views.AssetTrackerView, basename='asset-trackers')
router.register(r'tracked-assets', asset_views.TrackedAssetView, basename='tracked-assets')'''


'''  router.register(r'courses', curriculum_views.CoursesViewSet, basename='course')
router.register(r'lessons', curriculum_views.LessonViewSet, basename='lesson')
router.register(r'topics', curriculum_views.TopicViewSet, basename='topic')
router.register(r'questions', curriculum_views.QuestionViewSet, basename='question')
'''

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token-auth/', user_views.RestAPIJWT.as_view()), 
    path('api/obtain-token/', user_views.ObtainAPITokenView.as_view()), 
    path('api/logout/', user_views.LogOutUserView.as_view()), 
    path('api/bulk-contact-updates/', user_views.BulkContactsUpdateApiView.as_view()), 
    path('api/system-rights/', systemrights_views.SystemRightView.as_view()),
    path('api/company-type-components/',systemrights_views.CompanyTypeComponentsView.as_view()),
    path('api/company-components/', systemrights_views.CompanyComponentView.as_view()),
    path('api/company-rights/', systemrights_views.CompanyRightsApiView.as_view()),
    path('api/group-rights/', systemrights_views.GroupRightsView.as_view()),
    path('api/company-general-settings/', companies_views.GeneralSettingsView.as_view()),
    path('api/switch-company/', companies_views.SwitchCompany.as_view()),
    #path('api/update_gps_location/',asset_views.UpdateLocationsView.as_view()),
    path('api/send-sms/', sms_app_views.SendSMSApiView.as_view()), 
    path('api/trash-update-orders/', sms_app_views.TrashUpdateOrdersApiView.as_view()), 
    
    path('api/assign-group-contacts/', sms_app_views.AssignGroupContactApiView.as_view()),
    path('api/send-bulk-sms/', sms_app_views.SendBulkSMSApiView.as_view()), 
    path('api/send-scheduled-sms/', sms_app_views.ScheduledSMSCronJobView.as_view()), 
    path('api/sms-dashboard/', sms_app_views.smsDashBoardView.as_view()), 
    path('api/document/', sms_app_views.DocumentApiView.as_view()), 
    path('api/download-file/', sms_app_views.DownloadApiView.as_view()),  
    path('',monitoring_views.GPSDataAPIView.as_view()),

]
