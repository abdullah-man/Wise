from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
#--------------------- Login Logout UserProfile --------------------------------

    path('login/',views.loginpageview,name='loginpageview'),
    path('logout/',views.logoutUser,name='logout'),
    path('user_profile/', views.user_profile, name='user_profile'),
 
 
#------------------------- Main Views ----------------------
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
    path('add_course_batch_no/', views.course_batch_no_view, name='coursebatchnoview'),
    path('add_shift_name/', views.shift_name_view, name='shiftnameview'),
    path('add_course_section/', views.course_section_view, name='coursesectionview'),
    path('add_already_registered_with_course_body/<int:student_id>/', views.already_regitered_with_course_body_view, name='alreadyregisteredwithcoursebodyview'),
    path('add_document/<int:student_id>/', views.document_view, name='documentview'),
    path('download_document/<int:document_id>/', views.download_document, name='downloadview'),
    path('add_course_application/<int:student_id>/', views.course_application_view, name='courseapplicationview'),


#--------------------------- Delete -----------------------
 
    path('delete_skillstudent/<int:id>/',views.delete_skill_student,name='delete_skill_student'),
    path('delete_shortcoursetaken/<int:id>/<int:student_id>/',views.delete_shortcoursetaken,name='delete_shortcoursetaken'),
    path('delete_job/<int:job_id>/<int:student_id>/',views.delete_job,name='delete_job'),
    path('delete_job_position/<int:job_position_id>/',views.delete_job_position,name='delete_job_position'),
    path('delete_document_type/<int:document_type_id>/',views.delete_document_type,name='delete_doctype'),
    path('delete_pre_qualification/<int:pre_qualification_id>/',views.delete_pre_qualification,name='delete_prequalification'),
    # path('delete_query/<int:query_id>/<int:student_id>/',views.delete_query,name='delete_query'),
    path('delete_course_conducting_body/<int:course_conducting_body_id>/',views.delete_course_conducting_body,name='delete_courseconductingbody'),
    path('delete_course_name/<int:course_name_id>/',views.delete_course_name,name='delete_coursename'),
    path('delete_course_batch_no/<int:course_batch_id>/',views.delete_course_batch_no,name='delete_coursebatchno'),
    path('delete_shift_name/<int:shift_name_id>/',views.delete_shift_name,name='delete_shiftname'),
    path('delete_course_section/<int:course_section_id>/',views.delete_course_section,name='delete_coursesection'),
    path('delete_already_registered_with_course_body/<int:already_registered_id>/',views.delete_already_regitered_with_course_body,name='delete_alreadyregisteredwithcoursebody'),
    path('delete_document/<int:document_id>/', views.delete_document, name='delete_document'),
    path('delete_course_application/<int:application_id>/', views.delete_course_application, name='delete_courseapplication'),


#----------------------------- Update ----------------------

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
    path('update_course_batch_no/<int:course_batch_id>/',views.update_course_batch_no,name='updatecoursebatchno'),
    path('update_shift_name/<int:shift_name_id>/',views.update_shift_name,name='updateshiftname'),
    path('update_course_section/<int:course_section_id>/',views.update_course_section,name='updatecoursesection'),
    path('update_already_registered_with_course_body/<int:already_registered_id>/',views.update_already_regitered_with_course_body,name='updatealreadyregisteredwithcoursebody'),
    path('update_document/<int:document_id>/',views.update_document,name='updatedocument'),
    path('update_course_application/<int:application_id>/',views.update_course_application,name='updatecourseapplication'),



#-------------------------------------- Dashboard --------------------------------

    path('job_position_dashboard/',views.job_position_dashboard,name='job_position_dashboard'),
    path('shortcourse_name_dashboard/',views.shortcourse_name_dashboard,name='shortcourse_name_dashboard'),
    path('search_skill_dashboard/',views.search_skill_dashboard,name='search_skill_dashboard'),
    path('document_type_dashboard/',views.document_type_dashboard,name='documenttypedashboard'),
    path('pre_qualification_dashboard/',views.pre_qualification_dashboard,name='prequalificationdashboard'),
    path('course_conducting_body_dashboard/',views.course_conducting_body_dashboard,name='courseconductingbodydashboard'),
    path('course_name_dashboard/',views.course_name_dashboard,name='coursenamedashboard'),
    path('course_batch_no_dashboard/',views.course_batch_no_dashboard,name='coursebatchnodashboard'),
    path('shift_name_dashboard/',views.shift_name_dashboard,name='shiftnamedashboard'),
    path('course_section_dashboard/',views.course_section_dashboard,name='coursesectiondashboard'),
    path('document_dashboard/<int:student_id>/',views.document_dashboard,name='documentdashboard'),


]

