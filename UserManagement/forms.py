from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class Login_Form(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Enter Your Email'
    }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Enter Your Password'
    }))


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Your First Name'
    }))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Your Last Name'
    }))
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Enter your Username',
        'autocomplete': 'off' 
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

    is_superuser = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class' : 'form-check-input'
    }))

    is_admin = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class' : 'form-check-input'
    }))

    is_interviewer = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class' : 'form-check-input'
    }))

    class Meta:
        model = CustomUser
        fields = ('first_name','last_name', 'username', 'is_interviewer' , 'is_superuser', 'is_admin', 'email','password1', 'password2', 'photo')


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
    

