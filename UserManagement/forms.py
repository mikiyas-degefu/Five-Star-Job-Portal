from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from .models import CustomUser
from Company.models import Company
from django.urls import reverse_lazy

class Login_Form(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Enter Your Email'
    }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Enter Your Password'
    }))

class CustomUserEditForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=Company.objects.all(), widget=forms.Select(attrs={
        'class' : 'form-select ',
        'onkeyup' : 'filterFunction()'
    }))
    date_of_birth = forms.DateField(label='End Date: ', widget=forms.DateInput(attrs={
        'class' : 'form-control',
        'Placeholder' : 'mm/dd/yyyy (Required)',
        'type' : 'Date'
    }))
    class Meta:
        model = CustomUser
        fields =  ('first_name', 'last_name', 'photo', 'gender', 'date_of_birth', 'email', 'phone', 'company', 'address', 'linked_in', 'country', 'city')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control-file'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'linked_in': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
        }



class CustomUserEditFormAdmin(forms.ModelForm):
    date_of_birth = forms.DateField(label='End Date: ', widget=forms.DateInput(attrs={
        'class' : 'form-control',
        'Placeholder' : 'mm/dd/yyyy (Required)',
        'type' : 'Date'
    }))
    class Meta:
        model = CustomUser
        fields =  ('first_name', 'last_name', 'photo', 'gender', 'date_of_birth', 'email', 'phone', 'address', 'linked_in', 'country', 'city')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'linked_in': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
        }



class CustomUserEditFormCompanyAdmin(forms.ModelForm):
    date_of_birth = forms.DateField(label='End Date: ', widget=forms.DateInput(attrs={
        'class' : 'form-control',
        'Placeholder' : 'mm/dd/yyyy (Required)',
        'type' : 'Date'
    }))
    class Meta:
        model = CustomUser
        fields =  ('first_name', 'last_name', 'photo', 'gender', 'date_of_birth', 'email', 'phone', 'address', 'linked_in', 'country', 'city')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'linked_in': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
        }
        

class CustomUserCreationForm(UserCreationForm):

    password1 = forms.CharField( max_length=40, label='Password' ,widget=forms.PasswordInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Enter Your Password',
        'autocomplete': 'off'
    }))
    password2 = forms.CharField( max_length=40, label='Confirm Password', widget=forms.PasswordInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Confirm Password',
        'autocomplete': 'off'
    }))

  
    class Meta:
        model = CustomUser
        fields =  ('first_name', 'last_name', 'email','username')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class CompanyAdmin(UserCreationForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Your First Name'
    }))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Your Last Name'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Enter your Email',
        'autocomplete': 'off'
    }))
    
    password1 = forms.CharField( max_length=40, label='Password' ,widget=forms.PasswordInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Enter Your Password',
        'autocomplete': 'off'
    }))
    password2 = forms.CharField( max_length=40, label='Confirm Password', widget=forms.PasswordInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Confirm Password',
        'autocomplete': 'off'
    }))
    photo = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Add Photo(Optional)',
   
    }))
    date_of_birth = forms.DateField(label='Date of Birth: ', widget=forms.DateInput(attrs={
        'class' : 'form-control',
        'Placeholder' : 'mm/dd/yyyy (Required)',
        'type' : 'Date'
    }))
 
  

    class Meta:
        model = CustomUser
        fields =  ('first_name', 'last_name', 'username', 'photo', 'gender', 'date_of_birth', 'email', 'phone', 'address', 'linked_in', 'country', 'city')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control-file'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'linked_in': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
        }



class CompanyInterviewer(UserCreationForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Your First Name'
    }))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Your Last Name'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Enter your Email',
        'autocomplete': 'off'
    }))
    password1 = forms.CharField( max_length=40, label='Password' ,widget=forms.PasswordInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Enter Your Password',
        'autocomplete': 'off'
    }))
    password2 = forms.CharField( max_length=40, label='Confirm Password', widget=forms.PasswordInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Confirm Password',
        'autocomplete': 'off'
    }))
    photo = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Add Photo(Optional)',
   
    }))
    date_of_birth = forms.DateField(label='End Date: ', widget=forms.DateInput(attrs={
        'class' : 'form-control',
        'Placeholder' : 'mm/dd/yyyy (Required)',
        'type' : 'Date'
    }))
 
  

    class Meta:
        model = CustomUser
        fields =  ('first_name', 'last_name', 'photo', 'gender', 'date_of_birth', 'email', 'phone', 'address', 'linked_in', 'country', 'city')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control-file'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'linked_in': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
        }


class InterviewerForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Your First Name'
    }))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Your Last Name'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Enter your Email',
        'autocomplete': 'off'
    }))
    photo = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Add Photo(Optional)',
   
    }))


    class Meta:
        model = CustomUser
        fields = ('first_name','last_name', 'email', 'photo')
    




class ChangePasswordForm(PasswordChangeForm):
    error_css_class = 'text-danger'
    old_password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'current-password', 'autofocus': True, 'class': 'form-control',
                   'placeholder': 'Old Password'}),
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', 'class': 'form-control', 'placeholder': 'New Password'}),
        strip=False,
    )
    new_password2 = forms.CharField(
        strip=False,
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', 'class': 'form-control', 'placeholder': 'Confirm password'}),
    )
