from django.contrib import admin
from .models import AdmissionForm

@admin.register(AdmissionForm)
class AdmissionFormAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'gender', 'join_class', 'submitted_at')
    list_filter = ('join_class', 'gender', 'submitted_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')