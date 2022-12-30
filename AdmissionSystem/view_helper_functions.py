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
			This is an inner function to create context comprising of student data
			for both post and get requests on search_skill_dashboard.
		"""
		all_std_data = list()
		
		for std in skillstudentobjects:
			std_data = list()	
			std_data.append(std.id)
			std_data.append(std.name)
			std_data.append(std.cnic)
			std_data.append("")
			std_data.append("")
			std_data.append("")
			std_data.append("")
			
			# getting personal phone details of the respective student
			std_id = std.id
			query = f"SELECT * FROM AdmissionSystem_phoneno WHERE student_id={std_id}"
		    # print(query)
			# print(std_id)
			
			personal_phone_number_1_of_student = ''

			for phone_obj in PhoneNo.objects.raw(query):
				if phone_obj.personal_phone_no_1 is None:
					continue
				else:
					personal_phone_number_1_of_student = personal_phone_number_1_of_student + phone_obj.personal_phone_no_1

			std_data.append(personal_phone_number_1_of_student)
			all_std_data.append(std_data)

		return all_std_data
