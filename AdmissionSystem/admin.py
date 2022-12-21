from django.contrib import admin
from .models import SkillStudent,ConventionalStudent,CurrentStudy,PhoneNo, ShortCoursesTaken,Job,ShortCourseName,JobPosition, Contacted
from .models import UserProfile

# customizing backend ADMIN page
admin.site.site_header = 'WISE | Adminsitration'           # default: "Django Administration"
admin.site.index_title = 'WISE Admin Area'                 # default: "Site administration"
admin.site.site_title = 'Wise Institute'                   # default: "Site Title"


# Register your models here.
admin.site.register(ConventionalStudent)
admin.site.register(SkillStudent)
admin.site.register(CurrentStudy)
admin.site.register(PhoneNo)
admin.site.register(ShortCoursesTaken)
admin.site.register(Job)
admin.site.register(ShortCourseName)
admin.site.register(JobPosition)
admin.site.register(Contacted)
admin.site.register(UserProfile)

