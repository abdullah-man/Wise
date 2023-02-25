# This file contains functions that are being used in views.
# For better readability in views and code maintenance, these functions are being kept here.
# Also, these functions are called many times in views, therefore, these are refactored here.
# This makes views.py less cluttered space.
#   - generate_context : generates context for search and modify dashboards
#   - delete_object : deletes an object while performing relevant checks and exception handling
#   - create_object : adds an object while performing relevant checks and exception handling
#

from .models import *


def generate_context(skillstudentobjects):
		"""
			Creates context for a view. Context is comprising of student data
			for both post and get requests on search_skill_dashboard.
		"""
		
		# getting all skill student objects
		skillstudentobjects=SkillStudent.objects.all()
		# 
		
		
		
		all_std_data = list()
		
		for std in skillstudentobjects:
			std_data = list()	
			std_data.append(std.id)
			std_data.append(std.name)
			
			if (std.cnic is None) or (std.cnic ==""):
				std_data.append(std.b_form)
			else:
				std_data.append(std.cnic)
			
			# getting personal phone details of the respective student
			phone_object = PhoneNo.objects.get(student_id=std.id)
			std_data.append(phone_object.personal_phone_no_1)
		
			# program/course_name -- one student can apply for multiple prgrams
			all_applicaitons_of_student = CourseApplication.objects.filter(student_id=std.id)
			
			course_html = ""
			for application in all_applicaitons_of_student.iterator():
				course_name = application.course_name
				course_html = course_html+f"{course_name}\n"
			std_data.append(course_html)

			# stauts -- each program application has different status
			status_html = ""
			for application in all_applicaitons_of_student.iterator():
				admission_status = application.admission_status
				status_html = status_html+f"{admission_status}\n"
			std_data.append(status_html)
			

			# date applied -- each program application has its own date
			date_html = ""
			for application in all_applicaitons_of_student.iterator():
				date_applied = application.date_applied
				date_html = date_html+f"{date_applied}\n"
			std_data.append(date_html)

			# already registered -- one student can be already registered with multiple course bodies
			all_already_applied_of_student = AlreadyRegisteredWithCourseBody.objects.filter(student_id=std.id)
			
			already_html = ""
			for body_details in all_already_applied_of_student.iterator():
				body_id = body_details.course_body_id
				# getting the body name from CourseConductingBody table using its id
				body_object = CourseConductingBody.objects.get(id=body_id)
				body_name = body_object.course_conducting_body_name
				already_html = already_html + f"{body_name}\n"
			std_data.append(already_html)
			
			# appending student to all student's data
			all_std_data.append(std_data)

		return all_std_data
