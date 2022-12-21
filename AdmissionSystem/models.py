from django.db import models
from django import  forms
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.

# model to add skill student 
class SkillStudent(models.Model):
	"""
		Skill Student Data Entry
	"""

	# drop down choices for pre qualification
	pre_qualification_choice = (
	('Matric','Matric'),
	('O-Levels','O-Levels'),
	('A-Levels','A-Levels'),
	('Inter','Inter'),
	('ADP','ADP'),
	('BS','BS'),
	('BE','BE'),
	('Masters','Masters'),
	('M.Phil','M.Phil'),
	('PhD','PhD'),
	)
	
	# drop down choices for residencial status
	residencial_status_choice = (
	('Hostel','Hostel'),
	('Local','Local'),
	)
	
	# drop down choices for gender
	gender_choice = (
	('Male','Male'),
	('Female','Female'),
	('Intersex','Intersex'),
	)

	# drop down choices for shifts
	shifts_choice = (
	('Morning','Morning'),
	('Afternoon','Afternoon'),
	('Evening','Evening'),
	('Night','Night'),
	)
	
	# drop down choices for program of interests
	program_of_interest_choice = (
	('Artifical Intelligence','Artifical Intelligence'),
	('Big Data','Big Data'),
	('Blockchain Programming','Blockchain Programming'),
	('Graphics Designing','Graphics Designing'),
	('Graphics and Web Design','Graphics and Web Design'),
	('Digital Marketing','Digital Marketing')
	)

	# drop down choices for transportations
	transportation_choice = (
	('Personal Conveyance','Personal Conveyance'),
	('Parent Conveyance','Parent Conveyance'),
	('Local Transport','Local Transport')
	)

	# drop down choices for admission status
	admissionstatus_choice = (
	('Contacted Virtually','Contacted Virtually'),
	('Reception Appearance','Reception Interview'),
	('Internal Interview','Internal Interview'),
	('External Interview','External Interview'),
	('Admitted','Admitted'),
	('Rejected','Rejected'),
	('Drop out','Drop out'),
	('Passed out','Passed out'),
	)

	# drop down choices information source
	informationsource_choice = (
	('Random Walk-in','Random Walk-in'),
	('Social Media','Social Media'),
	('By Reference','By Reference'),
	('Electronic Media','Electronic Media'),
	('On-Ground Advertisement ','On-Ground Advertisement'),
	('Relative','Relative'),
	('Neighbour','Neighbour'),
	('Friend','Friend'),
	('Class Fellow','Class Fellow'),
	('Any Other','Any Other'),
	)

	# to save student images to folder named to his form no
	def student_directory_path(instance, filename):
		return 'static/admissionsystem/student_images/%s/%s' % (instance.form_no, filename)

	form_no = models.CharField(max_length=100, null=True, blank=True)
	name = models.CharField(max_length=100)
	pre_qualification = models.CharField(max_length=100,choices=pre_qualification_choice)
	photograph = models.ImageField(upload_to=student_directory_path,blank=True, default='/static/default-images/default-student-img.jpg')
	gender = models.CharField(max_length=100,choices=gender_choice, null=True, blank=True)
	father_Name = models.CharField(max_length=100, null=True, blank=True)
	cnic_or_B_form_No = models.CharField(max_length=100,null=True,blank=True)
	email = models.EmailField(max_length=100,null=True,blank=True)
	domicile = models.CharField(max_length=100, null=True, blank=True)
	date_of_birth = models.DateField(null=True, blank=True)
	residencial_status = models.CharField(max_length=100,choices=residencial_status_choice, null=True, blank=True)
	address = models.CharField(max_length=600, null=True, blank=True)
	area = models.CharField(max_length=100, null=True, blank=True)
	laptop = models.BooleanField(null=True, blank=True)
	computer_at_Home = models.BooleanField(null=True, blank=True)
	shift = models.CharField(max_length=20,choices=shifts_choice, null=True, blank=True)
	program_of_interest = models.CharField(max_length=100,choices=program_of_interest_choice, null=True, blank=True)
	transportation = models.CharField(max_length=100,choices=transportation_choice, null=True, blank=True)
	information_source=models.CharField(max_length=100,choices=informationsource_choice, null=True, blank=True)
	admission_status = models.CharField(max_length=100,choices=admissionstatus_choice,default="Pending")
	date_applied=models.DateField(null=True,blank=True)
	created_by = models.CharField(max_length=100,null=True,blank=True)
	updated_by = models.CharField(max_length=100,null=True,blank=True)

	def __str__(self):
		return str(self.id)



# model to add conventional student 
class ConventionalStudent(models.Model):	
	# drop down choices for shifts
	shifts_choice = (
	('Morning','Morning'),
	('Evening','Evening'),
	)
	
	# drop down choices for admission status
	admissionstatus_choice = (
	('Contacted Virtually','Contacted Virtually'),
	('Reception Appearance','Reception Interview'),
	('Internal Interview','Internal Interview'),
	('External Interview','External Interview'),
	('Admitted','Admitted'),
	('Rejected','Rejected'),
	('Drop out','Drop out'),
	)

	# drop down choices for gender
	gender_choice = (
	('Male','Male'),
	('Female','Female'),
	)

	form_no = models.CharField(max_length=199,null=True,blank=True)
	name = models.CharField(max_length=100)
	gender = models.CharField(max_length=100,choices=gender_choice)
	cnic_or_B_form_No = models.CharField(max_length=100)
	father_Name = models.CharField(max_length=100)
	father_income = models.CharField(max_length=100)
	father_occupation = models.CharField(max_length=100)
	class_of_interest = models.CharField(max_length=199,null=True,blank=True)
	mobileno = models.CharField(max_length=100)
	domicile = models.CharField(max_length=100)
	date_of_birth = models.DateField()
	religion = models.CharField(max_length=100)
	district = models.CharField(max_length=100)
	email = models.EmailField(max_length=100)
	present_address=models.CharField(max_length=100)
	sport_person = models.BooleanField()
	hafiz = models.BooleanField()
	disability= models.BooleanField()
	shift = models.CharField(max_length=20,choices=shifts_choice)
	admission_status = models.CharField(max_length=100,choices=admissionstatus_choice,default="Pending")

	def __str__(self):
		return self.name

# query and its reply model for student
class Contacted(models.Model):
	student = models.ForeignKey(SkillStudent, on_delete=models.CASCADE, blank=True)
	query = models.TextField()
	reply = models.TextField()
	created_by = models.CharField(max_length=100, null=True, blank=True)
	updated_by = models.CharField(max_length=100, null=True, blank=True)
	
	def __str__(self):
		return str(self.student)

# model to add current study for student
class CurrentStudy(models.Model):
	student = models.ForeignKey(SkillStudent, on_delete=models.CASCADE, blank=True)
	program = models.CharField(max_length=100, null=True, blank=True)
	institute = models.CharField(max_length=100, null=True, blank=True)
	semester = models.CharField(max_length=100, null=True, blank=True)
	start_timings = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
	end_timings=models.TimeField(auto_now=False,auto_now_add=False, null=True, blank=True)
	institute_Address = models.CharField(max_length=100, null=True, blank=True)
	CGPA = models.DecimalField(max_digits=3 ,decimal_places=2, null=True, blank=True)
	created_by = models.CharField(max_length=100, null=True, blank=True)
	updated_by = models.CharField(max_length=100, null=True, blank=True)

	def __str__(self):
		return str(self.student)

# model to add short course names for student
class ShortCourseName(models.Model):
	"""
		gggg
	"""
	course_title=models.CharField(max_length=100)
	created_by = models.CharField(max_length=100, null=True, blank=True)
	updated_by = models.CharField(max_length=100, null=True, blank=True)	
	
	def __str__(self):
		return self.course_title

# model to add short course taken by student
class ShortCoursesTaken(models.Model):
	shortcoursetakentype_choice = (
	('Private','Private'),
	('NAVTTC','NAVTTC'),
	('PSDA','PSDA'),
	('TEVTA','TEVTA'),	
	('Digiskill','Digiskill'),
	('PIAIC','PIAIC'),
	)
	student = models.ForeignKey(SkillStudent, on_delete=models.CASCADE, blank=True)
	course_name=models.ForeignKey(ShortCourseName,on_delete=models.CASCADE, null=True, blank=True)
	course_type= models.CharField(max_length=100,choices=shortcoursetakentype_choice, null=True, blank=True)
	institute_name = models.CharField(max_length=100, null=True, blank=True)
	start_date = models.DateField(blank=True, null=True)
	end_date = models.DateField(blank=True, null=True)
	created_by = models.CharField(max_length=100, null=True, blank=True)
	updated_by = models.CharField(max_length=100, null=True, blank=True)	

	def __str__(self):
		return str(self.student)

# model to add job positions
class JobPosition(models.Model):
	job_title=models.CharField(max_length=100)
	created_by = models.CharField(max_length=100, null=True, blank=True)
	updated_by = models.CharField(max_length=100, null=True, blank=True)	
	
	def __str__(self):
		return str(self.job_title)

# model to add job for student
class Job(models.Model):
	student = models.ForeignKey(SkillStudent, on_delete=models.CASCADE, blank=True)
	position=models.ForeignKey(JobPosition,on_delete=models.DO_NOTHING, null=True, blank=True)
	company = models.CharField(max_length=100, null=True, blank=True)
	start_timings = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
	end_timings=models.TimeField(auto_now=False,auto_now_add=False, null=True, blank=True)
	salary = models.CharField(max_length=100, null=True, blank=True)
	company_address=models.CharField(max_length=100, null=True, blank=True)
	created_by = models.CharField(max_length=100, null=True, blank=True)
	updated_by = models.CharField(max_length=100, null=True, blank=True)	
	
	def __str__(self):
		return str(self.student)

# model to add phone numbers for student
class PhoneNo(models.Model):
	student = models.ForeignKey(SkillStudent, on_delete=models.CASCADE, blank=True)
	Personal_Phone_no_1 = models.CharField(max_length=100, null=True, blank=True)	
	Personal_Phone_no_2 = models.CharField(max_length=100, null=True, blank=True)	
	Father_Phone_no = models.CharField(max_length=100, null=True, blank=True)	
	Mother_Phone_no = models.CharField(max_length=100, null=True, blank=True)	
	Emergency_Phone_no = models.CharField(max_length=100, null=True, blank=True)	
	created_by = models.CharField(max_length=100, null=True, blank=True)
	updated_by = models.CharField(max_length=100, null=True, blank=True)	
	
	def __str__(self):
		return str(self.student)

# model for user profile with image
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='static/default-images/default-staff-female.png', upload_to='static/admissionsystem/user-images')
    def __str__(self):
        return f'{self.user.username} Profile'
    def save(self):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

	# educational background