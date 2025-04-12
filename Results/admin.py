# admin.py
from django.contrib import admin
from .models import StudentProfile, Result

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('roll_no', 'user', 'admission_year')  # Use roll_number here

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam_year', 'exam_type', 'percentage', 'result_status')
