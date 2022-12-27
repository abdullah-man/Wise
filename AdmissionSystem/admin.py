from django.contrib import admin
from .models import *
from .models import UserProfile

# customizing backend ADMIN page
admin.site.site_header = 'WISE | Adminsitration'           # default: "Django Administration"
admin.site.index_title = 'WISE Admin Area'                 # default: "Site administration"
admin.site.site_title = 'Wise Institute'                   # default: "Site Title"


# Register your models here.
admin.site.register(PreQualification)
admin.site.register(SkillStudent)
admin.site.register(Contacted)
admin.site.register(CurrentStudy)
admin.site.register(ShortCourseName)
admin.site.register(ShortCoursesTaken)
admin.site.register(JobPosition)
admin.site.register(Job)
admin.site.register(PhoneNo)
admin.site.register(UserProfile)
admin.site.register(DocumentType)
admin.site.register(Document)
admin.site.register(StudentAvailability)
admin.site.register(RollNo)
admin.site.register(CourseConductingBody)
admin.site.register(CourseName)
admin.site.register(CourseBatchNo)
admin.site.register(CourseSection)
admin.site.register(ShiftName)
admin.site.register(CourseApplication)
admin.site.register(AlreadyRegisteredWithCourseBody)



