from rest_framework import serializers
from .models import *
from kwani_api.utils import get_current_user

class CourseCategorySerializer(serializers.ModelSerializer):
    organisation = serializers.CharField(read_only=True)
    class Meta:
        model = CourseCategory
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    organisation = serializers.CharField(read_only=True)
    class Meta:
        model = Course
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    organisation = serializers.CharField(read_only=True)
    course_name   = serializers.CharField(read_only=True, source="course.title")
    class Meta:
        model = Lesson
        fields = '__all__'

class TopicSerializer(serializers.ModelSerializer):
    course        = serializers.CharField(read_only=True, source="lesson.course.id")
    lesson_name   = serializers.CharField(read_only=True, source="lesson.title")
    
    class Meta:
        model = Topic
        fields = '__all__'

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, required=False)
    class Meta:
        model = Question
        fields = '__all__'


