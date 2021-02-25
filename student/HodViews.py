from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from student import forms
from student.filters import staffFilter, studentFilter, testFilter, noticeFilter, courseFilter, subjectFilter,questionFilter
from student.forms import AddStudentForm, EditStudentForm
from student.models import CustomUser, Staffs, Courses, Subjects, Students, Notice, Test, Question, Result


def admin_home(request):
    test_count=Test.objects.all().count()
    question_count=Question.objects.all().count()
    student_count=Students.objects.all().count()
    staff_count=Staffs.objects.all().count()
    subject_count=Subjects.objects.all().count()
    course_count=Courses.objects.all().count()
    notice_count=Notice.objects.all().count()
    return render(request,"hod_template/home_content.html",{"test_count":test_count,"question_count":question_count,"student_count":student_count,"staff_count":staff_count,"subject_count":subject_count,"course_count":course_count,"notice_count":notice_count})



def add_staff(request):
    return render(request,"hod_template/add_staff_template.html")

def add_staff_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        staff_id = request.POST.get("staff_id")
        email=request.POST.get("email")
        password=request.POST.get("password")
        address=request.POST.get("address")
        try:
            user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=2)
            user.staffs.address=address
            user.staffs.staff_id = staff_id
            user.save()
            messages.success(request,"Successfully Added Staff")
            return HttpResponseRedirect(reverse("add_staff"))
        except:
            messages.error(request,"Failed to Add Staff")
            return HttpResponseRedirect(reverse("add_staff"))


def add_course(request):
    return render(request,"hod_template/add_course_template.html")

def add_course_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        course=request.POST.get("course")
        try:
            course_model=Courses(course_name=course)
            course_model.save()
            messages.success(request,"Successfully Added Course")
            return HttpResponseRedirect(reverse("add_course"))
        except:
            messages.error(request,"Failed To Add Course")
            return HttpResponseRedirect(reverse("add_course"))


def add_student(request):
    form=AddStudentForm()
    return render(request,"hod_template/add_student_template.html",{"form":form})

def add_student_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        form=AddStudentForm(request.POST,request.FILES)
        if form.is_valid():
            first_name=form.cleaned_data["first_name"]
            last_name=form.cleaned_data["last_name"]
            username=form.cleaned_data["username"]
            pnr = form.cleaned_data["pnr"]
            email=form.cleaned_data["email"]
            password=form.cleaned_data["password"]
            address=form.cleaned_data["address"]
            dob=form.cleaned_data["dob"]
            course_id=form.cleaned_data["course"]
            gender=form.cleaned_data["gender"]
            Academic_year=form.cleaned_data["Academic_year"]

            profile_pic=request.FILES['profile_pic']
            fs=FileSystemStorage()
            filename=fs.save(profile_pic.name,profile_pic)
            profile_pic_url=fs.url(filename)

            try:
                user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=3)
                user.students.pnr = pnr
                user.students.address=address
                course_obj=Courses.objects.get(id=course_id)
                user.students.course_id=course_obj
                user.students.dob=dob
                user.students.gender=gender
                user.Academic_year=Academic_year
                user.students.profile_pic=profile_pic_url
                user.save()
                messages.success(request,"Successfully Added Student")
                return HttpResponseRedirect(reverse("add_student"))
            except:
                messages.error(request,"Failed to Add Student")
                return HttpResponseRedirect(reverse("add_student"))
        else:
            form=AddStudentForm(request.POST)
            return render(request, "hod_template/add_student_template.html", {"form": form})



def add_subject(request):
    courses=Courses.objects.all()
    return render(request,"hod_template/add_subject_template.html",{"courses":courses})

def add_subject_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_name=request.POST.get("subject_name")
        course_id=request.POST.get("course")
        course=Courses.objects.get(id=course_id)

        try:
            subject=Subjects(subject_name=subject_name,course_id=course)
            subject.save()
            messages.success(request,"Successfully Added Subject")
            return HttpResponseRedirect(reverse("add_subject"))
        except:
            messages.error(request,"Failed to Add Subject")
            return HttpResponseRedirect(reverse("add_subject"))


def manage_staff(request):
    staffs=Staffs.objects.all().order_by('admin__last_name','admin__first_name')
    myFilter=staffFilter(request.GET,queryset=staffs)
    staffs=myFilter.qs
    return render(request,"hod_template/manage_staff_template.html",{"staffs":staffs,"myFilter":myFilter})

def manage_student(request):
    students=Students.objects.all().order_by('-Academic_year','course_id__course_name','admin__last_name','admin__first_name')
    myFilter = studentFilter(request.GET, queryset=students)
    students = myFilter.qs
    return render(request,"hod_template/manage_student_template.html",{"students":students,"myFilter":myFilter})

def manage_course(request):
    courses=Courses.objects.all().order_by('course_name')
    myFilter = courseFilter(request.GET, queryset=courses)
    courses = myFilter.qs
    return render(request,"hod_template/manage_course_template.html",{"courses":courses,"myFilter":myFilter})

def manage_subject(request):
    subjects=Subjects.objects.all().order_by('course_id__course_name','subject_name')
    myFilter = subjectFilter(request.GET, queryset=subjects)
    subjects = myFilter.qs
    return render(request,"hod_template/manage_subject_template.html",{"subjects":subjects,"myFilter":myFilter})


def edit_staff(request,staff_id):
    staff=Staffs.objects.get(admin=staff_id)
    return render(request,"hod_template/edit_staff_template.html",{"staff":staff,"id":staff_id})

def edit_staff_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id=request.POST.get("staff_id")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        staff_id = request.POST.get("staff_id")
        email=request.POST.get("email")
        username=request.POST.get("username")
        address=request.POST.get("address")

        try:
            user=CustomUser.objects.get(admin=staff_id)
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.save()

            staff_model=Staffs.objects.get(admin=staff_id)
            staff_model.address=address
            staff_model.save()
            messages.success(request,"Successfully Edited Staff")
            return HttpResponseRedirect(reverse("edit_staff",kwargs={"staff_id":staff_id}))
        except:
            messages.error(request,"Failed to Edit Staff")
            return HttpResponseRedirect(reverse("edit_staff",kwargs={"staff_id":staff_id}))

def edit_student(request,student_id):
    request.session['student_id']=student_id
    student=Students.objects.get(admin=student_id)
    form=EditStudentForm()
    form.fields['email'].initial=student.admin.email
    form.fields['first_name'].initial=student.admin.first_name
    form.fields['last_name'].initial=student.admin.last_name
    form.fields['username'].initial=student.admin.username
    form.fields['address'].initial=student.address
    form.fields['course'].initial=student.course_id.id
    form.fields['gender'].initial=student.gender
    form.fields['dob'].initial=student.dob
    form.fields['Academic_year'].initial=student.Academic_year
    return render(request,"hod_template/edit_student_template.html",{"form":form,"id":student_id,"username":student.admin.username})

def edit_student_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        student_id=request.session.get("student_id")
        if student_id==None:
            return HttpResponseRedirect(reverse("manage_student"))

        form=EditStudentForm(request.POST,request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            pnr = form.cleaned_data["pnr"]
            email = form.cleaned_data["email"]
            address = form.cleaned_data["address"]
            dob = form.cleaned_data["dob"]
            course_id = form.cleaned_data["course"]
            gender = form.cleaned_data["gender"]
            Academic_year=form.cleaned_data["Academic_year"]

            if request.FILES.get('profile_pic',False):
                profile_pic=request.FILES['profile_pic']
                fs=FileSystemStorage()
                filename=fs.save(profile_pic.name,profile_pic)
                profile_pic_url=fs.url(filename)
            else:
                profile_pic_url=None


            try:
                user=CustomUser.objects.get(id=student_id)
                user.first_name=first_name
                user.last_name=last_name
                user.username=username
                user.email=email
                user.save()

                student=Students.objects.get(admin=student_id)
                student.pnr = pnr
                student.address=address
                student.dob=dob
                student.gender=gender
                course=Courses.objects.get(id=course_id)
                student.course_id=course
                student.Academic_year=Academic_year
                if profile_pic_url!=None:
                    student.profile_pic=profile_pic_url
                student.save()
                del request.session['student_id']
                messages.success(request,"Successfully Edited Student")
                return HttpResponseRedirect(reverse("edit_student",kwargs={"student_id":student_id}))
            except:
                messages.error(request,"Failed to Edit Student")
                return HttpResponseRedirect(reverse("edit_student",kwargs={"student_id":student_id}))
        else:
            form=EditStudentForm(request.POST)
            student=Students.objects.get(admin=student_id)
            return render(request,"hod_template/edit_student_template.html",{"form":form,"id":student_id,"username":student.admin.username})



def edit_subject(request,subject_id):
    subject=Subjects.objects.get(id=subject_id)
    courses=Courses.objects.all()
    return render(request,"hod_template/edit_subject_template.html",{"subject":subject,"courses":courses,"id":subject_id})

def edit_subject_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_id=request.POST.get("subject_id")
        subject_name=request.POST.get("subject_name")
        course_id=request.POST.get("course")

        try:
            subject=Subjects.objects.get(id=subject_id)
            subject.subject_name=subject_name
            course=Courses.objects.get(id=course_id)
            subject.course_id=course
            subject.save()

            messages.success(request,"Successfully Edited Subject")
            return HttpResponseRedirect(reverse("edit_subject",kwargs={"subject_id":subject_id}))
        except:
            messages.error(request,"Failed to Edit Subject")
            return HttpResponseRedirect(reverse("edit_subject",kwargs={"subject_id":subject_id}))


def edit_course(request,course_id):
    course=Courses.objects.get(id=course_id)
    return render(request,"hod_template/edit_course_template.html",{"course":course,"id":course_id})

def edit_course_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        course_id=request.POST.get("course_id")
        course_name=request.POST.get("course")

        try:
            course=Courses.objects.get(id=course_id)
            course.course_name=course_name
            course.save()
            messages.success(request,"Successfully Edited Course")
            return HttpResponseRedirect(reverse("edit_course",kwargs={"course_id":course_id}))
        except:
            messages.error(request,"Failed to Edit Course")
            return HttpResponseRedirect(reverse("edit_course",kwargs={"course_id":course_id}))

def admin_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    return render(request,"hod_template/admin_profile.html",{"user":user})

def admin_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("admin_profile"))
    else:
        first_name=request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password=request.POST.get("password")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            if password!=None and password!="":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("admin_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("admin_profile"))

def add_notice(request):
    return render(request,"hod_template/add_notice_template.html")

def add_notice_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        message=request.POST.get("message")
        Academic_year=request.POST.get("Academic_year")
        try:
           notice=Notice(message=message,Academic_year=Academic_year)
           notice.save()
           messages.success(request,"Successfully Added Notice")
           return HttpResponseRedirect(reverse("add_notice"))
        except:
            messages.error(request,"Failed To Add Course")
            return HttpResponseRedirect(reverse("add_notice"))


def manage_notice(request):
    notices=Notice.objects.all().order_by('-Academic_year','-created_at')
    myFilter = noticeFilter(request.GET, queryset=notices)
    notices = myFilter.qs
    return render(request,"hod_template/manage_notice_template.html",{"notices":notices,"myFilter":myFilter})


def edit_notice(request,notice_id):
    notice = Notice.objects.get(id=notice_id)
    return render(request,"hod_template/edit_notice_template.html",{"notice":notice,"id":notice_id})

def edit_notice_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        notice_id=request.POST.get("notice_id")
        message=request.POST.get("message")
        Academic_year=request.POST.get("Academic_year")
        try:
            notice=Notice.objects.get(id=notice_id)
            notice.message=message
            notice.Academic_year=Academic_year
            notice.save()
            messages.success(request,"Successfully Edited Notice")
            return HttpResponseRedirect(reverse("edit_notice",kwargs={"notice_id":notice_id}))
        except:
            messages.error(request,"Failed to Edit Notice")
            return HttpResponseRedirect(reverse("edit_notice",kwargs={"notice_id":notice_id}))


def admin_add_test(request):
    form = forms.TestForm()
    return render(request,"hod_template/add_test_template.html",{"form":form})

def admin_add_test_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        form = forms.TestForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data["name"]
            subject_id=form.cleaned_data["subject_id"]
            course_id = form.cleaned_data[ "course_id" ]
            question_number = form.cleaned_data[ "question_number" ]
            total_marks = form.cleaned_data[ "total_marks" ]
            Academic_year=form.cleaned_data["Academic_year"]
            due = form.cleaned_data[ "due" ]
            complete=form.cleaned_data["complete"]
            try:
                test=Test()
                test.name=name
                subject_obj=Subjects.objects.get(id=subject_id)
                test.subject_id=subject_obj
                course_obj = Courses.objects.get(id=course_id)
                test.course_id=course_obj
                test.question_number=question_number
                test.total_marks=total_marks
                test.Academic_year=Academic_year
                test.due=due
                test.complete=complete
                test.save()
                messages.success(request,"Successfully Added Test")
                return HttpResponseRedirect(reverse("admin_add_test"))
            except:
                messages.error(request,"Failed to Add Test")
                return HttpResponseRedirect(reverse("admin_add_test"))
        else:
            form=forms.TestForm(request.POST)
    return render('request',"hod_template/add_test_template.html",{'form':form})

def admin_manage_test(request):
    test=Test.objects.all().order_by('-Academic_year','complete','due','name')
    myFilter = testFilter(request.GET, queryset=test)
    test = myFilter.qs
    return render(request,"hod_template/manage_test_template.html",{"test":test,"myFilter":myFilter})

def admin_edit_test(request,test_id):
    request.session['test_id']=test_id
    test=Test.objects.get(id=test_id)
    form=forms.EditTestForm()
    form.fields['name'].initial=test.name
    form.fields[ 'course_id' ].initial = test.course_id.id
    form.fields[ 'subject_id' ].initial = test.subject_id.id
    form.fields[ 'question_number' ].initial = test.question_number
    form.fields[ 'total_marks' ].initial = test.total_marks
    form.fields['Academic_year'].initial = test.Academic_year
    form.fields[ 'due' ].initial = test.due
    form.fields[ 'complete' ].initial = test.complete
    return render(request,"hod_template/edit_test_template.html",{"test":test,"form":form,"id":test_id})

def admin_edit_test_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        test_id=request.session.get("test_id")
        form=forms.EditTestForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            course_id = form.cleaned_data["course_id"]
            subject_id =form.cleaned_data["subject_id"]
            question_number = form.cleaned_data["question_number"]
            total_marks = form.cleaned_data["total_marks"]
            Academic_year = form.cleaned_data["Academic_year"]
            due = form.cleaned_data["due"]
            complete=form.cleaned_data['complete']
            try:
                test=Test.objects.get(id=test_id)
                course = Courses.objects.get(id=course_id)
                test.course_id=course
                subject = Subjects.objects.get(id=subject_id)
                test.subject_id=subject
                test.name = name
                test.question_number=question_number
                test.total_marks=total_marks
                test.Academic_year=Academic_year
                test.due=due
                test.complete=complete
                test.save()
                del request.session['test_id']
                messages.success(request,"Successfully Edited Test")
                return HttpResponseRedirect(reverse("admin_edit_test",kwargs={"test_id":test_id}))
            except:
                messages.error(request,"Failed to Edit Test")
                return HttpResponseRedirect(reverse("admin_edit_test",kwargs={"test_id":test_id}))
        else:
            form=forms.EditTestForm(request.POST)
            test=Test.objects.get(id=test_id)
            return render(request,"hod_template/edit_test_template.html",{"form":form,"id":test_id,"test":test,"name":test.name})

def admin_add_question(request):
    tests=Test.objects.all()
    return render(request,"hod_template/add_question_template.html",{"tests":tests})

def admin_add_question_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        Test_name=request.POST.get("test")
        test=Test.objects.get(id=Test_name)
        question=request.POST.get("question")
        question_type=request.POST.get("question_type")
        marks=request.POST.get("marks")
        Option1=request.POST.get("Option1")
        Option2=request.POST.get("Option2")
        Option3=request.POST.get("Option3")
        Option4=request.POST.get("Option4")
        answer=request.POST.get("answer")
        try:
            questions=Question(Test_name=test,question=question,question_type=question_type,marks=marks,Option1=Option1,Option2=Option2,Option3=Option3,Option4=Option4,answer=answer)
            questions.save()
            messages.success(request,"Successfully Added Question")
            return HttpResponseRedirect(reverse("admin_add_question"))
        except:
            messages.error(request,"Failed to Add Question")
            return HttpResponseRedirect(reverse("admin_add_question"))


def admin_manage_question(request):
    questions=Question.objects.all().order_by('-Test_name__Academic_year','Test_name__course_id__course_name','Test_name__name')
    myFilter = questionFilter(request.GET, queryset=questions)
    questions = myFilter.qs
    return render(request,"hod_template/manage_question_template.html",{"questions":questions,'myFilter':myFilter})

def admin_edit_question(request,question_id):
    questions=Question.objects.get(id=question_id)
    test=Test.objects.all()
    return render(request,"hod_template/edit_question_template.html",{"questions":questions,"test":test,"id":question_id})

def admin_edit_question_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        question_id=request.POST.get("question_id")
        Test_name = request.POST.get("test")
        question = request.POST.get("question")
        question_type = request.POST.get("question_type")
        marks = request.POST.get("marks")
        Option1 = request.POST.get("Option1")
        Option2 = request.POST.get("Option2")
        Option3 = request.POST.get("Option3")
        Option4 = request.POST.get("Option4")
        answer = request.POST.get("answer")
        try:
            questions=Question.objects.get(id=question_id)
            test = Test.objects.get(id=Test_name)
            questions.Test_name=test
            questions.question=question
            questions.question_type=question_type
            questions.Option1=Option1
            questions.Option2 = Option2
            questions.Option3 = Option3
            questions.Option4 = Option4
            questions.answer = answer
            questions.marks=marks
            questions.save()
            messages.success(request,"Successfully Edited Question")
            return HttpResponseRedirect(reverse("admin_edit_question",kwargs={"question_id":question_id}))
        except:
            messages.error(request,"Failed to Edit Question")
            return HttpResponseRedirect(reverse("admin_edit_question",kwargs={"question_id":question_id}))

def admin_question_view(request):
    return render(request,'hod_template/admin_question.html')

def admin_view_question_view(request):
    test= Test.objects.all().order_by('-Academic_year', 'complete', 'due','name')
    return render(request,'hod_template/admin_view_question.html',{'test':test})


def view_question_view(request,pk):
    questions=Question.objects.all().filter(Test_name=pk)
    myFilter = questionFilter(request.POST, queryset=questions)
    questions = myFilter.qs
    return render(request,'hod_template/view_question.html',{'questions':questions,'myFilter':myFilter})

def delete_question_view(request,pk):
    question=Question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect('/admin_view_question_view')


def delete_subject_view(request,pk):
    subject=Subjects.objects.get(id=pk)
    subject.delete()
    return HttpResponseRedirect('/manage_subject')

def delete_test_view(request,pk):
    test=Test.objects.get(id=pk)
    test.delete()
    return HttpResponseRedirect('/admin_manage_test')

def delete_student_view(request,pk):
    student=Students.objects.get(admin=pk)
    student.delete()
    return HttpResponseRedirect('/manage_student')

def delete_staff_view(request,pk):
    staff=Staffs.objects.get(admin=pk)
    staff.delete()
    return HttpResponseRedirect('/manage_staff')

def delete_notice_view(request,pk):
    notice=Notice.objects.get(id=pk)
    notice.delete()
    return HttpResponseRedirect('/manage_notice')

def admin_view_student_marks_view(request):
    students= Students.objects.all().order_by('-Academic_year','course_id__course_name','admin__last_name','admin__first_name')
    myFilter = studentFilter(request.GET, queryset=students)
    students = myFilter.qs
    return render(request,'hod_template/admin_view_student_marks.html',{'students':students,'myFilter':myFilter})

def admin_view_marks_view(request,pk):
    student= Students.objects.get(id=pk)
    course=student.course_id
    year=student.Academic_year
    test = Test.objects.all().order_by('complete', 'due','name').filter(course_id=course).filter(Academic_year=year)
    myFilter = testFilter(request.GET, queryset=test)
    test = myFilter.qs
    response = render(request,'hod_template/admin_view_marks.html',{'test':test,'myFilter':myFilter})
    response.set_cookie('student_id', str(pk))
    return response

def admin_check_marks_view(request,pk):
    student_id = request.COOKIES.get('student_id')
    student = Students.objects.get(id=student_id)
    test=Test.objects.get(id=pk)
    results = Result.objects.all().filter(student=student).filter(exam=test)
    questions = Question.objects.all().filter(Test_name=test)

    total_marks = 0
    for q in questions:
        total_marks += q.marks
    return render(request,'hod_template/admin_check_marks.html',{'results':results,'student':student,'total_marks':total_marks})

def delete_admin_marks_view(request,pk):
    result=Result.objects.get(id=pk)
    result.delete()
    return HttpResponseRedirect('/admin_view_student_marks_view')