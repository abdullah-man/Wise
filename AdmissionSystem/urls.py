from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
#--------------------- Login Logout UserProfile --------------------------------

    path('login/',views.loginpageview,name='loginpageview'),
    path('logout/',views.logoutUser,name='logout'),
    path('user_profile/', views.user_profile, name='user_profile'),
 
 
#-------------------- Main Views -----------------------------------------------
    # main
    path('',views.homeview,name='homeview'),
    path('addskillstudentview/',views.addskillstudentview,name='addskillstudentview'),
    path('addshortcoursetaken/<int:student_id>/',views.shortcoursetakenview,name='shortcoursetaken'),
    path('addshortcoursename/',views.shortcoursenameview,name='shortcoursenameview'),
    path('addjobview/<int:student_id>/',views.jobview,name='jobview'),
    path('addjobposition/',views.jobpositionview,name='jobpositionview'),
    path('add_query/<int:student_id>/',views.add_query,name='add_query'), 
    # view student details 
    path('skill_student_detail_view/<int:student_id>/',views.skill_student_detail_view,name='skill_student_detail_view'),
    path('add_document_type/', views.document_type_view, name='document_type_view'),
    path('add_pre_qualification/', views.pre_qualification_view, name='prequalificationview'),
    path('add_student_availability/<int:student_id>/', views.student_availability_view, name='studentavailabilityview'),
    path('add_course_conducting_body/', views.course_conducting_body_view, name='courseconductingbodyview'),
    path('add_course_name/', views.course_name_view, name='coursenameview'),


#----------------------- Delete Skill Students -----------------------
 
    path('delete_skillstudent/<int:id>/',views.delete_skill_student,name='delete_skill_student'),
    path('delete_shortcoursetaken/<int:id>/<int:student_id>/',views.delete_shortcoursetaken,name='delete_shortcoursetaken'),
    path('delete_job/<int:job_id>/<int:student_id>/',views.delete_job,name='delete_job'),
    path('delete_job_position/<int:job_position_id>/',views.delete_job_position,name='delete_job_position'),
    path('delete_document_type/<int:document_type_id>/',views.delete_document_type,name='delete_doctype'),
    path('delete_pre_qualification/<int:pre_qualification_id>/',views.delete_pre_qualification,name='delete_prequalification'),
    # path('delete_query/<int:query_id>/<int:student_id>/',views.delete_query,name='delete_query'),
    path('delete_course_conducting_body/<int:course_conducting_body_id>/',views.delete_course_conducting_body,name='delete_courseconductingbody'),
    path('delete_course_name/<int:course_name_id>/',views.delete_course_name,name='delete_coursename'),


#----------------------------- Update --------------------------------

    path('update_skill_student/<int:student_id>/',views.update_skill_student,name='update_skill_student'), 
    path('update_current_study/<int:student_id>/',views.update_current_study,name='update_current_study'),
    path('update_shortcourse_taken/<int:id>/',views.update_shortcourse_taken,name='update_shortcourse_taken'),
    path('update_job/<int:id>/',views.update_job,name='update_job'),
    path('update_phone_no/<int:id>/',views.update_phone_no,name='update_phone_no'),
    path('update_query/<int:id>/',views.update_query,name='update_query'),
    path('modify_skill_dashboard/',views.modify_skill_dashboard,name='modify_skill_dashboard'),
    path('update_job_position/<int:id>/',views.update_job_position,name='update_job_position'),
    path('update_shortcourse_name/<int:id>/',views.update_shortcourse_name,name='update_shortcourse_name'),
    # update student details using modify 
    path('update_skill_detail_view/<int:student_id>/',views.update_skill_detail_view,name='update_skill_detail_view'),
    path('update_document_type/<int:document_type_id>/',views.update_document_type,name='updatedocumenttype'),
    path('update_pre_qualification/<int:pre_qualification_id>/',views.update_pre_qualification,name='update_prequalification'),
    path('update_student_availability/<int:availability_id>/', views.update_student_availability, name='update_studentavailability'),
    path('update_course_conducting_body/<int:course_conducting_body_id>/',views.update_course_conducting_body,name='updatecourseconductingbody'),
    path('update_course_name/<int:course_name_id>/',views.update_course_name,name='updatecoursename'),



#-------------------------------------- Dashboard --------------------------------

    path('job_position_dashboard/',views.job_position_dashboard,name='job_position_dashboard'),
    path('shortcourse_name_dashboard/',views.shortcourse_name_dashboard,name='shortcourse_name_dashboard'),
    path('search_skill_dashboard/',views.search_skill_dashboard,name='search_skill_dashboard'),
    path('document_type_dashboard/',views.document_type_dashboard,name='documenttypedashboard'),
    path('pre_qualification_dashboard/',views.pre_qualification_dashboard,name='prequalificationdashboard'),
    path('course_conducting_body_dashboard/',views.course_conducting_body_dashboard,name='courseconductingbodydashboard'),
    path('course_name_dashboard/',views.course_name_dashboard,name='coursenamedashboard'),


]

