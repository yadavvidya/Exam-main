import django_filters

from . import forms
from .models import *

class DateTimeInput(forms.DateInput):
    input_type = "date"


class staffFilter(django_filters.FilterSet):
    staff = Staffs.objects.all()
    staff_list = [ ]
    for staff in staff:
        small_staff = (staff.admin.id, staff.admin)
        staff_list.append(small_staff)
    staff_id = django_filters.CharFilter(label="Staff ID", lookup_expr='icontains')
    address=django_filters.CharFilter(label="Address",lookup_expr='icontains')


class studentFilter(django_filters.FilterSet):
    gender_choice = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    )
    courses = Courses.objects.all()
    course_list = [ ]
    for course in courses:
        small_course = (course.id, course.course_name)
        course_list.append(small_course)

    student = Students.objects.all()
    student_list = [ ]
    for student in student:
        small_student = (student.admin.id, student.admin)
        student_list.append(small_student)
    pnr=django_filters.CharFilter(label="Enrollment No",lookup_expr='icontains')
    gender = django_filters.ChoiceFilter(choices=gender_choice)
    dob = django_filters.DateFilter(label="DOB",widget=DateTimeInput)
    Academic_year=django_filters.DateFilter(label="Academic Start Date",widget=DateTimeInput)
    course_id=django_filters.ChoiceFilter(label="Course",choices=course_list)
    address=django_filters.CharFilter(label="Address",lookup_expr='icontains')

class questionFilter(django_filters.FilterSet):
    test = Test.objects.all()
    test_list = [ ]
    for test in test :
        small_test = (test.id, test.name)
        test_list.append(small_test)

    question_choice = (
        ("MCQ", "MCQ"),
        ("True_False", "True_False"),
    )

    cat = (
        ("Option1", "Option1"),
        ("Option2", "Option2"),
        ("Option3", "Option3"),
        ("Option4", "Option4")
    )


    Test_name = django_filters.ChoiceFilter(choices=test_list)
    marks=django_filters.NumberFilter(label="Marks")
    question_type=django_filters.ChoiceFilter(choices=question_choice)
    Option1=django_filters.CharFilter(label="Option 1",lookup_expr='icontains')
    Option2 = django_filters.CharFilter(label="Option 2",lookup_expr='icontains')
    Option3 = django_filters.CharFilter(label="Option 3",lookup_expr='icontains')
    Option4 = django_filters.CharFilter(label="Option 4",lookup_expr='icontains')
    answer=django_filters.ChoiceFilter(label="Correct Option",choices=cat)

class testFilter(django_filters.FilterSet):
    courses = Courses.objects.all()
    course_list = [ ]
    for course in courses:
        small_course = (course.id, course.course_name)
        course_list.append(small_course)

    subjects = Subjects.objects.all()
    subject_list = [ ]
    for subject in subjects:
        small_subject = (subject.id,subject.subject_name)
        subject_list.append(small_subject)

    course_id = django_filters.ChoiceFilter(label="Course",choices=course_list)
    subject_id = django_filters.ChoiceFilter(label="Subject",choices=subject_list)
    question_number = django_filters.NumberFilter(label="No.of Questions",lookup_expr='exact')
    total_marks = django_filters.NumberFilter(lookup_expr='exact')
    due =django_filters.DateFilter(label="Due",widget=DateTimeInput())
    complete=django_filters.BooleanFilter()
    Academic_year=django_filters.DateFilter(label="Academic Start Date",widget=DateTimeInput())

class courseFilter(django_filters.FilterSet):
    course_name=django_filters.CharFilter(label="Course",lookup_expr='icontains')

class subjectFilter(django_filters.FilterSet):
    courses = Courses.objects.all()
    course_list = [ ]
    for course in courses:
        small_course = (course.id, course.course_name)
        course_list.append(small_course)
    subject_name=django_filters.CharFilter(label="Subject",lookup_expr='icontains')
    course_id = django_filters.ChoiceFilter(choices=course_list)

class noticeFilter(django_filters.FilterSet):
    message=django_filters.CharFilter(label="Notice",lookup_expr='icontains')
    Academic_year=django_filters.DateFilter(label="Academic Start Date",widget=DateTimeInput())


class resultFilter(django_filters.FilterSet):
    test = Test.objects.all()
    test_list = [ ]
    for test in test:
        small_test = (test.id, test.name)
        test_list.append(small_test)
    exam = django_filters.ChoiceFilter(choices=test_list)