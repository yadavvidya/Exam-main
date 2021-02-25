import random

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from student.models import CustomUser, Students, Notice, Test, Question, Result, Subjects


def student_home(request):
    student = Students.objects.get(admin=request.user.id)
    course=student.course_id
    year=student.Academic_year
    test_count=Test.objects.all().filter(course_id=course).filter(Academic_year=year).count()
    notice_count = Notice.objects.all().filter(Academic_year=year).count()
    subject_count=Subjects.objects.all().filter(course_id=course).count()
    return render(request,"student_template/student_template.html",{"test_count":test_count,"notice_count":notice_count,"subject_count":subject_count})

def student_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    student=Students.objects.get(admin=user)
    return render(request,"student_template/student_profile.html",{"user":user,"student":student})

def student_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("student_profile"))
    else:
        first_name=request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        address = request.POST.get("address")
        password=request.POST.get("password")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            if password!=None and password!="":
                customuser.set_password(password)
            customuser.save()
            student=Students.objects.get(admin=customuser.id)
            student.address=address
            student.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("student_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("student_profile"))

def view_notice(request):
    student = Students.objects.get(admin=request.user.id)
    year=student.Academic_year
    notices=Notice.objects.all().filter(Academic_year=year).order_by('-created_at')
    return render(request,"student_template/view_notice_template.html",{"notices":notices})



def student_exam_view(request):
    student=Students.objects.get(admin=request.user.id)
    course=student.course_id
    year=student.Academic_year
    tests=Test.objects.all().filter(course_id=course).filter(Academic_year=year).order_by('complete','due')
    return render(request,'student_template/student_exam.html',{'tests':tests})



def take_exam_view(request, pk):
    test = Test.objects.get(id=pk)
    total_questions = Question.objects.all().filter(Test_name=test).count()
    questions = Question.objects.all().filter(Test_name=test)

    total_marks = 0
    for q in questions:
        total_marks += q.marks
    return render(request, 'student_template/take_exam.html',{'test': test,'total_questions': total_questions, 'total_marks': total_marks})

def start_exam_view(request,pk):
    test = Test.objects.get(id=pk)
    questions = list(Question.objects.all().filter(Test_name=test))
    random.shuffle(questions)
    if request.method == 'POST':
        pass
    response = render(request, 'student_template/start_exam.html', {'test': test, 'questions': questions})
    response.set_cookie('test_id', test.id)
    return response


def calculate_marks_view(request):
    if request.COOKIES.get('test_id') is not None:
        test_id = request.COOKIES.get('test_id')
        test = Test.objects.get(id=test_id)
        score=0
        total_marks = 0
        questions = Question.objects.all().filter(Test_name=test)
        for i in range(len(questions)):
            score+=questions[i].marks
            selected_ans = request.POST.get(str(questions[i].id))
            actual_answer = questions[ i ].answer
            if selected_ans == actual_answer:
                total_marks = total_marks + questions[ i ].marks
        customuser = CustomUser.objects.get(id=request.user.id)
        student = Students.objects.get(admin=customuser.id)
        result = Result()
        result.marks = total_marks
        result.exam = test
        result.percentage=(total_marks/score)*100
        result.student = student
        result.save()
        return HttpResponseRedirect('view-result')

def view_result_view(request):
    student = Students.objects.get(admin=request.user.id)
    course = student.course_id
    year = student.Academic_year
    tests = Test.objects.all().filter(course_id=course).filter(Academic_year=year).order_by('complete','due')
    return render(request, 'student_template/view_result.html', {'tests': tests})


def check_marks_view(request,pk):
    customuser = CustomUser.objects.get(id=request.user.id)
    student = Students.objects.get(admin=customuser.id)
    test=Test.objects.get(id=pk)
    results= Result.objects.all().filter(exam=test).filter(student=student)
    questions = Question.objects.all().filter(Test_name=test)

    total_marks = 0
    for q in questions:
        total_marks += q.marks
    return render(request,'student_template/check_marks.html',{'results':results,'total_marks':total_marks})

def student_marks_view(request):
    student = Students.objects.get(admin=request.user.id)
    course = student.course_id
    year=student.Academic_year
    tests = Test.objects.all().filter(course_id=course).filter(Academic_year=year).order_by('complete','due')
    return render(request,'student_template/view_result.html',{'tests':tests})

def student_view_subject(request):
    student=Students.objects.get(admin=request.user.id)
    course = student.course_id
    subjects = Subjects.objects.all().filter(course_id=course).order_by('subject_name')
    return render(request,'student_template/manage_subject_template.html',{'subjects':subjects})