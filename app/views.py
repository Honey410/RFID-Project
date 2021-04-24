from django.shortcuts import render,redirect
from .models import *
# Create your views here.
def FacultyRegPage(request):
    return render(request, "app/facreg.html")

def FacultyLoginPage(request):
    return render(request, "app/facultylogin.html")

def FacultyIndexPage(request):
    return render(request, "app/faculty-index.html")

def AddStudentPage(request):
    return render(request, "app/add-student.html")

def FacultyRegistration(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        gender = request.POST['gender']
        email = request.POST['email']
        password = request.POST['passwd']
        profile = request.FILES['profilepic']

        faculty =Faculty.objects.create(Firstname=fname,Lastname=lname,Gender=gender,Email=email,Password=password,Profilepic=profile)
        return redirect('facultylogin')

def FacultyLogin(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['passwd']

        user = Faculty.objects.filter(Email=email)
        if len(user) > 0:
            if user[0].Password == password:
                fac = Faculty.objects.get(Email=user[0].Email)
                request.session['id'] = fac.id
                request.session['email'] = fac.Email
                request.session['firstname'] = fac.Firstname
                return redirect("faculty-index")
            else:
                msg = "Password is invalid"
                return render(request, "app/facultylogin.html", {'msg': msg})
        else:
            msg = "faculty doesn't exist"
            return render(request, "app/facultylogin.html", {'msg': msg})

def ScanRfid(request):
    rfid = request.GET['card_uid']
    return render(request, "app/add-student.html",{'rfid':rfid})