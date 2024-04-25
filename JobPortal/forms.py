from django import forms
from .models import Candidate, Skill, Education, Experience, Job_Posting,Sector,Application, Interviews, application_status
from datetime import date
from django.forms import formset_factory
from phonenumber_field.formfields import PhoneNumberField
from froala_editor.widgets import FroalaEditor


class CandidateForm(forms.ModelForm):
    gender_list = [
    ('male', 'Male'),
    ('female', 'Female'),
]
    first_name = forms.CharField( max_length=20,widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'First Name (Required)'
    }))
    last_name = forms.CharField( max_length=20,widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Last Name (Required)'
    }))
    gender = forms.ChoiceField(choices=gender_list, widget=forms.Select(attrs={
        'class': 'form-select',
        'placeholder' : 'Select Gender (Required)'
    }))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={
        'class':'form-control',
        'type' : 'date',
        'placeholder' : 'mm/dd/yyyy (Required)'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class' : 'form-control',
        'placeholder':'Email (Required)'
    }))
    phone1 = forms.CharField(max_length=15, widget=forms.TextInput({
        'class' : 'form-control',
        'type': 'tel',
        'placeholder' : 'Phone 1 (Required)'
    }))
    phone2 = forms.CharField(max_length=15, required=False,widget=forms.TextInput({
        'class' : 'form-control',
        'type': 'tel',
        'placeholder' : 'Phone 1 (Optional)'
    }))
    address = forms.CharField(max_length=100,widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Address (Requires)'
    }))
    linked_in = forms.URLField(required=False, widget=forms.URLInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Linked In (Optional)'
    }))
    git_hub = forms.URLField(required=False, widget=forms.URLInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Git Hub (Optional)'
    }))
    country = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Country (required)'
    }))
    city = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'City (required)'
    })) 
    zip_code = forms.CharField(max_length=20, required=False,widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'ZIP (Optional)'
    }))
    photo = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={
        'class' : 'form-control text-sm ',
        'accept':'image/*',
    }))
    resume = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Resume (Optional)',
        'accept' : 'application/pdf application/vnd.ms-word'
    }))
    about = forms.CharField(widget=forms.Textarea(attrs={
        'class' : 'form-control',
        'placeholder' : 'About Your Self (Required)'
    }))
    
    
    class Meta:
        model = Candidate
        exclude = ['user']
    
    skill = forms.ModelMultipleChoiceField(required=True,queryset=Skill.objects.all())
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name or len(first_name) < 2:
            raise forms.ValidationError('Enter a Valid Name')
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name or  len(last_name) < 2:
            raise forms.ValidationError('Enter a Valid Name')
        return last_name
    
    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data['date_of_birth']
        min_date = date(1900, 1,1)
        max_date = date(2007, 1,1)
        if date_of_birth < min_date or date_of_birth > max_date:
            raise forms.ValidationError('Invalid date of Birth')
        return date_of_birth
    
    def clean_photo(self):
        photo = self.cleaned_data['photo']
        max_size_mb = 1
        max_size_bytes = max_size_mb * 1024 * 1024
        
        if not photo:
            return photo
        if photo.size > max_size_bytes:
            raise forms.ValidationError(
            ('The image file size is too large. Please upload an image smaller than 1 MB.'),
            code='invalid_image_size',
            params={'max_size_mb': max_size_mb},
            )
        return photo
    
    def clean_about(self):
        about = self.cleaned_data['about']
        if not about or len(about) < 10:
         raise forms.ValidationError('Enter a Valid Resume Content')
        return about

class EducationForm(forms.ModelForm):
    education_status_list = [
    ('none', 'Select Education (Required)'),
    ('highschool', 'High School'),
    ('Certificate', 'Certificate'),
    ('diploma', 'Diploma'),
    ('bachelor-degree', "Bachelor's degree"),
    ('Master-degree', "Master's Degree"),
    ('doctorate', "Doctorate"),
    ('other', 'Other')
]
    institution_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'Placeholder' : 'Institution Name (Required)'
    }))
    
    field_of_study = forms.CharField(max_length=40, widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'Placeholder' : 'Field Of Study (Required)'
    }))
    education_status = forms.ChoiceField(choices=education_status_list, widget=forms.Select(attrs={
        'class' : 'form-select bg-white text-dark ',

    }))
    education_period_start = forms.DateField(widget=forms.DateInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'DD-MM-YYYY (Required)',
        'type' : 'date'
    }))
    education_period_end = forms.DateField(widget=forms.DateInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'DD-MM-YYYY (Required)',
        'type' : 'date'
    }))
    class Meta:
        model = Education
        exclude = ['candidate']

class ExperienceForm(forms.ModelForm):
    company_name = forms.CharField(label='Company Name: ',max_length=40, widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Company Name (Required)'
    }))
    work_time_line_start = forms.DateField(label='Start Date: ', widget=forms.DateInput(attrs={
        'class' : 'form-control',
        'Placeholder' : 'mm/dd/yyyy (Required)',
        'type' : 'Date'
    }))
    work_time_line_end = forms.DateField(label='End Date: ', widget=forms.DateInput(attrs={
        'class' : 'form-control',
        'Placeholder' : 'mm/dd/yyyy (Required)',
        'type' : 'Date'
    }))
    job_title = forms.CharField(label='Job Title: ',max_length=40, widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Job Title (Required)'
    }))
    reference_phone = forms.CharField(label = 'Reference Phone: ', max_length=15, widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Phone (Required)',
    }))
    reference_name = forms.CharField(label='Job Title: ',max_length=40, widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Job Title (Required)'
    }))
    reference_email = forms.EmailField(label='Reference Email: ', widget=forms.EmailInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Reference Email (Required)'
    }))
    reference_job_title = forms.CharField(max_length=40,label='Reference Job Title: ', widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Reference Job Title (Required)'
    }))
    responsibility = forms.CharField(required=False, label='Your Responsibility: ',widget=forms.Textarea(attrs={
        'class' : 'form-control',
        'placeholder' : 'Your Responsibility (Optional)'
    }))
    class Meta:
        model = Experience
        exclude = ['candidate']



class JobPostingForm(forms.ModelForm):
    job_type = [
    ('full_time', 'Full Time'),
    ('part_time', 'Part Time'),
    ('freelance', 'Freelance'),
    ('internship', 'Internship'),
    ('seasonal ','seasonal'),
    ('contract', 'Contract'),
    ('remote', 'Remote'),
]
    
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control '
    }))
    sector = forms.ModelChoiceField(queryset=Sector.objects.all(), widget=forms.Select(attrs={
        'class' : 'form-select ',
        'onkeyup' : 'filterFunction()'
    }))

    experience = forms.CharField(widget=forms.TextInput(attrs={
        'class ' : 'form-control'
    }))

    skills = forms.ModelMultipleChoiceField(required=True,queryset=Skill.objects.all())
    location = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control'
    }))
    salary_range_start = forms.FloatField(widget=forms.NumberInput(attrs={
        'class' : 'form-control'
    }))
    salary_range_final = forms.FloatField(widget=forms.NumberInput(attrs={
        'class' : 'form-control'
    }))
    type = forms.ChoiceField(choices=job_type, widget=forms.Select(attrs={
        'class' : 'form-select'
    }))
    job_status = forms.BooleanField( required=False ,widget=forms.CheckboxInput(attrs={
        'class' : 'form-check-input'
    }))
    date_closed = forms.DateField(widget=forms.DateInput(attrs={
        'class' : 'form-control',
        'type' : 'date',
    }))
    description = forms.CharField(widget=FroalaEditor())
    

    class Meta:
        model = Job_Posting
        fields = '__all__'

        widgets = {
            'vacancies' : forms.NumberInput(attrs={
                'class' : 'form-control'
            })
        }

        def clean_vacancies(self):
           vacancies = self.cleaned_data['vacancies']
           if  vacancies < 1:
            raise forms.ValidationError('Enter a Valid Number')
           return vacancies

class SectorForm(forms.ModelForm):
    class Meta:
        model = Sector
        fields = '__all__'
    
        widgets = {
            'name' : forms.TextInput(attrs={
                'class' : 'form-control'
            })
        }


class ApplicationForm(forms.ModelForm):
    status = forms.ChoiceField(choices=application_status, required=False, widget=forms.Select(attrs={
        'class' : 'form-select'
    }))
    class Meta:
        model = Application
        fields = ('status',)

class InterviewForm(forms.ModelForm):
    
    class Meta:
        model = Interviews
        fields = '__all__'

        widgets = {
            'date_schedule' : forms.DateInput(attrs={
                'class' : 'form-control',
                'type' : 'date',
                'placeholder' : 'dd/mm/yy'
            }),
            'time_schedule' : forms.TimeInput(attrs={
                'class' : 'form-control',
                'type' : 'time'
            }),
            'status' : forms.Select(attrs={
                'class' : 'form-select'
            }),
            'type' : forms.Select(attrs={
                'class' : 'form-select'
            }),
         }

class InterviewerForm(forms.ModelForm):
    
    class Meta:
        model = Interviews
        fields = ('date_schedule','time_schedule', 'status','type')

        widgets = {
            'date_schedule' : forms.DateInput(attrs={
                'class' : 'form-control',
                'type' : 'date',
                'placeholder' : 'dd/mm/yy'
            }),
            'time_schedule' : forms.TimeInput(attrs={
                'class' : 'form-control',
                'type' : 'time'
            }),
            'status' : forms.Select(attrs={
                'class' : 'form-select'
            }),
            'job_status' : forms.Select(attrs={
                'class' : 'form-select'
            }),
            'type' : forms.Select(attrs={
                'class' : 'form-select'
            }),
            'interviewer' : forms.Select(attrs={
                'class' : 'form-select'
            }),
         }


class InterviewerNoteForm(forms.ModelForm):
    class Meta:
        model = Interviews
        fields = ('note',)

        widgets = {
            'note' : FroalaEditor()
        }