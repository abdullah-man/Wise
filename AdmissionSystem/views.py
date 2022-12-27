from .models import *
from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required

 
# ----------------------------------------------------------------------------------------
# 							LOGIN / LOGOUT
# ----------------------------------------------------------------------------------------

def loginpageview(request):
	"""
		Login page view. Shows login.html on Get request.
		On Post request, authenticates user information and 
		redirects to home.
	"""
	if request.method=='POST':
		username=request.POST.get('username')
		password=request.POST.get('password')
		user=authenticate(request,username=username,password=password)
		if user is not None:
			login (request,user)
			# putting the currently logged-in user into the session
			request.session['current-user-username'] = user.username
			return redirect('homeview')
		else:
			messages.info(request,'Username or Password incorrect')
	context={}
	return render(request,'login.html',context)


@login_required(login_url='loginpageview')
def logoutUser(request):
	"""
		Logs-out the logged-in user and redirects to login page.
	"""
	logout(request)
	return redirect('loginpageview')


# ------------------------------------------------------------------------------------------
#									MAIN VIEWS 
# ------------------------------------------------------------------------------------------


@login_required(login_url='loginpageview')
def homeview(request):
	"""
		Main page view. Displays total number of skill and conventional students.
	"""

	# getting all skill student objects count
	skillstudentcount=SkillStudent.objects.all().count()
	
	context={'skillstudentcount':skillstudentcount}
	return render(request=request, template_name="home.html",context=context)


@login_required(login_url='loginpageview')
def addskillstudentview(request):
	"""
		On Get request, this view displays empty skill_student_form that is to be filled.
		On Post request, it saves skill_student_form and creates empty objects 
		for this user in these tables as a student's id is saved as a foreign key 
		in these tables under student_id field.
			- CurrentStudy
			- ShortCoursesTaken
			- PhoneNo
			- Job
		So, a student's object cannot be completey created unless these tables are also
		populated with its information though with empty strings.
	"""

	if request.method == "POST":
		print("0")
		add_skill_student_form = AddSkillStudentForm(request.POST)
		print("1")
		
		if add_skill_student_form.is_valid():
			print("2")
			# getting the filled data 
			name = add_skill_student_form.cleaned_data['name']
			personal_phone_no_1 = add_skill_student_form.cleaned_data['personal_phone_no_1']
			personal_phone_no_2 = add_skill_student_form.cleaned_data['personal_phone_no_2']
			area = add_skill_student_form.cleaned_data['area']
			laptop = add_skill_student_form.cleaned_data['laptop']
			availability_from = add_skill_student_form.cleaned_data['availability_from']
			availabitity_to = add_skill_student_form.cleaned_data['availabitity_to']
			date_applied = add_skill_student_form.cleaned_data['date_applied']
			pre_qualification = add_skill_student_form.cleaned_data['pre_qualification']
			currently_studying = add_skill_student_form.cleaned_data['currently_studying']
			admission_status = add_skill_student_form.cleaned_data['admission_status']			
			

			# pre-qualification is a ModelMultipleChoiceField whereas pre_qualification is 
			# a query-set. To get the relevant object from it, we use first()
			pre_qualification = pre_qualification.first()

			

			data_list = [name, personal_phone_no_1, personal_phone_no_2, area, laptop, availability_from, availabitity_to, date_applied, pre_qualification, currently_studying, admission_status]
			
			print("Data List: ", data_list)

			# --- 		Writing data to respective Models 		---
			# -----------------------------------------------------	

			# skillstudent Model object creation
			SkillStudent.objects.create(name=name, area=area, laptop=laptop, pre_qualification=pre_qualification, created_by=request.user)
			
			# getting id of the most recently registered student by this user to get student_id of this student
			students_of_this_user = SkillStudent.objects.filter(created_by=request.user).order_by('id')
			newly_added_student = students_of_this_user.last() # gettting the newly created user
			newly_added_student_id = newly_added_student.id # getting its id

			print("------ id : ",newly_added_student.id)

			# CurrentStudy Model object creation
			CurrentStudy.objects.create(student_id=newly_added_student_id, program=currently_studying, created_by=request.user)

			# PhoneNo Model object creation
			PhoneNo.objects.create(student_id=newly_added_student_id, Personal_Phone_no_1=personal_phone_no_1, Personal_Phone_no_2=personal_phone_no_2, created_by=request.user)

			messages.success(request, ('Skill Student has successfully been added!'))
			return redirect('update_skill_detail_view', newly_added_student_id)

		else:
			messages.error(request, 'Error saving Skill Student. Please Try again.')		
			return redirect('homeview')
	
	skill_student_form = AddSkillStudentForm() # testing new form
	print(skill_student_form)
	return render(request=request, template_name="add_skillstudent_new.html", context={'skill_student_form':skill_student_form})

@login_required(login_url='loginpageview')
def prequalificationview(request):
	"""
		Pre-Qualification
	"""
	pass


@login_required(login_url='loginpageview')
def shortcoursenameview(request):
	"""
		On Get request, this view displays shortcoursename_form to be filled. 
		On Post request, it adds a short course name. 
		This created name is associated with shortcoursetaken objects.
	"""

	# get id of Student to display in template
	skillstudentobjects=SkillStudent.objects.order_by('id').last()

	if request.method == "POST":
		shortcoursename_form = ShortCourseNameForm(request.POST, request.FILES)
		if shortcoursename_form.is_valid():
			shortcoursename_form.save()
			messages.success(request, ('ShortCourseName was successfully added!'))
			return redirect('shortcourse_name_dashboard')
		else:
			messages.error(request, 'Error saving ShortCourseName')
	shortcoursename_form = ShortCourseNameForm()
	return render(request=request, template_name="shortcoursename.html", context={'shortcoursename_form':shortcoursename_form,'skillstudentobjects':skillstudentobjects})


@login_required(login_url='loginpageview')
def shortcoursetakenview(request, student_id):
	"""
		This view adds short course taken by a skill student.
		params:
			student_id: The id of a student for whom the short course info is being added.
	"""

	if request.method == "POST":
		shortcoursetaken_form = ShortCoursesTakenForm(request.POST)
		if shortcoursetaken_form.is_valid():
			shortcoursetaken_form.save()
			messages.success(request, ('ShortCourseTaken was successfully added!'))
			return redirect('update_skill_detail_view',student_id)
	shortcoursetaken_form = ShortCoursesTakenForm()
	return render(request=request, template_name="add_shortcoursetaken.html", context={'shortcoursetaken_form':shortcoursetaken_form,'student_id':student_id})


@login_required(login_url='loginpageview')
def jobpositionview(request):
	"""
		On Get request, this view displays shortcoursename_form to be filled. 
		On Post request, it adds a short course name. 
		This created name is associated with shortcoursetaken objects.
	"""

	# # getting the id of Student to display in template
	# skillstudentobjects=SkillStudent.objects.order_by('id').last()
	jobposition_form = JobPositionForm()

	if request.method == "POST":
		jobposition_form = JobPositionForm(request.POST)
		if jobposition_form.is_valid():
			jobposition_form.save()
			messages.success(request, ('Job Position was successfully added!'))
			return redirect('job_position_dashboard')
		else:
			messages.error(request, 'Error saving JobPosition')
	
	# return render(request=request, template_name="jobposition.html", context={'jobposition_form':jobposition_form,'skillstudentobjects':skillstudentobjects})
	return render(request=request, template_name="jobposition.html", context={'jobposition_form':jobposition_form})


@login_required(login_url='loginpageview')
def jobview(request,student_id):
	"""
		On Get request, this view displays job_form to be filled for a particular student
		whose id is passed in the parameters under student_id argument.
		On Post request, it adds job information against the passed student_id.
		params:
			student_id : The id of a student for whom the job info is being added.
	"""
	if request.method == "POST":
		job_form = JobForm(request.POST)
		if job_form.is_valid():
			job_form.save()
			messages.success(request, ('Job was successfully added!'))
			return redirect('update_skill_detail_view',student_id)
		else:
			messages.error(request, 'Error saving Job')
	job_form = JobForm()
	return render(request=request, template_name="job.html", context={'job_form':job_form,'student_id':student_id})


# query view named as contacted in models and as ContactedForm in forms.py 
@login_required(login_url='loginpageview')
def add_query(request,student_id):
	"""
		Adds a Query and its Reply against a skill student.
		On Get request, it displays a contacted_form for the passed student (student_id).
		On Post request, it adds a Contacted object in the table against student_id.
		add_query view is related to contacted in models and as ContactedForm in forms.py
		params:
			student_id : The id of a student for whom the query info is being added.
	"""

	contacted_form = ContactedForm()

	if request.method == "POST":
		contacted_form = ContactedForm(request.POST)
		if contacted_form.is_valid():
			contacted_form.save()
			messages.success(request, ('Query was successfully added!'))
			return redirect('update_skill_detail_view', student_id)
		else:
			messages.error(request, 'Error saving')

	return render(request=request, template_name="add_query.html", context={'contacted_form':contacted_form,'student_id':student_id})


@login_required(login_url='loginpageview')
def user_profile(request):
	"""
		Returns the profile of currently logged-in user.
	"""

	user = request.user
	profile_object_queryset = UserProfile.objects.filter(user_id=user.id)
	profile_object = profile_object_queryset.first() # reading the only-one found profile-object associated with the given user id
	profile_image = profile_object.image # as there is only one field in the profile object i.e. image
	
	return render(request,"user_profile.html",context={'current_user':user, 'profile_image':profile_image})



@login_required(login_url='loginpageview')
def skill_student_detail_view(request,student_id):
	"""
		This view displays a detailed view of a passed skill student (student_id).
		Information of passed student is extracted from tables hereunder against 
		its students_id and displayed.
			- SkillStudent
			- CurrentStudy
			- ShortCoursesTaken
			- PhoneNo
			- Job

		params:
			student_id : The id of a student for whom the detailed info is being displayed.
	"""

	skill_std__query_set=SkillStudent.objects.filter(id=student_id)
	phone_no_query_set=PhoneNo.objects.filter(student_id=student_id)
	current_study_query_set=CurrentStudy.objects.filter(student_id=student_id)
	job_form_query_set=Job.objects.filter(student_id=student_id)
	short_course_taken_query_set=ShortCoursesTaken.objects.filter(student_id=student_id)

	# only one object exists in these quesry sets. Thus, getting it.
	skill_std = skill_std__query_set.first() 
	phone_no = phone_no_query_set.first()
	current_study = current_study_query_set.first()

	# getting student ids from contacted table where they are mentioned under student_id field.
	# As student_id is a foreign-key from here which is primary-key in skill student table
	contacted_query_set=Contacted.objects.filter(student_id=student_id)

	# .first() used because queryset contain only 1 obj so that's why .first() used
	context={
		'skill_std_form':skill_std, 
		'phone_no_form':phone_no,
		'current_study_form':current_study,
		'short_course_taken_form':short_course_taken_query_set,
		'job_form':job_form_query_set,
		'query_form':contacted_query_set
	}

	return render(request,"skill_student_detail_view.html",context=context)


# ---------------------------------------------------------------------------------------- 
# 							SEARCH Dashboard
# ----------------------------------------------------------------------------------------


@login_required(login_url='loginpageview')
def search_skill_dashboard(request):
	"""
		This view handles the search skill dashboard creation and display.
		On Get request, it returns a context comprising of information 
		of all the students in the database.
		On Post request, it returns a context comprising of information of
		students that are selected on the basis of criteria sent in the Post request.
	"""

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
			std_data.append(std.program_of_interest)
			std_data.append(std.shift)
			std_data.append(std.admission_status)
			std_data.append(std.date_applied)
			
			# getting personal phone details of the respective student
			std_id = std.id
			query = f"SELECT * FROM AdmissionSystem_phoneno WHERE student_id={std_id}"
		    # print(query)
			# print(std_id)
			
			personal_phone_number_1_of_student = ''

			for phone_obj in PhoneNo.objects.raw(query):
				if phone_obj.Personal_Phone_no_1 is None:
					continue
				else:
					personal_phone_number_1_of_student = personal_phone_number_1_of_student + phone_obj.Personal_Phone_no_1

			std_data.append(personal_phone_number_1_of_student)
			all_std_data.append(std_data)

		return all_std_data


	if request.method == "POST":
		contacted_form = StudentCustomSearchForm(request.POST)
		if contacted_form.is_valid():
			shift = contacted_form.cleaned_data['shift']
			program_of_interest = contacted_form.cleaned_data['program_of_interest']
			admission_status = contacted_form.cleaned_data['admission_status']
			created_by = contacted_form.cleaned_data['created_by']

			data_list = [shift, program_of_interest, admission_status, created_by]
			dict_of_data={}
			
			# populating dict_of_data
			for item in enumerate(data_list):
				if item[1]=="": # if empty then leave this item and move on
					continue 
				else:
					if item[0]==0:
						dict_of_data['shift'] = item[1]
					elif item[0]==1:
						dict_of_data['program_of_interest'] = item[1]
					elif item[0]==2:
						dict_of_data['admission_status'] = item[1]
					elif item[0]==3:
						dict_of_data['created_by'] = item[1]

			# make a dictionary of keywords same as in the model
			# only those keys will be populated whose values are not string
			# then pass this dictionary into the filter like this: filter(**dict_name) as 
			# filter takes **kwargs as argument

			skillstudentobjects=SkillStudent.objects.filter(**dict_of_data)
			# generating context object
			std_data = generate_context(skillstudentobjects=skillstudentobjects)
	else:
		skillstudentobjects=SkillStudent.objects.all()
		std_data = generate_context(skillstudentobjects=skillstudentobjects)

	student_custom_search_form=StudentCustomSearchForm()
	context = {
		'students': std_data,
		'student_custom_search_form':student_custom_search_form
	}
	
	return render(request,'search_skill_dashboard.html',context)


# ----------------------------------------------------------------------------------------
# 							UPDATE VIEWS
# ----------------------------------------------------------------------------------------


def update_current_study(request, student_id):
	"""
		This view updates current study information of a skill student passed as argument (student_id).
		On Get request, it fetches and displays the CurrentStudy data of the student.
		On Post request, it updates the information and redirects to update_skill_detail_view
		params:
			student_id : The id of a student for whom current study info is being updated.
	"""

	student_currentstudy_object=CurrentStudy.objects.get(student_id=student_id) # get returns the only matching object
	form=CurrentStudyForm(instance=student_currentstudy_object)

	if request.method=='POST':
		form=CurrentStudyForm(request.POST, instance=student_currentstudy_object)
		if form.is_valid():
			form.save()
			return redirect('update_skill_detail_view', student_id)
	
	return render(request,'currentstudyupdate.html',{'form':form})


@login_required(login_url='loginpageview')
def update_skill_student(request,student_id):
	"""
		Updates the basic information of skill student as created in addskillstudentview.
		
		params:

	"""
	student_object=SkillStudent.objects.get(id=student_id)
	form=SkillStudentForm(instance=student_object)
	
	if request.method=='POST':
		form=SkillStudentForm(request.POST, request.FILES, instance=student_object)
		if form.is_valid():
			form.save()
			return redirect('update_skill_detail_view',student_object)
	return render(request,'skillstudentupdate.html',{'form':form})


@login_required(login_url='loginpageview')
def update_shortcourse_taken(request,id):
	"""

	"""

	shortcourse_object=ShortCoursesTaken.objects.get(id=id)
	form=ShortCoursesTakenForm(instance=shortcourse_object)
	# getting student id. As shortcourse_object returns student_id on print 
	# because of its dunder str function returns the student id
	# student_id is to be passed on in the context to make it available in the
	# shortcoursetakenupdate.html template where this would be used inside
	# delete button to be passed as argument to run delete view
	student_id = shortcourse_object.student_id

	if request.method=='POST':
		form=ShortCoursesTakenForm(request.POST,instance=shortcourse_object)
		if form.is_valid():
			form.save()
			return redirect('update_skill_detail_view',shortcourse_object)
	return render(request,'shortcoursetakenupdate.html',{'form':form,'id':id, 'student_id':student_id})


# view to update added job for skill students
@login_required(login_url='loginpageview')
def update_job(request,id):
	"""
		This 
	"""
	student_job_object=Job.objects.get(id=id)
	# getting student_id to be passed on to the template. As delete would require to
	# redirect to update student profile after deletion of a job object
	student_id = student_job_object.student_id 
	# print(student_id)
	form=JobForm(instance=student_job_object)
	
	if request.method=='POST':
		form=JobForm(request.POST,instance=student_job_object)
		if form.is_valid():
			form.save()
			return redirect('update_skill_detail_view',student_job_object)

	# passing id of the job and student_id to which this pbject belongs in 
	# context as delete view requires both and to invoke the delete job view,
	# the delete button requires these two.
	return render(request,'jobupdate.html',{'form':form, 'job_id': id, 'student_id':student_id})


# view to update added phone no for skill students
@login_required(login_url='loginpageview')
def update_phone_no(request,id):
	student_phone_object=PhoneNo.objects.get(student_id=id)
	if request.method=='POST':
		form=PhoneNoForm(request.POST,instance=student_phone_object)
		if form.is_valid():
			form.save()
			return redirect('update_skill_detail_view',student_phone_object)
	else:
		form=PhoneNoForm(instance=student_phone_object)
	return render(request,'phonenoupdate.html',{'form':form})



# view to update added query for skill students
@login_required(login_url='loginpageview')
def update_query(request,id):
	contacted_object=Contacted.objects.get(id=id)
	form=ContactedForm(instance=contacted_object)
	if request.method=='POST':
		form=ContactedForm(request.POST,instance=contacted_object)
		if form.is_valid():
			form.save()
			return redirect('update_skill_detail_view',contacted_object)
	else:
		form=ContactedForm(instance=contacted_object)
	return render(request,'update_query.html',{'form':form,'contacted_object':contacted_object})

# job position update View to update job position
@login_required(login_url='loginpageview')
def update_job_position(request,id):
	job_position_object=JobPosition.objects.get(id=id)
	form=JobPositionForm(instance=job_position_object)
	if request.method=='POST':
		form=JobPositionForm(request.POST,instance=job_position_object)
		if form.is_valid():
			form.save()
			return redirect('job_position_dashboard')
	else:
		form=JobPositionForm(instance=job_position_object)
	return render(request,'jobpositionupdate.html',{'form':form})


# short course name update view to update added shortcourse names
@login_required(login_url='loginpageview')
def update_shortcourse_name(request,id):
	shortcourse_object=ShortCourseName.objects.get(id=id)
	form=ShortCourseNameForm(instance=shortcourse_object)
	if request.method=='POST':
		form=ShortCourseNameForm(request.POST,instance=shortcourse_object)
		if form.is_valid():
			form.save()
			return redirect('shortcourse_name_dashboard')
	return render(request,'shortcoursenameupdate.html',{'form':form})
  
# ----------------------------------------------------------------------------------------
# 							DELETE VIEWS
# ----------------------------------------------------------------------------------------

# view to delete added skill students
@login_required(login_url='loginpageview')
def delete_skill_student(request,id):
	"""
		This view deletes a skill student.
		params:
			id:	 id of Skill Student object which is to be deleted
	"""
	# skillstudent object to be deleted
	skillstudentobject=SkillStudent.objects.get(id=id)

	skillstudentobject.delete()
	return redirect('modify_skill_dashboard')


@login_required(login_url='loginpageview')
def delete_shortcoursetaken(request, id, student_id):
	"""
		This view deletes a short course taken by studen.
		params:
			id:				id of shortcoursetaken object which is to be deleted
			student:id:		id of student against whom this short course object has been created
	"""
	shortcourse_object=ShortCoursesTaken.objects.get(id=id)
	# deleting the object
	shortcourse_object.delete()
	# redirecting back to the update view of the student
	return redirect('update_skill_detail_view', student_id) 


@login_required(login_url='loginpageview')
def delete_job(request, job_id, student_id):
	"""
		This view deletes a job added for student.
		params:
			job_id:				id of job object which is to be deleted
			student:id:		id of student against whom this job object has been created
	"""
	job_object=Job.objects.get(id=job_id)
	# deleting the object
	job_object.delete()
	# redirecting back to the update view of the student
	return redirect('update_skill_detail_view', student_id) 

# @login_required(login_url='loginpageview')
# def delete_query(request, query_id, student_id):
# 	"""
# 		This view deletes a query added for student.
# 		params:
# 			 query_id:				id of query object which is to be deleted
# 			student:id:		id of student against whom this job object has been created
# 	"""
# 	query_object=Contacted.objects.get(id=query_id)
# 	# deleting the object
# 	query_object.delete()
# 	# redirecting back to the update view of the student
# 	return redirect('update_skill_detail_view', student_id) 





# ----------------------------------------------------------------------------------------
# 							DASHBOARD VIEWS
# ----------------------------------------------------------------------------------------


# view to get all skillstudents on dashboard for update 
@login_required(login_url='loginpageview')
def modify_skill_dashboard(request):

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
			std_data.append(std.program_of_interest)
			std_data.append(std.shift)
			std_data.append(std.admission_status)
			std_data.append(std.date_applied)
			
			# getting personal phone details of the respective student
			std_id = std.id
			query = f"SELECT * FROM AdmissionSystem_phoneno WHERE student_id={std_id}"
		    # print(query)
			# print(std_id)
			
			personal_phone_number_1_of_student = ''

			for phone_obj in PhoneNo.objects.raw(query):
				if phone_obj.Personal_Phone_no_1 is None:
					continue
				else:
					personal_phone_number_1_of_student = personal_phone_number_1_of_student + phone_obj.Personal_Phone_no_1

			std_data.append(personal_phone_number_1_of_student)
			all_std_data.append(std_data)

		return all_std_data


	if request.method == "POST":
		contacted_form = StudentCustomSearchForm(request.POST)
		if contacted_form.is_valid():
			shift = contacted_form.cleaned_data['shift']
			program_of_interest = contacted_form.cleaned_data['program_of_interest']
			admission_status = contacted_form.cleaned_data['admission_status']
			created_by = contacted_form.cleaned_data['created_by']

			data_list = [shift, program_of_interest, admission_status, created_by]
			dict_of_data={}
			
			for item in enumerate(data_list):
				if item[1]=="":
					continue 
				else:
					if item[0]==0:
						dict_of_data['shift'] = item[1]
					elif item[0]==1:
						dict_of_data['program_of_interest'] = item[1]
					elif item[0]==2:
						dict_of_data['admission_status'] = item[1]
					elif item[0]==3:
						dict_of_data['created_by'] = item[1]

			# make a dictionary of keywords same as in the model
			# only those keys will be populated whose values are not string
			# then pass this dictionary into the filter like this: filter(**dict_name) as 
			# filter takes **kwargs as argument

			skillstudentobjects=SkillStudent.objects.filter(**dict_of_data)
			# generating context object
			std_data = generate_context(skillstudentobjects=skillstudentobjects)
	else:
		skillstudentobjects=SkillStudent.objects.all()
		std_data = generate_context(skillstudentobjects=skillstudentobjects)

	student_custom_search_form=StudentCustomSearchForm()
	context = {
		'students': std_data,
		'student_custom_search_form':student_custom_search_form
	}
	
	return render(request,'modify_skill_dashboard.html',context)



# job position dashboard to view job position
@login_required(login_url='loginpageview')
def job_position_dashboard(request):
	jobpositionobjects=JobPosition.objects.all()
	all_data = list()
	for std in jobpositionobjects:
		std_data = list()	
		std_data.append(std.id)
		std_data.append(std.job_title)
		all_data.append(std_data)

	context = {'alldata': all_data}
	return render(request,'job_name_dashboard.html',context)


# short course name dashboard to view added shortcourse names
@login_required(login_url='loginpageview')
def shortcourse_name_dashboard(request):
	shortcoursenameobjects=ShortCourseName.objects.all()
	all_data = list()
	for std in shortcoursenameobjects:
		std_data = list()	
		std_data.append(std.id)
		std_data.append(std.course_title)
		all_data.append(std_data)

	context = {'alldata': all_data}
	return render(request,'shortcourse_name_dashboard.html',context)

# view to get all skillstudent details in one page to update them
@login_required(login_url='loginpageview')
def update_skill_detail_view(request, student_id):
	"""
		This view displays a detailed view of a passed skill student (student_id).
		Information of passed student is extracted from tables hereunder against 
		its students_id and displayed.
			- SkillStudent
			- CurrentStudy
			- ShortCoursesTaken
			- PhoneNo
			- Job

		params:
			student_id : The id of a student for whom the detailed info is being displayed.
	"""

	skill_std__query_set=SkillStudent.objects.filter(id=student_id)
	phone_no_query_set=PhoneNo.objects.filter(student_id=student_id)
	current_study_query_set=CurrentStudy.objects.filter(student_id=student_id)
	job_form_query_set=Job.objects.filter(student_id=student_id)
	short_course_taken_query_set=ShortCoursesTaken.objects.filter(student_id=student_id)

	# only one object exists in these quesry sets. Thus, getting it.
	skill_std = skill_std__query_set.first() 
	phone_no = phone_no_query_set.first()
	current_study = current_study_query_set.first()

	# getting student ids from contacted table where they are mentioned under student_id field.
	# As student_id is a foreign-key from here which is primary-key in skill student table
	contacted_query_set=Contacted.objects.filter(student_id=student_id)

	# .first() used because queryset contain only 1 obj so that's why .first() used
	context={
		'skill_std_form':skill_std, 
		'phone_no_form':phone_no,
		'current_study_form':current_study,
		'short_course_taken_form':short_course_taken_query_set,
		'job_form':job_form_query_set,
		'query_form':contacted_query_set
	}

	return render(request,"update_skill_detail_view.html",context=context)