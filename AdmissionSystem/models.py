from django.db import models
from django import  forms
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.

class PreQualification(models.Model):
	"""
		Pre-Qualificaiton is last degree or certificate gotten by a student.
	"""
	pre_qualification_name = models.CharField(max_length=10, blank=True)
	created_by = models.CharField(max_length=100,null=True,blank=True)
	updated_by = models.CharField(max_length=100,null=True,blank=True)

	def __str__(self):
		return str(self.pre_qualification_name)

# model to add skill student 
class SkillStudent(models.Model):
	"""
		Skill Student details.
	"""
	
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
		return 'static/admissionsystem/student_images/{0}/{1}'.format(instance.id, filename)

	name = models.CharField(max_length=100)
	pre_qualification = models.ForeignKey(PreQualification, on_delete=models.SET_NULL, null=True, blank=True)
	photograph = models.ImageField(upload_to=student_directory_path,blank=True, default='/static/default-images/default-student-img.jpg')
	gender = models.CharField(max_length=100,choices=gender_choice, null=True, blank=True)
	father_Name = models.CharField(max_length=100, null=True, blank=True)
	cnic = models.CharField(max_length=100,null=True,blank=True)
	b_form = models.CharField(max_length=100,null=True,blank=True)
	email = models.EmailField(max_length=100,null=True,blank=True)
	domicile = models.CharField(max_length=100, null=True, blank=True)
	date_of_birth = models.DateField(null=True, blank=True)
	residencial_status = models.CharField(max_length=100,choices=residencial_status_choice, null=True, blank=True)
	address = models.CharField(max_length=600, null=True, blank=True)
	area = models.CharField(max_length=100, null=True, blank=True)
	laptop = models.BooleanField(null=True, blank=True)
	computer_at_Home = models.BooleanField(null=True, blank=True)
	transportation = models.CharField(max_length=100,choices=transportation_choice, null=True, blank=True)
	information_source=models.CharField(max_length=100,choices=informationsource_choice, null=True, blank=True)
	reference = models.CharField(max_length=100, blank=True)
	created_by = models.CharField(max_length=100,null=True,blank=True)
	updated_by = models.CharField(max_length=100,null=True,blank=True)

	def __str__(self):
		return str(self.id)


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
	student = models.OneToOneField(SkillStudent, on_delete=models.CASCADE, blank=True)
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
	student = models.OneToOneField(SkillStudent, on_delete=models.CASCADE, blank=True)
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

	

class DocumentType(models.Model):
	"""
		Name/Type of a document.
	"""

	doc_type = models.CharField(max_length=100)
	created_by = models.CharField(max_length=100)
	updated_by = models.CharField(max_length=100, null=True, blank=True)

	def __str__(self):
		return str(self.doc_type)

class Document(models.Model):
	"""
		Document of a student. A student can have multiple documents.
	"""
	
	def student_directory_path(instance, filename):
		return 'static/admissionsystem/student_images/{0}/{1}'.format(instance.student, filename)

	student = models.ForeignKey(SkillStudent, on_delete=models.CASCADE)
	doc_type = models.ForeignKey(DocumentType, on_delete=models.SET_DEFAULT, default='DOC')
	doc_file = models.FileField(upload_to=student_directory_path)
	original_held = models.BooleanField(default=None)
	created_by = models.CharField(max_length=100)
	updated_by = models.CharField(max_length=100, null=True, blank=True)

	def __str__(self):
		return str(self.doc_type) + "_" + str(self.student)


class StudentAvailability(models.Model):
	"""
		Availability of a student. A student can be available in multiple
		time slots in a day.
	"""
	student = models.ForeignKey(SkillStudent, on_delete=models.CASCADE)
	available_from = models.TimeField(auto_now=False,auto_now_add=False)
	available_to = models.TimeField(auto_now=False,auto_now_add=False)

	def __str__(self):
		return "availability of "+ str(self.student)


class RollNo(models.Model):
	"""
		Roll-number of a student.
	"""
	Student = models.OneToOneField(SkillStudent, on_delete=models.CASCADE)
	roll_no = models.CharField(max_length=100)
	created_by = models.CharField(max_length=100)
	updated_by = models.CharField(max_length=100, null=True, blank=True) # can be updated if abbreviation of course name or conducting body get modified

	def __str__(self):
		return str(self.roll_no)

class CourseConductingBody(models.Model):
	course_conducting_body_name = models.CharField(max_length=50)
	course_conducting_body_abbreviation = models.CharField(max_length=10)
	created_by = models.CharField(max_length=100)
	updated_by = models.CharField(max_length=100, null=True, blank=True)

	def __str__(self):
		return str(self.course_conducting_body_name)


class CourseName(models.Model):
	course_name = models.CharField(max_length=100)
	course_abbreviation = models.CharField(max_length=10)
	created_by = models.CharField(max_length=100)
	updated_by = models.CharField(max_length=100, null=True, blank=True)

	def __str__(self):
		return str(self.course_name)


class CourseBatchNo(models.Model):
	course_batch_no = models.CharField(max_length=10)
	created_by = models.CharField(max_length=100)
	updated_by = models.CharField(max_length=100, null=True, blank=True)

	def __str__(self):
		return str(self.course_batch_no)


class CourseSection(models.Model):
	course_section = models.CharField(max_length=10)
	created_by = models.CharField(max_length=100)
	updated_by = models.CharField(max_length=100, null=True, blank=True)

	def __str__(self):
		return str(self.course_section)


class ShiftName(models.Model):
	shift_name = models.CharField(max_length=10)
	created_by = models.CharField(max_length=100)
	updated_by = models.CharField(max_length=100, null=True, blank=True)

	def __str__(self):
		return str(self.shift_name)

class CourseApplication(models.Model):
	"""
		Course application. A student can have multiple course applications 
		for different courses. 
	"""

	# drop down choices for admission status
	admissionstatus_choice = (
	('Contacted Virtually','Contacted Virtually'),
	('Reception Appearance','Reception Interview'),
	('Internal Interview','Internal Interview'),
	('External Interview','External Interview'),
	('Admitted','Admitted'),
	('Rejected','Rejected'),
	('Awaiting','Awaiting'),
	('Drop out','Drop out'),
	('Passed out','Passed out'),
	)
	form_no = models.CharField(max_length=100, null=True, blank=True)
	# only two fields are required to create a course application object: date and admission status
	# rest are optional, hence, given null=True
	date_applied=models.DateField(null=True, blank=True)
	admission_status = models.CharField(max_length=100,choices=admissionstatus_choice)
	remarks = models.TextField(max_length=1000, null=True, blank=True)

	course_body = models.ForeignKey(CourseConductingBody, on_delete=models.SET_NULL, null=True, blank=True)
	course_name = models.ForeignKey(CourseName, on_delete=models.SET_NULL, null=True, blank=True)
	batch = models.ForeignKey(CourseBatchNo, related_name="course_batch_id", on_delete=models.SET_NULL, null=True, blank=True)
	section = models.ForeignKey(CourseBatchNo, related_name="course_section_id", on_delete=models.SET_NULL, null=True, blank=True)
	shift = models.ForeignKey(ShiftName, on_delete=models.SET_NULL, null=True, blank=True)

	created_by = models.CharField(max_length=100)
	updated_by = models.CharField(max_length=100, null=True, blank=True)

	def __str__(self):
		return "application "+str(self.id)

class AlreadyRegisteredWithCourseBody(models.Model):
	"""
		A student may already be registered in databases of multiple course conducting bodies.
	"""
	student = models.ForeignKey(SkillStudent, on_delete=models.CASCADE)
	course_body = models.ForeignKey(CourseConductingBody, on_delete=models.SET_NULL, null=True)
	created_by = models.CharField(max_length=100)
	updated_by = models.CharField(max_length=100, null=True, blank=True)

	def __str__(self):
		return "student "+str(self.student)+" already applied in"+str(self.course_body)
