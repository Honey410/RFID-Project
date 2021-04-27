from django.db import models
from .models import *
# Create your models here.

class Faculty(models.Model):
    Firstname = models.CharField(max_length=100, default="fname")
    Lastname = models.CharField(max_length=100, default="lname")
    Gender = models.CharField(max_length=100, default="Gender")
    Email = models.EmailField(max_length=100, default="Email", unique=True)
    Password = models.CharField(max_length=100, default="passwd")
    Profilepic = models.ImageField(upload_to="faculty-profile/", default="abc")


class Student(models.Model):
    Firstname = models.CharField(max_length=100, default="fname")
    Lastname = models.CharField(max_length=100, default="lname")
    Gender = models.CharField(max_length=100, default="Gender")
    Email = models.EmailField(max_length=100, default="Email", unique=True)
    Password = models.CharField(max_length=100, default="passwd")
    Profilepic = models.ImageField(upload_to="student-profile/", default="abc")

class Rfid(models.Model):
    Card_key = models.CharField(max_length=100)
    att_mode = models.CharField(max_length=100,default="Mode")
    stu_allot = models.ForeignKey(Student,on_delete=models.CASCADE,null=True)
    allot = models.BooleanField(default=False)

class Attendance(models.Model):
    rfid = models.ForeignKey(Rfid, on_delete=models.CASCADE,null=True)
    Date = models.DateField(null=True)
    TimeIn = models.TimeField(null=True)
    TimeOut = models.TimeField(null=True)