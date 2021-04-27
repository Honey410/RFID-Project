from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('faculty/',views.FacultyRegPage,name="faculty"),
    path('faculty-login/',views.FacultyLoginPage,name="facultylogin"),
    path('add-student/',views.AddStudentPage,name="addstudent"),
    path('student-reg/<str:rf>/',views.StudenRegPage,name="student-reg"),
    path('reg-student/',views.RegStudent,name="regstudent"),
    path('all-reg-student/',views.AllRegStudent,name="allregstudent"),
    path('update-student/<int:pk>/',views.UpdateStudentPage,name="update-student"),
    path('update-stu/<int:pk>/',views.UpdateStudent,name="updatestu"),
    path('Faculty-index/',views.FacultyIndexPage,name="faculty-index"),
    path('faculty-registration/',views.FacultyRegistration,name="facreg"),
    path('login-faculty/',views.FacultyLogin,name="faclogin"),
    path('scan-id/',views.ScanRfid,name='scanid'),
]