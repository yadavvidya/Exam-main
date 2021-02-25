from django.contrib import messages
from django.contrib.auth import authenticate , login, logout
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from student.models import Courses, CustomUser, Subjects
from django.urls import reverse
from student.EmailBackEnd import EmailBackEnd

# Create your views here.
def index(request):
    return render(request,'index.html')

def ShowLoginPage(request):
    return render(request,"login_page.html")

def doLogin(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user = EmailBackEnd.authenticate(request,username=request.POST.get("username"),password=request.POST.get("password"))
        if user!=None:
            login(request,user)
            if user.user_type=="1":
                return HttpResponseRedirect(reverse('admin_home'))
            elif user.user_type=="2":
                return HttpResponseRedirect(reverse("staff_home"))
            else:
                return HttpResponseRedirect(reverse("student_home"))
        else:
            messages.error(request,"Invalid Login Details")
            return HttpResponseRedirect("/")

def GetUserDetails(request):
    if request.user!=None:
       return HttpResponse("User : "+request.user.email+" usertype : "+str(request.user.user_type))
    else:
        return HttpResponse("Please Login First")

def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")


def signup_student(request):
    courses=Courses.objects.all()
    return render(request,"signup_student_page.html",{"courses":courses})

def do_student_signup(request):
    first_name=request.POST.get("first_name")
    last_name=request.POST.get("last_name")
    username=request.POST.get("username")
    pnr = request.POST.get("pnr")
    email=request.POST.get("email")
    password=request.POST.get("password")
    address=request.POST.get("address")
    course_id=request.POST.get("course")
    gender=request.POST.get("gender")
    dob=request.POST.get("dob")
    profile_pic = request.FILES['profile_pic']
    fs = FileSystemStorage()
    filename = fs.save(profile_pic.name,profile_pic)
    profile_pic_url = fs.url(filename)
    try:
        user=CustomUser.objects.create_user(first_name=first_name,last_name=last_name,username=username,password=password,email=email,user_type=3)
        user.students.address=address
        course_obj=Courses.objects.get(id=course_id)
        user.students.course_id=course_obj
        user.dob=dob
        user.students.pnr = pnr
        user.students.gender=gender
        user.students.profile_pic=profile_pic_url
        user.save()
        messages.success(request,"Successfully Registered")
        return HttpResponseRedirect(reverse("login"))
    except:
        messages.error(request,"Failed to Create Account")
        return HttpResponseRedirect(reverse("login"))

