from django import forms

from student import models
from student.models import Courses, Subjects, Test


class DateInput(forms.DateInput):
    input_type = "date"

class DateTimeInput(forms.TimeInput):
    input_type = "time"

class AddStudentForm(forms.Form):
    email=forms.EmailField(label="Email",widget=forms.EmailInput(attrs={"class":"form-control"}))
    password=forms.CharField(label="Password",max_length=50,widget=forms.PasswordInput(attrs={"class":"form-control"}))
    first_name=forms.CharField(label="First Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name=forms.CharField(label="Last Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    username=forms.CharField(label="Username",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    pnr=forms.CharField(label="Enrollment No",max_length=16,widget=forms.TextInput(attrs={"class":"form-control"}))
    address=forms.CharField(label="Address",max_length=255,widget=forms.TextInput(attrs={"class":"form-control"}))
    dob=forms.DateField(label="DOB",widget=DateInput(attrs={"class":"form-control"}))
    courses=Courses.objects.all()
    course_list=[]
    for course in courses:
        small_course=(course.id,course.course_name)
        course_list.append(small_course)

    gender_choice=(
        ("Male","Male"),
        ("Female","Female"),
        ("Other", "Other"),
    )

    course=forms.ChoiceField(label="Course",choices=course_list,widget=forms.Select(attrs={"class":"form-control"}))
    gender=forms.ChoiceField(label="Sex",choices=gender_choice,widget=forms.Select(attrs={"class":"form-control"}))
    profile_pic=forms.FileField(label="Profile Pic",max_length=50,widget=forms.FileInput(attrs={"class":"form-control"}))
    Academic_year=forms.DateField(label="Academic Start Date",widget=DateInput(attrs={"class":"form-control"}))

class EditStudentForm(forms.Form):
    email=forms.EmailField(label="Email",widget=forms.EmailInput(attrs={"class":"form-control"}))
    first_name=forms.CharField(label="First Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name=forms.CharField(label="Last Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    username=forms.CharField(label="Username",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    pnr=forms.CharField(label="Enrollment No",max_length=16,widget=forms.TextInput(attrs={"class":"form-control"}))
    address=forms.CharField(label="Address",max_length=255,widget=forms.TextInput(attrs={"class":"form-control"}))
    dob = forms.DateField(label="DOB", widget=DateInput(attrs={"class": "form-control"}))

    courses=Courses.objects.all()
    course_list=[]
    for course in courses:
        small_course=(course.id,course.course_name)
        course_list.append(small_course)

    gender_choice=(
        ("Male","Male"),
        ("Female","Female"),
        ("Other","Other"),
    )

    course=forms.ChoiceField(label="Course",choices=course_list,widget=forms.Select(attrs={"class":"form-control"}))
    gender=forms.ChoiceField(label="Sex",choices=gender_choice,widget=forms.Select(attrs={"class":"form-control"}))
    profile_pic=forms.FileField(label="Profile Pic",max_length=255,widget=forms.FileInput(attrs={"class":"form-control"}),required=False)
    Academic_year = forms.DateField(label="Academic Start Date", widget=DateInput(attrs={"class": "form-control"}))

class TestForm(forms.ModelForm):
    courses = Courses.objects.all()
    course_list = [ ]
    for course in courses:
        small_course = (course.id, course.course_name)
        course_list.append(small_course)

    subjects = Subjects.objects.all()
    subject_list = [ ]
    for subject in subjects:
        small_subject = (subject.id, subject.subject_name)
        subject_list.append(small_subject)
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter Test Name',"class":"form-control"}))
    subject_id=forms.ChoiceField(label="Subject",choices=subject_list,widget=forms.Select(attrs={"class":"form-control"}))
    course_id =forms.ChoiceField(label="Course",choices=course_list,widget=forms.Select(attrs={"class":"form-control"}))
    question_number = forms.IntegerField(label="No. of Questions",widget=forms.NumberInput(attrs={"class":"form-control"}))
    total_marks = forms.IntegerField(label="Total Marks",widget=forms.NumberInput(attrs={"class":"form-control"}))
    due =forms.DateField(label="Due",widget=DateInput(attrs={"class":"form-control"}))
    Academic_year = forms.DateField(label="Academic Start Date",widget=DateInput(attrs={"class":"form-control"}))
    start_time = forms.TimeField(label="Exam Start Time",widget=DateTimeInput(attrs={"class":"form-control"}))
    end_time = forms.TimeField(label="Exam End Time",widget=DateTimeInput(attrs={"class":"form-control"}))

    class Meta:
        model=models.Test
        fields=['name','question_number','total_marks','Academic_year','due','complete','start_time','end_time']

class EditTestForm(forms.ModelForm):
    courses = Courses.objects.all()
    course_list = [ ]
    for course in courses:
        small_course = (course.id, course.course_name)
        course_list.append(small_course)

    subjects = Subjects.objects.all()
    subject_list = [ ]
    for subject in subjects:
        small_subject = (subject.id, subject.subject_name)
        subject_list.append(small_subject)
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Test Name', "class": "form-control"}))
    subject_id = forms.ChoiceField(label="Subject", choices=subject_list,widget=forms.Select(attrs={"class": "form-control"}))
    course_id = forms.ChoiceField(label="Course", choices=course_list,widget=forms.Select(attrs={"class": "form-control"}))
    question_number = forms.IntegerField(label="No. of Questions",widget=forms.NumberInput(attrs={"class": "form-control"}))
    total_marks = forms.IntegerField(label="Total Marks", widget=forms.NumberInput(attrs={"class": "form-control"}))
    due =forms.DateField(label="Due",widget=DateInput(attrs={"class":"form-control"}))
    Academic_year = forms.DateField(label="Academic Start Date",widget=DateInput(attrs={"class":"form-control"}))
    start_time = forms.TimeField(label="Exam Start Time", widget=DateTimeInput(attrs={"class": "form-control"}))
    end_time = forms.TimeField(label="Exam End Time", widget=DateTimeInput(attrs={"class": "form-control"}))
    class Meta:
        model=models.Test
        fields=['name','question_number','total_marks','Academic_year','due','complete','start_time','end_time']