import allauth.app_settings
from allauth import app_settings
from allauth.utils import get_username_max_length, set_form_field_order
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import pgettext

from .models import *
from allauth.account.forms import LoginForm, PasswordField

GENDER_CHOICES = (
    ('MALE', 'MALE'),
    ('FEMALE', 'FEMALE'),
    ('OTHERS', 'OTHERS'),
)


class MyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "{}".format(obj.name)


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=40)
    mobile_phone = forms.RegexField(max_length=10, required=True, regex=r'^\+?1?\d{9,15}$', widget=forms.TextInput(
        attrs={'class': 'input-sm form-control width-30', 'type': 'tel', 'pattern': '^\+?1?\d{9,15}$'}))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput())
    password2 = forms.CharField(required=True, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['email', 'mobile_phone', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['mobile_phone'].widget.attrs['class'] = \
            "form-control"
        self.fields['mobile_phone'].widget.attrs['placeholder'] = 'Mobile Number'
        self.fields['email'].widget.attrs['class'] = \
            "form-control"
        self.fields['email'].widget.attrs['placeholder'] = 'Email ID'
        self.fields['password1'].widget.attrs['class'] = \
            "form-control"
        self.fields['password1'].widget.attrs['placeholder'] = 'Password should be more than 8 letters and alphanumeric'
        self.fields['password2'].widget.attrs['class'] = \
            "form-control"
        self.fields['password2'].widget.attrs['placeholder'] = 'Password should be more than 8 letters and alphanumeric'

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists. Try a different Email-ID")
        return email
        # username = self.data['mobile_phone']
        # if User.objects.filter(username=username).exists():
        #     raise forms.ValidationError("Phone number already exists. Try a different Phone number")

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)

        user.email = self.cleaned_data['email']
        # user.username = self.cleaned_data['mobile_phone']
        if commit:
            user.save()
        return user

class DesignUploadsForm(forms.ModelForm):

    design_type = MyModelChoiceField(queryset=sub_category.objects.all())
    design_images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Design
        fields = ['design_type', 'design_name', 'design_images']
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super(DesignUploadsForm, self).__init__(*args, **kwargs)
        self.fields['design_type'].widget.attrs['class'] = \
            "form-control"
        self.fields['design_name'].widget.attrs['class'] = \
            "form-control"
        self.fields['design_images'].widget.attrs['class'] = \
            "form-control"
        self.fields['design_images'].required = False

class ProjectUploadsForm(forms.ModelForm):

    project_type = MyModelChoiceField(queryset=sub_category.objects.all())
    project_images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Project
        fields = ['project_type', 'project_name', 'project_images']
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super(ProjectUploadsForm, self).__init__(*args, **kwargs)
        self.fields['project_type'].widget.attrs['class'] = \
            "form-control"
        self.fields['project_name'].widget.attrs['class'] = \
            "form-control"
        self.fields['project_images'].widget.attrs['class'] = \
            "form-control"
        self.fields['project_images'].required = False

class PortfolioForm(forms.ModelForm):
    about_me = forms.CharField(widget=forms.Textarea(attrs={'rows': 10, 'cols': 30}))
    category = MyModelChoiceField(
        queryset=Category.objects.all(),
        required=False, )
    sub_category = MyModelChoiceField(queryset=sub_category.objects.all())

    class Meta:
        model = Portfolio
        fields = ['prefix', 'secondary_phone', 'gender',
                  'experience', 'qualification', 'profile_pic', 'about_me', 'budget', 'category',
                  'sub_category',
                  ]

    def __init__(self, *args, **kwargs):
        super(PortfolioForm, self).__init__(*args, **kwargs)
        self.fields['prefix'].widget.attrs['class'] = \
            "form-control"
        self.fields['experience'].widget.attrs['class'] = \
            "form-control"
        self.fields['budget'].widget.attrs['class'] = \
            "form-control"
