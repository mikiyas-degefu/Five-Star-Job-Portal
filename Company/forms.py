from django import forms
from  .models import Comment, Contact_Message, Company
from froala_editor.widgets import FroalaEditor

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name','logo', 'slogan', 'about', 'email', 'address', 'phone', 'since', 'location', 'website']

        widgets = {
            'name' : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : '*Required'
            }),
            'logo' : forms.ClearableFileInput(attrs={
                'class' : 'form-control',
                'placeholder' : '*Required'
            }),
             'slogan' : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : '*Required'
            }),
            'about' : FroalaEditor,
            'email' : forms.EmailInput(attrs={
                'class' : 'form-control',
                'placeholder' : '*Required'
            }),
            'address' : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : '*Required'
            }),
            'phone' : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : '*Required'
            }),
            'since' : forms.DateInput(attrs={
                'class' : 'form-control',
                'type' : 'date',
                'placeholder' : '*Required'
            }),
            'location' : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : '*Required'
            }),
            'website' : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : '*Required'
            })
        }

class CommentForm(forms.ModelForm):
    name = forms.CharField(max_length=40, error_messages={'required' : 'Can not be empty'})
    email = forms.EmailField(widget=forms.TextInput(), error_messages={'required' : 'Can not be empty'})
    comment = forms.CharField(widget=forms.TextInput(), error_messages={'required': 'Can not be empty'})
    
    class Meta:
        model = Comment
        fields = ['name', 'email', 'comment']

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 2:
            raise forms.ValidationError(' Enter a valid name.')
        return name

class ContactForm(forms.ModelForm):
    name = forms.CharField(max_length=40, error_messages={'required' : 'Can not be empty'})
    email = forms.EmailField(error_messages={'required' : 'Can not be empty'})
    subject = forms.CharField(error_messages={'required' : 'Can not be empty'})
    message = forms.CharField(widget=forms.TextInput, error_messages={'required' : 'Can not be empty'})

    class Meta:
        model = Contact_Message
        fields = '__all__'
    
    def clean_name(self):
     name = self.cleaned_data['name']
     if len(name) < 2:
         raise forms.ValidationError(' Enter a valid name.')
     return name
