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

class Attendance(models.Model):
    Student = models.ForeignKey(Student, on_delete=models.CASCADE)
    rfid = models.ForeignKey(Rfid, on_delete=models.CASCADE,null=True)
    Date = models.DateTimeField(auto_now_add=True)
    TimeIn = models.TimeField(auto_now_add=True)
    TimeOut = models.TimeField(auto_now_add=True)