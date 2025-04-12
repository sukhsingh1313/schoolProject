from django.urls import path
from . import views
from Admission.views import *
from Accounts.views import password_reset_request, register_student,student_login_view,password_reset_confirm,logout_view
from Results.views import(result_pdf,result_detail,result_search,upload_results)
urlpatterns = [
    path('',views.home,name='home'),
    # path('remove-notification/<int:notify_id>/', views.remove_notification, name='remove_notification'),
    path('news-post/<slug:slug>',views.NewsView,name='NewsView'),
    path('news/<int:id>/comment/',views.add_comment,name='add_comment'),
     path('archive/<slug:slug>/', views.archive, name='archive_view'),

    # about section
    path('about/', views.about_view, name='about_view'),
    path('about/<slug:slug>/',views.about_view,name='about_view'),

    # academic section
    path('academic/', views.academic_view, name='academic_view'),
    path('academic/time_table/<int:id>', views.Class_timetable, name='timetable'),

    #addmission section:
    path('admission-guidelines/', AdmissionGuidelines_view, name='admission_view'),
    path('admission/online_applications/', online_application_view, name='online_applications'),
    path('admission/admission_form_view/', admission_form_view, name='admission_form_view'),

    # Accounts:
    path('student-register/', register_student, name='register_student'),
    path('student-login/', student_login_view, name='student_login_view'),
    path('logout/', logout_view, name='logout_view'),
    path("password_reset/", password_reset_request, name="password_reset"),

    path("password-reset-confirm/<uidb64>/<token>/",password_reset_confirm,name="password_reset_confirm" ),

  #Results:
   path('results/', result_search, name='result_search'),
    path('results/<str:roll_no>/', result_detail, name='result_detail'),
    path('results/pdf/<str:roll_no>/', result_pdf, name='result_pdf'),
    #  path('upload-results/', upload_results, name='upload_results'), 
     path('Results/upload-results/', upload_results, name='upload_results'),

]