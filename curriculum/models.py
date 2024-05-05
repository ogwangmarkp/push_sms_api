from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.utils import timezone
from django.conf import settings
from companies.models import *
from users.models import Staff

class CourseCategory(models.Model):
    title =  models.CharField(max_length=100)
    description =  models.TextField()
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='course_category_added_by', null=True, blank=True)
    company_branch  =  models.ForeignKey(CompanyBranch, on_delete=models.CASCADE, related_name='course_category_company_branch')
   
    class Meta:
        unique_together = ('title','company_branch')
        db_table = 'public\".\"course_category'

class Course(models.Model):
    SHOW_MATERIAL = (
        ('always', 'Always Visible'),
        ('only_enrolled', 'Only Enrolled Users')
    )
    ACCESS_MODE = (
        ('open', 'Open'),
        ('free', 'Free'),
         ('buy', 'Buy Now')
    )
    title              =  models.CharField(max_length=100)
    content            =  models.TextField(default='', null=True, blank=True)
    material           =  models.TextField(default='', null=True, blank=True)
    is_content         = models.BooleanField(default=False)
    course_price       =  models.FloatField(default=0.0)
    course_period      =  models.IntegerField(default=0)
    prerequisites      =  models.CharField(max_length=100,default='',null=True, blank=True) # list of courses before starting
    delete_data_on_exp =  models.BooleanField(default=False)
    access_mode        = models.CharField(max_length=100,choices=ACCESS_MODE,default='buy')
    show_material      = models.CharField(max_length=100,choices=SHOW_MATERIAL,default='only_enrolled')
    show_certificate   = models.BooleanField(default=False)
    is_section         = models.BooleanField(default=False)
    date_added         = models.DateTimeField(default = timezone.now)
    added_by           = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='course_added_by', null=True, blank=True)
    company_branch     =  models.ForeignKey(CompanyBranch, on_delete=models.CASCADE, related_name='course_company_branch')
    course_category    =  models.ForeignKey(CourseCategory, on_delete=models.CASCADE, related_name='course_course_category', null=True, blank=True)
    class Meta:
        unique_together = ('title','company_branch')
        db_table = 'public\".\"course'

class CourseSection(models.Model):
    title =  models.CharField(max_length=100)
    course =  models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_section_course', null=True, blank=True)
    class Meta:
        db_table = 'public\".\"course_section'

class Lesson(models.Model):
    title         =  models.CharField(max_length=100)
    content       =  models.TextField( null=True, blank=True,default='')
    is_sample     =  models.BooleanField(default=False)
    show_material =  models.BooleanField(default=False)
    material      =  models.TextField(default='',null=True, blank=True)
    course        =  models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lesson_course', null=False, blank=False)
    company_branch  =  models.ForeignKey(CompanyBranch, on_delete=models.CASCADE, related_name='lesson_company_branch')
    date_added    = models.DateTimeField(default = timezone.now)
    added_by      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lesson_added_by', null=True, blank=True)
    class Meta:
        db_table = 'public\".\"lesson'

class CourseLesson(models.Model):
    title     =  models.CharField(max_length=100)
    content   =  models.TextField()
    is_sample = models.BooleanField(default=False)
    added_by  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='course_lesson_added_by', null=True, blank=True)
    lesson    =  models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='assigned_lesson', null=False, blank=False)
    course    =  models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assigned_course', null=False, blank=False)
    class Meta:
        db_table = 'public\".\"course_lesson'

class Topic(models.Model):
    title         =  models.CharField(max_length=100)
    content       =  models.TextField(default='',null=True, blank=True)
    show_material =  models.BooleanField(default=False)
    material      =  models.TextField(default='',null=True, blank=True)
    date_added    = models.DateTimeField(default = timezone.now)
    added_by      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='topic_added_by', null=True, blank=True)
    lesson        =  models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='topic_lesson', null=True, blank=True)
    class Meta:
        db_table = 'public\".\"topic'

class QuestionCategory(models.Model):
    title =  models.CharField(max_length=100)
    description    =  models.TextField()
    date_added     = models.DateTimeField(default = timezone.now)
    added_by       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='question_category_added_by', null=True, blank=True)
    company_branch =  models.ForeignKey(CompanyBranch, on_delete=models.CASCADE, related_name='question_category_company_branch')
   
    class Meta:
        db_table = 'public\".\"question_category'

class Question(models.Model):
    POINTS_TYPES = (
        ('points_for_question', 'Points for question'),
        ('points_for_answer', 'Points for answer')
    )
    QUESTION_TYPES = (
        ('single_choice', 'Single choice'),
        ('multiple_choice', 'Multiple choice'),
        ('free_choice', 'Free choice'),
        ('sorting_choice', 'Sorting choice'),
        ('matrix_sorting_choice', 'Matrix sorting choice'),
        ('fill_blank', 'Fill in the blank'),
        ('assessment', 'Assessment (survey)'),
        ('essay', 'Essay (open answer)')
    )
    title             =  models.CharField(max_length=100)
    content           =  models.TextField()
    explain_correct   =  models.TextField()
    explain_incorrect =  models.TextField()
    hint              =  models.TextField()
    is_hint           =  models.BooleanField(default=False)
    is_explain        =  models.BooleanField(default=False)
    question_type     =  models.CharField(max_length=100,choices=QUESTION_TYPES)
    points_type       =  models.CharField(max_length=100,choices=POINTS_TYPES)
    points            =  models.IntegerField(null=True, blank=True)
    show_points       =  models.BooleanField(default=False)
    correct_answer    = models.CharField(max_length=100)
    date_added        = models.DateTimeField(default = timezone.now)
    added_by          = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='question_added_by', null=True, blank=True)
    course            =  models.ForeignKey(Course, on_delete=models.CASCADE, related_name='question_course', null=True, blank=True)
    question_category =  models.ForeignKey(Course, on_delete=models.CASCADE, related_name='question_question_category', null=True, blank=True)
    class Meta:
        db_table = 'public\".\"question'

class Answer(models.Model):
    content        =  models.TextField()
    is_correct     =  models.BooleanField(default=False)
    points         =  models.IntegerField(null=True, blank=True)
    question       =  models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answer_question')
    date_added     = models.DateTimeField(default = timezone.now)
    added_by       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='question_answer_added_by', null=True, blank=True)
    class Meta:
        db_table = 'public\".\"answer'

class Quiz(models.Model):
    title              =  models.CharField(max_length=100)
    description        =  models.TextField()
    prerequisites      =  models.CharField(max_length=100) # list of quizes
    register_user_only =  models.BooleanField(default=False)
    passing_score      =  models.IntegerField(null=True, blank=True)
    auto_save_period   =  models.IntegerField(null=True, blank=True)
    time_limit         =  models.IntegerField(null=True, blank=True)
    retakes            =  models.IntegerField(null=True, blank=True)
    is_certificate     =  models.IntegerField(null=True, blank=True)
    is_auto_save       =  models.BooleanField(default=False)
    answer_all         =  models.BooleanField(default=False)
    is_time_limit      =  models.BooleanField(default=False)
    can_retake         =  models.BooleanField(default=False)
    auto_start         =  models.IntegerField(null=True, blank=True)
    show_summary       =  models.BooleanField(default=False)
    skip_question      =  models.BooleanField(default=False)
    show_category      =  models.BooleanField(default=False)
    show_position      =  models.BooleanField(default=False)
    show_numbering     =  models.BooleanField(default=False)
    show_points        =  models.BooleanField(default=False)
    randomize_answers  =  models.BooleanField(default=False)
    per_page           =  models.IntegerField(null=True, blank=True)
    is_material        =  models.BooleanField(default=False)
    show_avg_score     =  models.BooleanField(default=False)
    show_total_score   =  models.BooleanField(default=False)
    show_cat_score     =  models.BooleanField(default=False)
    correct_scores     =  models.BooleanField(default=False)
    time_spent         =  models.BooleanField(default=False)
    added_by           = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quiz_added_by', null=True, blank=True)
    topic              =  models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='quiz_topic', null=True, blank=True)
    lesson             =  models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='quiz_lesson', null=True, blank=True)
    course             =  models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quiz_course', null=True, blank=True)
    quiz_type          =  models.CharField(max_length=100)
    
    class Meta:
        db_table = 'public\".\"quiz'

class QuizQuestion(models.Model):
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quiz_question_added_by', null=True, blank=True)
    Question =  models.ForeignKey(Course, on_delete=models.CASCADE, related_name='question')
    quiz     =  models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='quiz')
    class Meta:
        db_table = 'public\".\"quiz_question'




