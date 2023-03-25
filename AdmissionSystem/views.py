from .models import *
from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from .view_helper_functions import generate_context
from django.core.exceptions import *
 
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
			login (request, user)
			# putting the currently logged-in user into the session
			request.session['current-user-username'] = user.username
			return redirect('homeview')
		else:
			messages.info(request,'Username or Password incorrect')

	return render(request,'login.html')


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
		
		add_skill_student_form = AddSkillStudentForm(request.POST)
		if add_skill_student_form.is_valid():
			# getting the filled data 
			name = add_skill_student_form.cleaned_data['name']
			personal_no_1 = add_skill_student_form.cleaned_data['personal_no_1']
			personal_no_2 = add_skill_student_form.cleaned_data['personal_no_2']
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

			data_list = [name, personal_no_1, personal_no_2, area, laptop, availability_from, availabitity_to, date_applied, pre_qualification, currently_studying, admission_status]
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
			PhoneNo.objects.create(student_id=newly_added_student_id, personal_phone_no_1=personal_no_1, personal_phone_no_2=personal_no_2, created_by=request.user)

			# StudentAvailability Model object creation
			StudentAvailability.objects.create(student_id=newly_added_student_id, available_from=availability_from, available_to=availabitity_to, created_by=request.user)

			# CourseApplication Model object creation
			CourseApplication.objects.create(student_id=newly_added_student_id, date_applied=date_applied, admission_status=admission_status)

			messages.success(request, 'Skill Student has successfully been added!')
			return redirect('update_skill_detail_view', newly_added_student_id)

		else:
			messages.error(request, 'Error saving Skill Student. Please Try again.')		
			return redirect('homeview')
	
	skill_student_form = AddSkillStudentForm()
	return render(request=request, template_name="add_skillstudent_new.html", context={'skill_student_form':skill_student_form})



@login_required(login_url='loginpageview')
def shortcoursenameview(request):
	"""
		On Get request, this view displays shortcoursename_form to be filled. 
		On Post request, it adds a short course name. 
		This created name is associated with shortcoursetaken objects.
	"""
	if request.method == "POST":
		shortcoursename_form = ShortCourseNameForm(request.POST)
		if shortcoursename_form.is_valid():
			shortcoursename_form.save()
			messages.success(request, ('Short Course Name has successfully been added!'))
			return redirect('shortcourse_name_dashboard')
		else:
			messages.error(request, 'Error saving Short Course Name')
	
	shortcoursename_form = ShortCourseNameForm()
	return render(request=request, template_name="shortcoursename.html", context={'shortcoursename_form':shortcoursename_form})


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
		
	"""	
	if request.method == "POST":
		jobposition_form = JobPositionForm(request.POST)
		if jobposition_form.is_valid():
			jobposition_form.save()
			messages.success(request, ('Job position has successfully been added!'))
			return redirect('job_position_dashboard')
		else:
			messages.error(request, 'Error saving job position')

	jobposition_form = JobPositionForm()
	return render(request=request, template_name="jobposition.html", context={'jobposition_form':jobposition_form})


@login_required(login_url='loginpageview')
def jobview(request, student_id):
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
def add_query(request, student_id):
	"""
		Adds a Query and its Reply against a skill student.
		On Get request, it displays a contacted_form for the passed student (student_id).
		On Post request, it adds a Contacted object in the table against student_id.
		add_query view is related to contacted in models and as ContactedForm in forms.py
		params:
			student_id : The id of a student for whom the query info is being added.
	"""
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

	if UserProfile.objects.filter(user_id=user.id).first()!=None:
		profile_object = UserProfile.objects.filter(user_id=user.id).first() # reading the only-one found profile-object associated with the given user id
		profile_image = profile_object.image # as there is only one field in the profile object i.e. image

	else:
		# if there is no profile object created for this user, then create it
		UserProfile.objects.create(user=request.user)
		profile_object = UserProfile.objects.filter(user_id=user.id).first()
		profile_image = profile_object.image

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
	availability_query_set=StudentAvailability.objects.filter(student_id=student_id)

	# only one object exists in these quesry sets. Thus, getting it.
	skill_std = skill_std__query_set.first() 
	phone_no = phone_no_query_set.first()
	current_study = current_study_query_set.first()

	# getting student ids from contacted table where they are mentioned under student_id field.
	# As student_id is a foreign-key from here which is primary-key in skill student table
	contacted_query_set=Contacted.objects.filter(student_id=student_id)
	
	context={
		'skill_std_form':skill_std, 
		'phone_no_form':phone_no,
		'current_study_form':current_study,
		'short_course_taken_form':short_course_taken_query_set,
		'job_form':job_form_query_set,
		'query_form':contacted_query_set,
		'availability_form':availability_query_set
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
	if request.method == "POST":
		custom_search_done = StudentCustomSearchForm(request.POST)
		if custom_search_done.is_valid():
			shift = custom_search_done.cleaned_data['shift']
			program_of_interest = custom_search_done.cleaned_data['program_of_interest']
			admission_status = custom_search_done.cleaned_data['admission_status']
			created_by = custom_search_done.cleaned_data['created_by']

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

@login_required(login_url='loginpageview')
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
			return redirect('update_skill_detail_view',student_id)
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
	if request.method=='POST':
		form=JobPositionForm(request.POST,instance=job_position_object)
		if form.is_valid():
			form.save()
			return redirect('job_position_dashboard')
	else:
		form=JobPositionForm(instance=job_position_object)
	return render(request,'jobpositionupdate.html',{'form':form, 'job_position_id':id})


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
	return render(request,'shortcoursenameupdate.html', {'form':form})
  
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


@login_required(login_url='loginpageview')
def delete_job_position(request, job_position_id):
	"""
		This view deletes a job name / position.
		params:
			job_id:				id of job object which is to be deleted
	"""
	job_position_object=JobPosition.objects.get(id=job_position_id)
	# deleting the object
	job_position_object.delete()
	# redirecting back to the update view of the student
	return redirect('job_position_dashboard')






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
	availability_query_set=StudentAvailability.objects.filter(student_id=student_id)

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
		'query_form':contacted_query_set,
		'availability_form':availability_query_set
	}

	return render(request,"update_skill_detail_view.html",context=context)



# ---------------------------------------------------------------
# 			New Views
# ---------------------------------------------------------------

# Document Type -------------------

@login_required(login_url='loginpageview')
def document_type_view(request):
	"""
		On Get request, this view displays DocumentTypeForm to be filled.
		On Post request, it adds document type information.
	"""
	if request.method == "POST":
		document_type_form = DocumentTypeForm(request.POST)
		if document_type_form.is_valid():
			document_type_form.save()
			messages.success(request, ('Document type was successfully added!'))
			return redirect('documenttypedashboard')
		else:
			messages.error(request, 'Error saving Document Type')

	document_type_form = DocumentTypeForm()
	return render(request=request, template_name="add_document_type.html", context={'document_type_form':document_type_form})



# job position dashboard to view job position
@login_required(login_url='loginpageview')
def document_type_dashboard(request):
	document_type_objects = DocumentType.objects.all()
	all_data = list()
	for document_type in document_type_objects:
		doc_type_data = list()	
		doc_type_data.append(document_type.id)
		doc_type_data.append(document_type.doc_type)
		all_data.append(doc_type_data)

	context = {'alldata': all_data}
	return render(request,'document_type_dashboard.html',context=context)



@login_required(login_url='loginpageview')
def update_document_type(request, document_type_id):
	"""
		This view updates information of a 'document type' student passed as argument (document_type_id).
		On Get request, it fetches and displays the document-type data.
		On Post request, it updates the information and redirects to home.
		params:
			document_type_id : The id of a document-type.
	"""

	document_type_object = DocumentType.objects.get(id=document_type_id) # get returns the only matching object
	form = DocumentTypeForm(instance=document_type_object)

	if request.method=='POST':
		form=DocumentTypeForm(request.POST, instance=document_type_object)
		if form.is_valid():
			form.save()
			return redirect('documenttypedashboard')
	
	return render(request,'update_document_type.html',context= {'document_type_form':form, 'document_type_id': document_type_id})



@login_required(login_url='loginpageview')
def delete_document_type(request, document_type_id):
	"""
		This view deletes a document type.
		params:
			document_type_id:	id of document type object which is to be deleted
	"""

	document_type_object=DocumentType.objects.get(id=document_type_id)

	# deleting the object
	try:
		document_type_object.delete()
		# redirecting back to the update view of the student
		return redirect('documenttypedashboard')
	except Exception:
		messages.info(request, 'Error. Object could not be deleted. Try again.')
		return redirect('documenttypedashboard')

# Document -------------------

# Prequalification -------------------


@login_required(login_url='loginpageview')
def pre_qualification_view(request):
	"""
		On Get request, this view displays PrequalificaitonForm to be filled.
		On Post request, it adds Pre-qualificaiton information to db.
	"""
	if request.method == "POST":
		pre_qualification_form = PrequalificaitonForm(request.POST)
		if pre_qualification_form.is_valid():
			pre_qualification_form.save()
			messages.success(request, 'Pre-qualification was successfully added!')
			return redirect('prequalificationdashboard')
		else:
			messages.error(request, 'Error saving Pre-Qualification')
			return redirect('prequalificationview')

	pre_qualification_form = PrequalificaitonForm()
	return render(request=request, template_name="add_pre_qualification.html", context={'pre_qualification_form':pre_qualification_form})



# job position dashboard to view job position
@login_required(login_url='loginpageview')
def pre_qualification_dashboard(request):
	pre_qualification_objects = PreQualification.objects.all()
	all_data = list()
	for prequal_object in pre_qualification_objects:
		prequal_data = list()	
		prequal_data.append(prequal_object.id)
		prequal_data.append(prequal_object.pre_qualification_name)
		all_data.append(prequal_data)

	context = {'alldata': all_data}
	return render(request,'pre_qualification_dashboard.html',context=context)


@login_required(login_url='loginpageview')
def update_pre_qualification(request, pre_qualification_id):
	"""
		This view updates information of a 'pre-qualification'.
		On Get request, it fetches and displays the pre-qualification data.
		On Post request, it updates the information and redirects to pre-qualification dashboard.
		params:
			pre_qualification_id : The id of a pre-qualification.
	"""

	pre_qualification_object = PreQualification.objects.get(id=pre_qualification_id) # get returns the only matching object
	form = PrequalificaitonForm(instance=pre_qualification_object)

	if request.method=='POST':
		form=PrequalificaitonForm(request.POST, instance=pre_qualification_object)
		if form.is_valid():
			form.save()
			return redirect('prequalificationdashboard')
	
	return render(request,'update_pre_qualification.html',context= {'pre_qualification_form':form, 'pre_qualification_id': pre_qualification_id})


@login_required(login_url='loginpageview')
def delete_pre_qualification(request, pre_qualification_id):
	"""
		This view deletes a pre-qualification object.
		params:
			pre_qualification_id:	id of pre-qualification object which is to be deleted
	"""

	pre_qualification_object=PreQualification.objects.get(id=pre_qualification_id)

	# deleting the object
	try:
		pre_qualification_object.delete()
		# redirecting back to the update view of the student
		return redirect('prequalificationdashboard')
	except Exception:
		messages.info(request, 'Error. Object could not be deleted. Try again.')
		return redirect('prequalificationdashboard')


# Student Availability -------------------

@login_required(login_url='loginpageview')
def student_availability_view(request, student_id):
	"""
		On Get request, this view displays StudentAvailabilityForm to be filled.
		On Post request, it adds Student-Availability information to db.
	"""
	if request.method == "POST":
		student_availability_form = StudentAvailabilityForm(request.POST)
		print(student_availability_form.errors) # checking for errors in the form
		if student_availability_form.is_valid():
			student_availability_form.save()
			messages.success(request, 'Student-Availability was successfully added!')
			return redirect('update_skill_detail_view',student_id)
		else:
			messages.error(request, 'Error saving Student-Availability information.')
			return redirect('update_skill_detail_view',student_id)

	student_availability_form = StudentAvailabilityForm()
	return render(request=request, template_name="add_student_availability.html", context={'student_availability_form':student_availability_form, 'student_id':student_id})



@login_required(login_url='loginpageview')
def update_student_availability(request, availability_id):
	"""
		This view updates information of a student's availability object.
		On Get request, it fetches and displays the availability object data.
		On Post request, it updates the information and redirects to the update_skill_detail_view_dashboard.
		params:
			availability_id : The id of the availability object that needs to be updated.
	"""
	availability_object = StudentAvailability.objects.get(id=availability_id) # get returns the only matching object
	form = StudentAvailabilityForm(instance=availability_object)
	
	student_id = availability_object.student_id # getting the student id for redirect
	print("-------- ", student_id, "-------------")

	if request.method=='POST':
		form=StudentAvailabilityForm(request.POST, instance=availability_object)
		if form.is_valid():
			form.save()
			return redirect('update_skill_detail_view', student_id)
	

	return render(request,'update_student_availability.html',context= {'student_availability_form':form, 'availability_id': availability_id})



# Course Conducting Body -------------------

@login_required(login_url='loginpageview')
def course_conducting_body_view(request):
	"""
		On Get request, this view displays CourseConductingBodyForm to be filled.
		On Post request, it adds Course-Conducting-Body's information to db.
	"""

	if request.method == "POST":
		course_conducting_body_form = CourseConductingBodyForm(request.POST)
		if course_conducting_body_form.is_valid():
			course_conducting_body_form.save()
			messages.success(request, 'Course Conducting Body was successfully added!')
			return redirect('courseconductingbodydashboard')
		else:
			messages.error(request, 'Error saving Course Conducting Body information.')
			return redirect('courseconductingbodydashboard')

	course_conducting_body_form = CourseConductingBodyForm()
	return render(request=request, template_name="add_course_conducting_body.html", context={'course_conducting_body_form':course_conducting_body_form})



@login_required(login_url='loginpageview')
def course_conducting_body_dashboard(request):
	course_conducting_body_objects = CourseConductingBody.objects.all()
	all_data = list()
	for coursecondbody_object in course_conducting_body_objects:
		coursecondbody_data = list()	
		coursecondbody_data.append(coursecondbody_object.id)
		coursecondbody_data.append(coursecondbody_object.course_conducting_body_name)
		all_data.append(coursecondbody_data)

	context = {'alldata': all_data}
	return render(request,'course_conducting_body_dashboard.html',context=context)



@login_required(login_url='loginpageview')
def update_course_conducting_body(request, course_conducting_body_id):
	"""
		This view updates information of a 'course_conducting_body'.
		On Get request, it fetches and displays the course-conducting-body data.
		On Post request, it updates the information and redirects to pre-qualification dashboard.
		params:
			course_conducting_body_id : The id of a course-conducting-body.
	"""

	course_conducting_body_object = CourseConductingBody.objects.get(id=course_conducting_body_id) # get returns the only matching object
	form = CourseConductingBodyForm(instance=course_conducting_body_object)

	if request.method=='POST':
		form=CourseConductingBodyForm(request.POST, instance=course_conducting_body_object)
		if form.is_valid():
			form.save()
			messages.success(request, 'Successfully updated Course Conducting Body information.')
			return redirect('courseconductingbodydashboard')
		else:
			messages.error(request, 'Error updating Course Conducting Body information.')
			return redirect('courseconductingbodydashboard')
	
	return render(request,'update_course_conducting_body.html',context= {'course_conducting_body_form':form, 'course_conducting_body_id': course_conducting_body_id})



@login_required(login_url='loginpageview')
def delete_course_conducting_body(request, course_conducting_body_id):
	"""
		This view deletes a course_conducting_body object.
		params:
			course_conducting_body_id:	id of course_conducting_body object which is to be deleted
	"""

	course_conducting_body_object=CourseConductingBody.objects.get(id=course_conducting_body_id)

	# deleting the object
	try:
		course_conducting_body_object.delete()
		# redirecting back to the update view of the student
		return redirect('courseconductingbodydashboard')
	except Exception:
		messages.error(request, 'Error. Object could not be deleted. Try again.')
		return redirect('courseconductingbodydashboard')



# Course Name -------------------


@login_required(login_url='loginpageview')
def course_name_view(request):
	"""
		On Get request, this view displays CourseNameForm to be filled.
		On Post request, it adds Course-Name's information to db.
	"""

	if request.method == "POST":
		course_name_form = CourseNameForm(request.POST)
		if course_name_form.is_valid():
			course_name_form.save()
			messages.success(request, 'Course Name was successfully added!')
			return redirect('coursenamedashboard')
		else:
			messages.error(request, 'Error saving Course Conducting Body information.')
			return redirect('coursenamedashboard')

	course_name_form = CourseNameForm()
	return render(request=request, template_name="add_course_name.html", context={'course_name_form':course_name_form})



@login_required(login_url='loginpageview')
def course_name_dashboard(request):
	course_name_objects = CourseName.objects.all()
	all_data = list()
	for course_object in course_name_objects:
		course_data = list()	
		course_data.append(course_object.id)
		course_data.append(course_object.course_name)
		all_data.append(course_data)

	context = {'alldata': all_data}
	return render(request,'course_name_dashboard.html',context=context)



@login_required(login_url='loginpageview')
def update_course_name(request, course_name_id):
	"""
		This view updates information of a 'Course-Name'.
		On Get request, it fetches and displays the course-name data.
		On Post request, it updates the information and redirects to course-name dashboard.
		params:
			course_name_id : The id of a course-name.
	"""

	course_name_object = CourseName.objects.get(id=course_name_id) # get returns the only matching object
	form = CourseNameForm(instance=course_name_object)

	if request.method=='POST':
		form=CourseNameForm(request.POST, instance=course_name_object)
		if form.is_valid():
			form.save()
			messages.success(request, 'Successfully updated Course Name information.')
			return redirect('coursenamedashboard')
		else:
			messages.error(request, 'Error updating Course Name information.')
			return redirect('coursenamedashboard')
	
	return render(request,'update_course_name.html',context= {'course_name_form':form, 'course_name_id': course_name_id})



@login_required(login_url='loginpageview')
def delete_course_name(request, course_name_id):
	"""
		This view deletes a course_name object.
		params:
			course_name_id:	id of course_name object which is to be deleted
	"""

	course_name_object=CourseName.objects.get(id=course_name_id)

	# deleting the object
	try:
		course_name_object.delete()
		messages.success(request, 'Successfully deleted.')
		# redirecting back to the update view of the student
		return redirect('coursenamedashboard')
	except Exception:
		messages.error(request, 'Error. Object could not be deleted. Try again.')
		return redirect('coursenamedashboard')



# Course Batch No -------------------

@login_required(login_url='loginpageview')
def course_batch_no_view(request):
	"""
		On Get request, this view displays CourseBatchNoForm to be filled.
		On Post request, it adds Course-Batch-No.'s information to db.
	"""
	if request.method == "POST":
		course_batch_no_form = CourseBatchNoForm(request.POST)
		if course_batch_no_form.is_valid():
			course_batch_no_form.save()
			messages.success(request, 'Course Batch No. was successfully added!')
			return redirect('coursebatchnodashboard')
		else:
			messages.error(request, 'Error saving Course Batch No. information.')
			return redirect('coursebatchnodashboard')

	course_batch_no_form = CourseBatchNoForm()
	return render(request=request, template_name="add_course_batch_num.html", context={'course_batch_no_form':course_batch_no_form})



@login_required(login_url='loginpageview')
def course_batch_no_dashboard(request):
	course_batch_no_objects = CourseBatchNo.objects.all()
	all_data = list()
	for course_batch_object in course_batch_no_objects:
		course_batch_data = list()	
		course_batch_data.append(course_batch_object.id)
		course_batch_data.append(course_batch_object.course_batch_no)
		all_data.append(course_batch_data)

	context = {'alldata': all_data}
	return render(request,'course_batch_num_dashboard.html',context=context)



@login_required(login_url='loginpageview')
def update_course_batch_no(request, course_batch_id):
	"""
		This view updates information of a 'course_batch_number'.
		On Get request, it fetches and displays the course_batch_number data.
		On Post request, it updates the information and redirects to course-batch-number dashboard.
		params:
			course_batch_id : The id of a course-batch-no object.
	"""
	course_batch_object = CourseBatchNo.objects.get(id=course_batch_id) # get returns the only matching object
	form = CourseBatchNoForm(instance=course_batch_object)

	if request.method=='POST':
		form=CourseBatchNoForm(request.POST, instance=course_batch_object)
		if form.is_valid():
			form.save()
			messages.success(request, 'Successfully updated Course Batch No. information.')
			return redirect('coursebatchnodashboard')
		else:
			messages.error(request, 'Error updating Course Batch No. information.')
			return redirect('coursebatchnodashboard')
	
	return render(request,'update_course_batch_num.html',context= {'course_batch_no_form':form, 'course_batch_id': course_batch_id})



@login_required(login_url='loginpageview')
def delete_course_batch_no(request, course_batch_id):
	"""
		This view deletes a course_batch_num object.
		params:
			course_batch_id:	id of course_batch_num object which is to be deleted
	"""
	course_batch_object = CourseBatchNo.objects.get(id=course_batch_id)

	# deleting the object
	try:
		course_batch_object.delete()
		messages.success(request, 'Successfully deleted.')
		# redirecting back to the update view of the student
		return redirect('coursebatchnodashboard')
	except Exception:
		messages.error(request, 'Error. Object could not be deleted. Try again.')
		return redirect('coursebatchnodashboard')



# Course Applicaiton -------------------


# Roll No -------------------

# Already Registered With Course Conducting Body -------------------

# Shift Name -------------------

@login_required(login_url='loginpageview')
def shift_name_view(request):
	"""
		On Get request, this view displays ShiftNameForm to be filled.
		On Post request, it adds Shift-Name's information to db.
	"""
	if request.method == "POST":
		shift_name_form = ShiftNameForm(request.POST)
		if shift_name_form.is_valid():
			shift_name_form.save()
			messages.success(request, 'Shift Name was successfully added!')
			return redirect('homeview')
		else:
			messages.error(request, 'Error saving Shift Name information.')
			return redirect('homeview')

	shift_name_form = ShiftNameForm()
	return render(request=request, template_name="add_shift_name.html", context={'shift_name_form':shift_name_form})



@login_required(login_url='loginpageview')
def shift_name_dashboard(request):
	shift_name_objects = ShiftName.objects.all()
	all_data = list()
	for shift_name_object in shift_name_objects:
		shift_name_data = list()	
		shift_name_data.append(shift_name_object.id)
		shift_name_data.append(shift_name_object.shift_name)
		all_data.append(shift_name_data)

	context = {'alldata': all_data}
	return render(request,'shift_name_dashboard.html',context=context)



@login_required(login_url='loginpageview')
def update_shift_name(request, shift_name_id):
	"""
		This view updates information of a 'shift-name'.
		On Get request, it fetches and displays the shift-name data.
		On Post request, it updates the information and redirects to shift-name dashboard.
		params:
			shift_name_id : The id of a shift-name object.
	"""
	shift_name_object = ShiftName.objects.get(id=shift_name_id) # get returns the only matching object
	form = ShiftNameForm(instance=shift_name_object)

	if request.method=='POST':
		form=ShiftNameForm(request.POST, instance=shift_name_object)
		if form.is_valid():
			form.save()
			messages.success(request, 'Successfully updated Shift Name information.')
			return redirect('shiftnamedashboard')
		else:
			messages.error(request, 'Error updating Shift Name information.')
			return redirect('shiftnamedashboard')
	
	return render(request,'update_shift_name.html',context= {'shift_name_form':form, 'shift_name_id': shift_name_id})



@login_required(login_url='loginpageview')
def delete_shift_name(request, shift_name_id):
	"""
		This view deletes a shift-name object.
		params:
			shift_name_id:	id of shift-name object which is to be deleted
	"""
	shift_name_object = ShiftName.objects.get(id=shift_name_id)

	# deleting the object
	try:
		shift_name_object.delete()
		messages.success(request, 'Successfully deleted.')
		# redirecting back to the update view of the student
		return redirect('shiftnamedashboard')
	except Exception:
		messages.error(request, 'Error. Object could not be deleted. Try again.')
		return redirect('shiftnamedashboard')




# Course Section -------------------

