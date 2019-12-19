from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *


class CustomerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['phone_number', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(CustomerRegistrationForm, self).__init__(*args, **kwargs)


# class ClientRegistrationForm(UserCreationForm):
#     class Meta:
#         model = Client
#         fields = ['username', 'mobile_phone', 'email']
#
#     def __init__(self, *args, **kwargs):
#         super(ClientRegistrationForm, self).__init__(*args, **kwargs)
#         self.fields.pop('password2')


# class New_PortfolioForm(forms.ModelForm):
#     class Meta:
#         model = New_Portfolio
#         fields = '__all__'
#
#     def __init__(self, *args, **kwargs):
#         super(New_PortfolioForm, self).__init__(*args, **kwargs)
#         self.fields.pop('user')
#         self.fields.pop('experience')
#         self.fields.pop('budget')


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = FeedBack
        fields = ['user', 'customer', 'feedback']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = '__all__'


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answers
        fields = '__all__'
