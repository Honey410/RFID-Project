from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('faculty/',views.FacultyRegPage,name="faculty"),
    path('faculty-login/',views.FacultyLoginPage,name="facultylogin"),
    path('Faculty-index/',views.FacultyIndexPage,name="faculty-index"),
    path('faculty-registration/',views.FacultyRegistration,name="facreg"),
    path('login-faculty/',views.FacultyLogin,name="faclogin"),
]