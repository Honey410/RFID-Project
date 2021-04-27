from django.shortcuts import render,redirect
from .models import *
from django.conf import settings
from django.core.mail import send_mail
import pytz
import datetime
from datetime import datetime as dt
# Create your views here.
def FacultyRegPage(request):
    return render(request, "app/facreg.html")

def FacultyLoginPage(request):
    return render(request, "app/facultylogin.html")

def FacultyIndexPage(request):
    return render(request, "app/faculty-index.html")

def AddStudentPage(request):
    all_id = Rfid.objects.all()
    if len(all_id) > 0:
        return render(request, "app/add-student.html",{'rfid':all_id})
    else:
        return render(request, "app/add-student.html",{'rfid':'No Key'})

def StudenRegPage(request,rf):
    getrf = Rfid.objects.get(Card_key=rf)
    print(f"--------------------->GOT RFID---------->{getrf}")
    return render(request, "app/stureg.html",{'rfid':getrf})

def RegStudent(request):
    if request.method == 'POST':
        rfid = request.POST['rfid']
        fname = request.POST['fname']
        lname = request.POST['lname']
        gender = request.POST['gender']
        email = request.POST['email']
        password = request.POST['passwd']
        profile = request.FILES['profilepic']
        attmode = request.POST['mode']

        student = Student.objects.create(Firstname=fname,Lastname=lname,Gender=gender,Email=email,Password=password,Profilepic=profile)
        get_rfid = Rfid.objects.get(Card_key=rfid)
        get_rfid.att_mode = attmode
        get_rfid.stu_allot = student
        if attmode == 'on':
            get_rfid.allot = True
        elif attmode == 'off':
            get_rfid.allot = False
        get_rfid.save()
        return redirect('allregstudent')

def AllRegStudent(request):
    allregstu = Rfid.objects.all()
    return render(request, "app/all-reg-stu.html",{'allstu':allregstu})

def UpdateStudentPage(request,pk):
    getrfid = Rfid.objects.get(id=pk)
    print(f"------------------>RFID:{getrfid.Card_key}")
    return render(request, "app/update-stu.html",{'rfid':getrfid})

def UpdateStudent(request,pk):
    getrfid = Rfid.objects.get(id=pk)
    stu_id = request.POST['stuid']
    getStu = Student.objects.get(id=stu_id)
    print(f"-------------UP_DATA-------AND STU ID---->{getrfid.stu_allot.Firstname},{getStu.Firstname}")
    getrfid.stu_allot.Firstname = request.POST['fname'] if request.POST['fname'] else getrfid.stu_allot.Firstname
    getrfid.stu_allot.Lastname = request.POST['lname'] if request.POST['lname'] else getrfid.stu_allot.Lastname
    getrfid.stu_allot.Gender = request.POST['gender'] if request.POST['gender'] else getrfid.stu_allot.Gender
    getrfid.stu_allot.Email = request.POST['email'] if request.POST['email'] else getrfid.stu_allot.Email
    getrfid.stu_allot.Password = request.POST['passwd'] if request.POST['passwd'] else getrfid.stu_allot.Password
    getrfid.att_mode = request.POST['mode'] if request.POST['mode'] else getrfid.att_mode
    if request.POST['mode'] == 'on':
        getrfid.allot = True
    elif request.POST['mode'] == 'off':
        getrfid.allot = False
    try:
        getrfid.stu_allot.Profilepic = request.FILES['img'] if request.FILES['img'] else getrfid.stu_allot.Profilepic
        print("IMAGE UPDATED")
    except Exception as error:
        print(f"-------------IMG-EXC------------>{error}")
    getrfid.save()
    getrfid.stu_allot.save()
    url = f"/update-student/{pk}/"
    return redirect(url)

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

count = 1
def InsertAttendance(request,rfid):
    global count
    getrfid = Rfid.objects.get(Card_key=rfid)
    IST = pytz.timezone('Asia/Kolkata')
    istdt = dt.now(IST)
    date = istdt.strftime("%Y-%m-%d")
    time = istdt.strftime("%H:%M")
    count = count + 1
    if count%2==0:
        storeatten = Attendance.objects.create(rfid=getrfid,Date=date,TimeIn=time)
        request.session['attid'] = storeatten.id
        subject = f'{getrfid.stu_allot.Firstname} In Attendance'
        message = f'{getrfid.stu_allot.Firstname} | {getrfid.Card_key} | {date} | {time} |'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [getrfid.stu_allot.Email, ]
        send_mail( subject, message, email_from, recipient_list )  
    else:
        print("IN ELSE")
        storeatten = Attendance.objects.get(id=request.session['attid'])
        storeatten.TimeOut = time
        storeatten.save()
        subject = f'{getrfid.stu_allot.Firstname} Out Attendance'
        message = f'{getrfid.stu_allot.Firstname} | {getrfid.Card_key} | {date} | {time} |'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [getrfid.stu_allot.Email, ]
        send_mail( subject, message, email_from, recipient_list )
        count = 1

def ScanRfid(request):
    rfids = request.GET['card_uid']
    chech_rf = Rfid.objects.filter(Card_key=rfids)
    if len(chech_rf) > 0:
        if chech_rf[0].att_mode == 'on':
            InsertAttendance(request,rfids)
        elif chech_rf[0].att_mode == 'off':
            print("RFID MODE OFF")
    else:
        store = Rfid.objects.create(Card_key=rfids)
    return redirect('addstudent')
