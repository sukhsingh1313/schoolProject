from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now
from MySchoolApp.models import *

# addmission models :- 
class Admission_Guidelines(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    documents_required = models.CharField(max_length=500,null=True,blank=True)
    upload_document = models.FileField(upload_to='', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"


class School_Guidelines(models.Model):
    title = models.CharField(max_length=1000)
    description = models.TextField()



# online applications:-

class AdmissionForm(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES) 
    address = models.TextField()
    join_class = models.ForeignKey(Class, on_delete=models.CASCADE,blank=True,null=True)
    additional_info = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} - {self.last_name}"


class AdmissionFormPdf(models.Model):
    Offline_pdf = models.FileField(upload_to='')



