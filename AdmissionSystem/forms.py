from django import forms
from .models import *
 
class AddSkillStudentForm(forms.Form):


    admissionstatus_choice = [
    ('',''),
    ('Contacted Virtually','Contacted Virtually'),
    ('Reception Appearance','Reception Appearance'),
    ('Internal Interview','Internal Interview'),
    ('External Interview','External Interview'),
    ('Admitted','Admitted'),
    ('Rejected','Rejected'),
    ('Awaiting','Awaiting'),
    ('Drop out','Drop out'),
    ('Pass out','Pass out'),
    ]

    name = forms.CharField(required=True)
    personal_no_1 = forms.CharField(required=True)
    personal_no_2 = forms.CharField(required=False)
    area = forms.CharField(required=True)
    laptop = forms.CharField(required=True)
    availability_from = forms.TimeField(required=True)
    availabitity_to = forms.TimeField(required=True)
    date_applied = forms.DateField(required=True)
    pre_qualification = forms.ModelMultipleChoiceField(queryset=(PreQualification.objects.all()), required=True)
    currently_studying = forms.CharField()
    admission_status = forms.CharField(widget=forms.Select(choices=admissionstatus_choice), required=True)



class SkillStudentForm(forms.ModelForm):
    class Meta:
        model = SkillStudent
        fields = ('__all__')

class CurrentStudyForm(forms.ModelForm):    
    class Meta:
        model = CurrentStudy
        fields = ('__all__')

class PhoneNoForm(forms.ModelForm):
    class Meta:
        model = PhoneNo
        fields = ('__all__')

class ShortCoursesTakenForm(forms.ModelForm):
     class Meta:
        model = ShortCoursesTaken
        fields = ('__all__')

class JobForm(forms.ModelForm):
      class Meta:
        model = Job
        fields = ('__all__')

class ShortCourseNameForm(forms.ModelForm):
    class Meta:
        model = ShortCourseName
        fields = ('__all__')

class JobPositionForm(forms.ModelForm):
    class Meta:
        model = JobPosition
        fields = ('__all__')

class ContactedForm(forms.ModelForm):
    class Meta:
        model = Contacted
        fields = ('__all__')


class PrequalificaitonForm(forms.ModelForm):
    class Meta:
        pass


class StudentCustomSearchForm(forms.Form):
    pre_qualification_choice = [
    ('',''),
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
    ]
    
    # drop down choices for residencial status
    residencial_status_choice = [
    ('',''),
    ('Hostel','Hostel'),
    ('Local','Local'),
    ]
    
    # drop down choices for gender
    gender_choice = [
    ('',''),
    ('Male','Male'),
    ('Female','Female'),
    ('Intersex','Intersex'),
    ]

    # drop down choices for shifts
    shifts_choice = [
    ('',''),
    ('Morning','Morning'),
    ('Afternoon','Afternoon'),
    ('Evening','Evening'),
    ('Night','Night'),
    ]
    
    # drop down choices for program of interests
    program_of_interest_choice = [
    ('',''),
    ('Artifical Intelligence','Artifical Intelligence'),
    ('Big Data','Big Data'),
    ('Blockchain Programming','Blockchain Programming'),
    ('Graphics Designing','Graphics Designing'),
    ('Graphics and Web Design','Graphics and Web Design'),
    ('Digital Marketing','Digital Marketing')
    ]

    # drop down choices for transportations
    transportation_choice = [
    ('',''),
    ('Personal Conveyance','Personal Conveyance'),
    ('Parent Conveyance','Parent Conveyance'),
    ('Local Transport','Local Transport')
    ]

    # drop down choices for admission status
    admissionstatus_choice = [
    ('',''),
    ('Contacted Virtually','Contacted Virtually'),
    ('Reception Appearance','Reception Appearance'),
    ('Internal Interview','Internal Interview'),
    ('External Interview','External Interview'),
    ('Admitted','Admitted'),
    ('Rejected','Rejected'),
    ('Awaiting','Awaiting'),
    ('Drop out','Drop out'),
    ('Pass out','Pass out'),
    ]

    created_by_choice = [
    ('',''),
    ('abdullah','abdullah'),
    ('zain','zain'),
    ('sana','sana'),
    ('mahrukh','mahrukh'),
    ('maryam','maryam')
    ]

    shift=forms.CharField(label='Shift', widget=forms.Select(choices=shifts_choice), required=False)
    program_of_interest = forms.CharField(label = 'Program', widget=forms.Select(choices=program_of_interest_choice), required=False)
    admission_status = forms.CharField(label='Admission Status', widget=forms.Select(choices=admissionstatus_choice), required=False)
    created_by = forms.CharField(label='Added by', widget=forms.Select(choices=created_by_choice) , required=False)
