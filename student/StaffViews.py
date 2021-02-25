from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from student import forms
from student.filters import studentFilter, staffFilter, courseFilter, subjectFilter, testFilter, questionFilter, \
    noticeFilter
from student.models import CustomUser, Courses, Students, Staffs, Subjects, Test, Question, Result, Notice


def staff_home(request):
    test_count=Test.objects.all().count()
    question_count=Question.objects.all().count()
    student_count = Students.objects.all().count()
    staff_count = Staffs.objects.all().count()
    subject_count = Subjects.objects.all().count()
    course_count = Courses.objects.all().count()
    return render(request,"staff_template/staff_template.html",{"test_count":test_count,"question_count":question_count,"student_count":student_count,"staff_count":staff_count,"subject_count":subject_count,"course_count":course_count})


def staff_manage_student(request):
    students=Students.objects.all().order_by('-Academic_year','course_id__course_name','admin__last_name','admin__first_name')
    myFilter = studentFilter(request.GET, queryset=students)
    students = myFilter.qs
    return render(request,"staff_template/staff_manage_student_template.html",{"students":students,"myFilter":myFilter})

def view_staff(request):
    staffs=Staffs.objects.all().order_by('admin__last_name','admin__first_name')
    myFilter = staffFilter(request.GET, queryset=staffs)
    staffs = myFilter.qs
    return render(request,"staff_template/view_staff_template.html",{"staffs":staffs,'myFilter':myFilter})

def view_course(request):
    courses=Courses.objects.all().order_by('course_name')
    myFilter = courseFilter(request.GET, queryset=courses)
    courses = myFilter.qs
    return render(request,"staff_template/view_course_template.html",{"courses":courses,"myFilter":myFilter})

def view_subject(request):
    subjects=Subjects.objects.all().order_by('course_id__course_name','subject_name')
    myFilter = subjectFilter(request.GET, queryset=subjects)
    subjects = myFilter.qs
    return render(request,"staff_template/view_subject_template.html",{"subjects":subjects,"myFilter":myFilter})

def staff_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    staff=Staffs.objects.get(admin=user)
    return render(request,"staff_template/staff_profile.html",{"user":user,"staff":staff})

def staff_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("staff_profile"))
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
            staff=Staffs.objects.get(admin=customuser.id)
            staff.address=address
            staff.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("staff_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("staff_profile"))




def staff_add_test(request):
    form = forms.TestForm()
    return render(request,"staff_template/add_test_template.html",{"form":form})

def staff_add_test_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        form = forms.TestForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data[ "name" ]
            subject_id = form.cleaned_data[ "subject_id" ]
            course_id = form.cleaned_data[ "course_id" ]
            question_number = form.cleaned_data[ "question_number" ]
            total_marks = form.cleaned_data[ "total_marks" ]
            Academic_year=form.cleaned_data["Academic_year"]
            due = form.cleaned_data[ "due" ]
            complete = form.cleaned_data[ "complete" ]
            try:
                test = Test()
                test.name = name
                subject_obj = Subjects.objects.get(id=subject_id)
                test.subject_id = subject_obj
                course_obj = Courses.objects.get(id=course_id)
                test.course_id = course_obj
                test.question_number = question_number
                test.total_marks = total_marks
                test.Academic_year=Academic_year
                test.due = due
                test.complete = complete
                test.save()
                messages.success(request, "Successfully Added Test")
                return HttpResponseRedirect(reverse("staff_add_test"))
            except:
                messages.error(request,"Failed to Add Test")
                return HttpResponseRedirect(reverse("staff_add_test"))
        else:
            form = forms.TestForm(request.POST)
            return render('request', "staff_template/add_test_template.html", {'form': form})

def staff_manage_test(request):
    test = Test.objects.all().order_by('-Academic_year', 'complete', 'due','name')
    myFilter = testFilter(request.GET, queryset=test)
    test = myFilter.qs
    return render(request,"staff_template/manage_test_template.html",{"test":test,"myFilter":myFilter})

def staff_edit_test(request,test_id):
    request.session[ 'test_id' ] = test_id
    test = Test.objects.get(id=test_id)
    form = forms.EditTestForm()
    form.fields[ 'name' ].initial = test.name
    form.fields[ 'course_id' ].initial = test.course_id.id
    form.fields[ 'subject_id' ].initial = test.subject_id.id
    form.fields[ 'question_number' ].initial = test.question_number
    form.fields[ 'total_marks' ].initial = test.total_marks
    form.fields['Academic_year'].initial = test.Academic_year
    form.fields[ 'due' ].initial = test.due
    form.fields[ 'complete' ].initial = test.complete
    return render(request,"staff_template/edit_test_template.html",{"test":test,"form":form,"id":test_id})

def staff_edit_test_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        test_id = request.session.get("test_id")
        form = forms.EditTestForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data[ "name" ]
            course_id = form.cleaned_data[ "course_id" ]
            subject_id = form.cleaned_data[ "subject_id" ]
            question_number = form.cleaned_data[ "question_number" ]
            total_marks = form.cleaned_data[ "total_marks" ]
            Academic_year=form.cleaned_data["Academic_year"]
            due = form.cleaned_data[ "due" ]
            complete = form.cleaned_data[ 'complete' ]
            try:
                test = Test.objects.get(id=test_id)
                course = Courses.objects.get(id=course_id)
                test.course_id = course
                subject = Subjects.objects.get(id=subject_id)
                test.subject_id = subject
                test.name = name
                test.question_number = question_number
                test.total_marks = total_marks
                test.Academic_year=Academic_year
                test.due = due
                test.complete = complete
                test.save()
                del request.session[ 'test_id' ]
                messages.success(request,"Successfully Edited Test")
                return HttpResponseRedirect(reverse("staff_edit_test",kwargs={"test_id":test_id}))
            except:
                messages.error(request,"Failed to Edit Test")
                return HttpResponseRedirect(reverse("staff_edit_test",kwargs={"test_id":test_id}))
        else:
            form=forms.EditTestForm(request.POST)
            test=Test.objects.get(id=test_id)
            return render(request,"staff_template/edit_test_template.html",{"form":form,"id":test_id,"test":test,"name":test.name})

def staff_add_question(request):
    tests=Test.objects.all()
    return render(request,"staff_template/add_question_template.html",{"tests":tests})

def staff_add_question_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        Test_name=request.POST.get("test")
        test=Test.objects.get(id=Test_name)
        question=request.POST.get("question")
        question_type = request.POST.get("question_type")
        Option1=request.POST.get("Option1")
        Option2 = request.POST.get("Option2")
        Option3 = request.POST.get("Option3")
        Option4 = request.POST.get("Option4")
        answer = request.POST.get("answer")
        marks=request.POST.get("marks")
        try:
            questions=Question(Test_name=test,question=question,question_type=question_type,Option1=Option1,Option2=Option2,Option3=Option3,Option4=Option4,answer=answer,marks=marks)
            questions.save()
            messages.success(request,"Successfully Added Question")
            return HttpResponseRedirect(reverse("staff_add_question"))
        except:
            messages.error(request,"Failed to Add Question")
            return HttpResponseRedirect(reverse("staff_add_question"))


def staff_manage_question(request):
    questions=Question.objects.all().order_by('-Test_name__Academic_year','Test_name__course_id','-created_at',)
    myFilter = questionFilter(request.GET, queryset=questions)
    questions = myFilter.qs
    return render(request,"staff_template/manage_question_template.html",{"questions":questions,"myFilter":myFilter})

def staff_question_view(request):
    return render(request,'staff_template/admin_question.html')

def staff_view_question_view(request):
    test= Test.objects.all().order_by('-Academic_year', 'complete', 'due','name')
    return render(request,'staff_template/admin_view_question.html',{'test':test})

def staff_edit_question(request,question_id):
    questions=Question.objects.get(id=question_id)
    test=Test.objects.all()
    return render(request,"staff_template/edit_question_template.html",{"questions":questions,"test":test,"id":question_id})

def staff_edit_question_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        question_id=request.POST.get("question_id")
        Test_name = request.POST.get("test")
        question = request.POST.get("question")
        question_type = request.POST.get("question_type")
        Option1 = request.POST.get("Option1")
        Option2 = request.POST.get("Option2")
        Option3 = request.POST.get("Option3")
        Option4 = request.POST.get("Option4")
        answer = request.POST.get("answer")
        marks=request.POST.get("marks")
        try:
            questions=Question.objects.get(id=question_id)
            test = Test.objects.get(id=Test_name)
            questions.Test_name=test
            questions.question=question
            questions.question_type=question_type
            questions.Option1=Option1
            questions.Option2=Option2
            questions.Option3=Option3
            questions.Option4=Option4
            questions.answer=answer
            questions.marks=marks
            questions.save()
            messages.success(request,"Successfully Edited Question")
            return HttpResponseRedirect(reverse("staff_edit_question",kwargs={"question_id":question_id}))
        except:
            messages.error(request,"Failed to Edit Question")
            return HttpResponseRedirect(reverse("staff_edit_question",kwargs={"question_id":question_id}))

def staff_question_view(request):
    return render(request,'staff_template/admin_question.html')

def staffs_view_question_view(request):
    test= Test.objects.all().order_by('-created_at', 'complete', 'due','name')
    return render(request,'staff_template/admin_view_question.html',{'test':test})


def staff_view_question_view(request,pk):
    questions=Question.objects.all().filter(Test_name=pk)
    myFilter = questionFilter(request.POST, queryset=questions)
    questions = myFilter.qs
    return render(request,'staff_template/view_question.html',{'questions':questions,"myFilter":myFilter})

def staff_delete_question_view(request,pk):
    question=Question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect('/admin_view_question_view')

def staff_delete_test(request,pk):
    test=Test.objects.get(id=pk)
    test.delete()
    return HttpResponseRedirect('/staff_manage_test')

def staff_view_student_marks_view(request):
    students= Students.objects.all().order_by('-Academic_year','course_id__course_name','admin__last_name','admin__first_name')
    myFilter = studentFilter(request.GET, queryset=students)
    students = myFilter.qs
    return render(request,'staff_template/admin_view_student_marks.html',{'students':students,'myFilter':myFilter})

def staff_view_marks_view(request,pk):
    student = Students.objects.get(id=pk)
    course = student.course_id
    year = student.Academic_year
    test = Test.objects.all().order_by('-Academic_year','complete', 'due', 'name').filter(course_id=course).filter(Academic_year=year)
    myFilter = testFilter(request.GET, queryset=test)
    test = myFilter.qs
    response =  render(request,'staff_template/admin_view_marks.html',{'test':test,'myFilter':myFilter})
    response.set_cookie('student_id',str(pk))
    return response

def staff_check_marks_view(request,pk):
    student_id = request.COOKIES.get('student_id')
    student = Students.objects.get(id=student_id)
    test = Test.objects.get(id=pk)
    results = Result.objects.all().filter(student=student).filter(exam=test)
    questions = Question.objects.all().filter(Test_name=test)

    total_marks = 0
    for q in questions:
        total_marks += q.marks
    return render(request, 'staff_template/admin_check_marks.html', {'results': results,'total_marks':total_marks})

def staff_view_notice(request):
    notices = Notice.objects.all().order_by('-Academic_year', '-created_at')
    myFilter = noticeFilter(request.GET, queryset=notices)
    notices = myFilter.qs
    return render(request,"staff_template/view_notice_template.html",{"notices":notices,"myFilter":myFilter})