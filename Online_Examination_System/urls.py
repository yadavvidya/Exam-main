"""studentsystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from student import views, HodViews
from student import StaffViews
from student import StudentViews
from django.conf import settings

urlpatterns = [
    path('admin/',admin.site.urls),
    path('signup_student',views.signup_student,name="signup_student"),
    path('do_student_signup',views.do_student_signup,name="do_student_signup"),
    path('accounts/',include('django.contrib.auth.urls')),
    path('',views.index,name="index"),
    path('login',views.ShowLoginPage,name="login"),
    path('doLogin',views.doLogin,name="do_login"),
    path('get_user_details',views.GetUserDetails),
    path('logout_user',views.logout_user,name="logout"),

    #admin urls
    path('admin_home',HodViews.admin_home,name="admin_home"),
    path('add_staff',HodViews.add_staff,name="add_staff"),
    path('add_staff_save',HodViews.add_staff_save,name="add_staff_save"),
    path('add_course',HodViews.add_course,name="add_course"),
    path('add_course_save',HodViews.add_course_save,name="add_course_save"),
    path('add_student',HodViews.add_student,name="add_student"),
    path('add_student_save',HodViews.add_student_save,name="add_student_save"),
    path('add_subject', HodViews.add_subject, name="add_subject"),
    path('admin_add_test',HodViews.admin_add_test,name="admin_add_test"),
    path('admin_add_test_save',HodViews.admin_add_test_save,name="admin_add_test_save"),
    path('admin_add_question',HodViews.admin_add_question,name="admin_add_question"),
    path('admin_add_question_save',HodViews.admin_add_question_save,name="admin_add_question_save"),
    path('add_notice',HodViews.add_notice,name="add_notice"),
    path('add_notice_save',HodViews.add_notice_save,name="add_notice_save"),
    path('add_subject_save',HodViews.add_subject_save,name="add_subject_save"),
    path('manage_staff',HodViews.manage_staff,name="manage_staff"),
    path('manage_student', HodViews.manage_student,name="manage_student"),
    path('manage_course', HodViews.manage_course,name="manage_course"),
    path('manage_notice', HodViews.manage_notice,name="manage_notice"),
    path('manage_subject', HodViews.manage_subject,name="manage_subject"),
    path('admin_manage_test', HodViews.admin_manage_test,name="admin_manage_test"),
    path('admin_manage_question', HodViews.admin_manage_question,name="admin_manage_question"),
    path('edit_staff/<str:staff_id>', HodViews.edit_staff,name="edit_staff"),
    path('edit_staff_save', HodViews.edit_staff_save,name="edit_staff_save"),
    path('edit_student/<str:student_id>', HodViews.edit_student,name="edit_student"),
    path('edit_student_save', HodViews.edit_student_save,name="edit_student_save"),
    path('edit_subject/<str:subject_id>', HodViews.edit_subject,name="edit_subject"),
    path('edit_subject_save', HodViews.edit_subject_save,name="edit_subject_save"),
    path('admin_edit_test/<str:test_id>', HodViews.admin_edit_test,name="admin_edit_test"),
    path('admin_edit_test_save', HodViews.admin_edit_test_save,name="admin_edit_test_save"),
    path('admin_edit_question/<str:question_id>', HodViews.admin_edit_question,name="admin_edit_question"),
    path('admin_edit_question_save', HodViews.admin_edit_question_save,name="admin_edit_question_save"),
    path('edit_course/<str:course_id>', HodViews.edit_course,name="edit_course"),
    path('edit_course_save', HodViews.edit_course_save,name="edit_course_save"),
    path('edit_notice/<str:notice_id>', HodViews.edit_notice,name="edit_notice"),
    path('edit_notice_save', HodViews.edit_notice_save,name="edit_notice_save"),
    path('admin_profile',HodViews.admin_profile,name="admin_profile"),
    path('admin_profile_save',HodViews.admin_profile_save,name="admin_profile_save"),

    path('admin_question_view', HodViews.admin_question_view,name='admin_question_view'),
    path('admin_view_question_view', HodViews.admin_view_question_view,name='admin_view_question_view'),
    path('view_question/<int:pk>', HodViews.view_question_view,name='view_question_view'),
    path('delete_question/<int:pk>', HodViews.delete_question_view,name='delete_question'),

    path('admin_view_student_marks_view', HodViews.admin_view_student_marks_view,name='admin_view_student_marks'),
    path('admin_view_marks_view/<int:pk>', HodViews.admin_view_marks_view,name='admin_view_marks_view'),
    path('admin_check_marks_view/<int:pk>', HodViews.admin_check_marks_view,name='admin_check_marks_view'),


    path('delete_subject_view/<int:pk>', HodViews.delete_subject_view,name='delete_subject_view'),
    path('delete_test_view/<int:pk>', HodViews.delete_test_view,name='delete_test_view'),
    path('delete_student_view/<int:pk>', HodViews.delete_student_view,name='delete_student_view'),
    path('delete_staff_view/<int:pk>', HodViews.delete_staff_view,name='delete_staff_view'),
    path('delete_notice_view/<int:pk>', HodViews.delete_notice_view, name='delete_notice_view'),
    path('delete_marks/<int:pk>', HodViews.delete_admin_marks_view, name='delete_marks'),

                  #exam department urls
    path('staff_home', StaffViews.staff_home, name="staff_home"),
    path('staff_manage_student', StaffViews.staff_manage_student,name="staff_manage_student"),
    path('staff_manage_student', StaffViews.staff_manage_student, name="staff_manage_student"),
    path('view_staff', StaffViews.view_staff, name="view_staff"),
    path('view_course', StaffViews.view_course, name="view_course"),
    path('view_subject',StaffViews.view_subject,name="view_subject"),
    path('staff_profile',StaffViews.staff_profile,name="staff_profile"),
    path('staff_profile_save',StaffViews.staff_profile_save,name="staff_profile_save"),
    path('staff_add_test', StaffViews.staff_add_test, name="staff_add_test"),
    path('staff_add_test_save', StaffViews.staff_add_test_save, name="staff_add_test_save"),
    path('staff_manage_test', StaffViews.staff_manage_test,name="staff_manage_test"),
    path('staff_edit_test/<str:test_id>', StaffViews.staff_edit_test,name="staff_edit_test"),
    path('staff_edit_test_save', StaffViews.staff_edit_test_save,name="staff_edit_test_save"),

    path('staff_manage_question', StaffViews.staff_manage_question,name="staff_manage_question"),
    path('staff_add_question', StaffViews.staff_add_question, name="staff_add_question"),
    path('staff_add_question_save', StaffViews.staff_add_question_save, name="staff_add_question_save"),
    path('staff_edit_question/<str:question_id>', StaffViews.staff_edit_question,name="staff_edit_question"),
    path('staff_edit_question_save', StaffViews.staff_edit_question_save, name="staff_edit_question_save"),
    path('staff_question_view', StaffViews.staff_question_view, name='staff_question_view'),
    path('staffs_view_question_view', StaffViews.staffs_view_question_view, name='staff_view_question_view'),
    path('staff_view_question_view/<int:pk>', StaffViews.staff_view_question_view, name='staff_view_question_view'),
    path('staff_delete_question_view/<int:pk>', StaffViews.staff_delete_question_view, name='staff_delete_question_view'),
    path('staff_delete_test/<int:pk>', StaffViews.staff_delete_test,name='staff_delete_test'),

    path('staff_view_student_marks_view', StaffViews.staff_view_student_marks_view,name='staff_view_student_marks_view'),
    path('staff_view_marks_view/<int:pk>', StaffViews.staff_view_marks_view,name='staff_view_marks_view'),
    path('staff_check_marks_view/<int:pk>', StaffViews.staff_check_marks_view,name='staff_check_marks_view'),
    path('staff_view_notice', StaffViews.staff_view_notice, name="staff_view_notice"),

                  #student urls
    path('student_home', StudentViews.student_home, name="student_home"),
    path('student_profile/', StudentViews.student_profile, name="student_profile"),
    path('student_profile_save',StudentViews.student_profile_save,name="student_profile_save"),
    path('view_notice',StudentViews.view_notice,name="view_notice"),

    path('student_exam_view', StudentViews.student_exam_view,name='student_exam_view'),
    path('take-exam/<int:pk>', StudentViews.take_exam_view,name='take-exam'),
    path('start-exam/<int:pk>', StudentViews.start_exam_view,name='start-exam'),

    path('calculate_marks_view', StudentViews.calculate_marks_view,name='calculate_marks_view'),
    path('view-result', StudentViews.view_result_view,name='view-result'),
    path('check_marks/<int:pk>', StudentViews.check_marks_view,name='check_marks'),
    path('student_marks_view', StudentViews.student_marks_view,name='student_marks_view'),
    path('student_view_subject',StudentViews.student_view_subject,name='student_view_subject'),
    ]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
