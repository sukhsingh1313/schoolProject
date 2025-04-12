from django.contrib import admin
from .models import *
from Admission.models import *
from .forms import NewsSessionAdminForm
# Register your models here.


# Customizing admin site headers and titles
admin.site.site_header = "Bright Future School Admin"
admin.site.site_title = "Bright Future Admin Portal"
admin.site.index_title = "Welcome to Bright Future Admin Panel"


# Register your models here

# index page==>
admin.site.register(notificationModel)
admin.site.register(Events)

class NewsAdminSession(admin.ModelAdmin):
    list_display = ('news_title', 'post_author', 'created_at')
    form = NewsSessionAdminForm
admin.site.register(News_session,NewsAdminSession)

admin.site.register(Archive)
admin.site.register(Comment)


@admin.register(HomeBenner)
class HomeBannerAdmin(admin.ModelAdmin):
    list_display = ('titlefirst','highlightwords','titlesecond')




# about page admin info. =>
admin.site.register(deppartment)

@admin.register(SchoolHistory)
class SchoolHistoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)

@admin.register(SchoolMission)
class SchoolMissionAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'mission_statement')
    list_filter = ('created_at',)

@admin.register(SchoolVision)
class SchoolVisionAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'vision_statement')
    list_filter = ('created_at',)

@admin.register(CoreValues)
class CoreValuesAdmin(admin.ModelAdmin):
    list_display = ('value_name', 'created_at')
    search_fields = ('value_name', 'description')
    list_filter = ('created_at',)


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  
    search_fields = ('name',)


@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation','deppartment')  
    search_fields = ('name', 'designation', 'deppartment')  


# academic admin data

class TeacherAdmin(admin.ModelAdmin):
    list_display = ("display_name", "display_subjects", "email", "phone")  # Include custom methods here

    def display_name(self, obj):
        return obj.name  # Displays the related StaffMember name
    display_name.short_description = "Teacher Name"

    def display_subjects(self, obj):
        # Join all subject names into a string for display
        return ", ".join([subject.name for subject in obj.subject.all()])
    display_subjects.short_description = "Subjects"

admin.site.register(Teacher,TeacherAdmin)

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'section')  
    search_fields = ('name',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')  
    search_fields = ('name',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'roll_number')  
    search_fields = ('name','roll_number')

@admin.register(Curriculm)
class CurriculmAdmin(admin.ModelAdmin):
    list_display = ('class_assigned', 'subject','start_date')  
    search_fields = ('class_assigned',)


@admin.register(TimetableEntry)
class TimetableEntryAdmin(admin.ModelAdmin):
    list_display = ('class_assigned', 'subject', 'teacher', 'day_of_week', 'start_time', 'end_time')
    list_filter = ('class_assigned', 'day_of_week', 'teacher')




# admission section:-


@admin.register(Admission_Guidelines)
class AdmissionGuideAdmin(admin.ModelAdmin):
    list_display = ('title','description')
    search_fields = ('title', 'description')

@admin.register(School_Guidelines)
class School_GuidelinesAdmin(admin.ModelAdmin):
    list_display = ('title',)
    

