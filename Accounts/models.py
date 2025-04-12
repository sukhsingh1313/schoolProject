from django.db import models

class Student(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    mothername = models.CharField(max_length=100)
    fathername = models.CharField(max_length=100)
    address = models.TextField()
    gender = models.CharField(max_length=10)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    dob = models.DateField()
    pincode = models.CharField(max_length=10)
    course = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.firstname
    


