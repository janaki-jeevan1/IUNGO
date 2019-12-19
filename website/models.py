# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User,AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import date
from .validations import validate_file_extension
import datetime, os

from django.core.files.storage import FileSystemStorage

# Create your models here.

PREFIX_CHOICES = (
    ('MR', 'MR'),
    ('MRS', 'MRS'),
    ('MS', 'MS'),
    ('MX', 'MX')
)

RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

EXPERIENCE_CHOICES = [(i, str(i)) for i in range(51)]

BUDGET_CHOICES = [(i, str(i)) for i in range(101)]

QUALIFICATION_CHOICES = (
    ('UG', 'UNDER GRADUATE'),
    ('GRADUATE', 'GRADUATE'),
    ('PG', 'POST GRADUATE'),
    ('PhD', 'PhD'),
)

GENDER_CHOICES = (
    ('MALE', 'MALE'),
    ('FEMALE', 'FEMALE'),
)


def change_file_path(instance, filename):
    ''' This function generates a random string of length 16 which will be a combination of (4 digits + 4
    characters(lowercase) + 4 digits + 4 characters(uppercase)) seperated 4 characters by hyphen(-) '''

    import random
    import string

    # random_str length will be 16 which will be combination of (4 digits + 4 characters + 4 digits + 4 characters)

    filetype = filename.split(".")[-1].lower()
    filename = filename + "." + filetype
    path = "MyANSRSource/uploads/" + str(datetime.datetime.now().year) + "/" + str(
        datetime.datetime.now().month) + "/" + str(datetime.datetime.now().day) + "/"
    os_path = os.path.join(path, filename)
    return os_path


def content_file_name(instance, filename):
    ''' This function generates a random string of length 16 which will be a combination of (4 digits + 4
    characters(lowercase) + 4 digits + 4 characters(uppercase)) seperated 4 characters by hyphen(-) '''

    import random
    import string

    # random_str length will be 16 which will be combination of (4 digits + 4 characters + 4 digits + 4 characters)

    filetype = filename.split(".")[-1].lower()
    filename = filename
    path = "uploads/" + str(instance.user)
    os_path = os.path.join(path, filename)
    return os_path


class Customer(models.Model):
    phone_number = models.CharField(verbose_name="Mobile phone", max_length=10, unique=True, blank=False, null=True)
    email = models.EmailField()
    password = models.CharField(max_length=20)
    con_password=models.CharField(max_length=20)

    def __str__(self):
        return self.id


# class Client(AbstractUser):
#     mobile_phone = models.CharField(verbose_name="Mobile phone", max_length=10, unique=True, blank=False, null=True)
#     USERNAME_FIELD = 'mobile_phone'
#
#     def __str__(self):
#         return self.username

class Appointment(models.Model):
    user = models.ForeignKey(User, related_name="client_appointment", on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, related_name="customer_appointment", on_delete=models.CASCADE)
    status = models.BooleanField(verbose_name='Status', default=False)
    date_time = models.DateField(verbose_name="Actual BRS Start Date", blank=True, null=True)

class Parameters(models.Model):
    user = models.ForeignKey(User, related_name="client", on_delete=models.CASCADE)
    clicks = models.CharField(verbose_name="clicks", max_length=10)
    date_time = models.DateField(verbose_name="Actual BRS Start Date", blank=True, null=True)

    def __unicode__(self):
        return u'{0}'.format(self.user)

class FeedBack(models.Model):
    user = models.ForeignKey(User, related_name="client_feedback", on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, related_name="Customer_feedback", on_delete=models.CASCADE)
    feedback = models.CharField(verbose_name="Feedback", max_length=250)
    date_time = models.DateTimeField(verbose_name="Actual BRS Start Date", auto_now_add = True)

    def __str__(self):
        return self.feedback


class Rating(models.Model):
    user = models.ForeignKey(User, related_name="client_rating", on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, related_name="Customer_rating", on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(null=True, choices=RATING_CHOICES, blank=False, default=0)
    date_time = models.DateField(verbose_name="Actual BRS Start Date",auto_now_add =True)

    def __str__(self):
        return self.rating


class Questions(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    question_title = models.TextField(max_length=200)
    question_description=models.TextField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_title


class Answers(models.Model):
    question=models.ForeignKey(Questions,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.TextField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.answer
