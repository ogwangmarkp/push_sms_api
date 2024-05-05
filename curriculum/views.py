import companies
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from kwani_api.utils import get_current_user
import json
from django.http import Http404
from companies.models import *

class CourseCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CourseCategorySerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend, )
    filterset_fields = ['title']
    search_fields = ('title' )
    ordering_fields = ['title']
    
    def get_queryset(self):
        organisation_id = get_current_user(self.request, 'organisation_id', None) 
        return CourseCategory.objects.filter(organisation=Organisation.objects.get(pk=organisation_id)).order_by('title')
    
    def perform_create(self, serializer):
        organisation_id = get_current_user(self.request, 'organisation_id', None) 
        organisation   = Organisation.objects.get(pk=organisation_id)
        serializer.save(organisation=organisation)


class CoursesViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend, )
    filterset_fields = ['title']
    search_fields = ('title' )
    ordering_fields = ['title']

    def get_queryset(self):
        organisation_id = get_current_user(self.request, 'organisation_id', None) 
        return Course.objects.filter(organisation=Organisation.objects.get(pk=organisation_id) ).order_by('title')

    def perform_create(self, serializer):
        organisation_id = get_current_user(self.request, 'organisation_id', None) 
        organisation   = Organisation.objects.get(pk=organisation_id)
        serializer.save(added_by=self.request.user,organisation=organisation)
        
class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend, )
    filterset_fields = ['title','course']
    search_fields = ('title','course' )
    ordering_fields = ['title','course']

    def get_queryset(self):
        organisation_id = get_current_user(self.request, 'organisation_id', None) 
        return Lesson.objects.filter(organisation=Organisation.objects.get(pk=organisation_id) ).order_by('title')
    
    def perform_create(self, serializer):
        organisation_id = get_current_user(self.request, 'organisation_id', None) 
        organisation    = Organisation.objects.get(pk=organisation_id)
        serializer.save(added_by=self.request.user,organisation=organisation)
       

class TopicViewSet(viewsets.ModelViewSet):
    serializer_class = TopicSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend, )
    filterset_fields = ['title']
    search_fields = ('title' )
    ordering_fields = ['title']

    def get_queryset(self):
        return Topic.objects.all().order_by('title')
    
    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)

class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend, )
    filterset_fields = ['title']
    search_fields = ('title' )
    ordering_fields = ['title']

    def get_queryset(self):
        return Question.objects.all().order_by('title')
    
    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)
       

