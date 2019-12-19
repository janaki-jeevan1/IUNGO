# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.shortcuts import render, redirect, render_to_response
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.contrib.auth import login, authenticate
from django.contrib import auth
from django.shortcuts import render, get_object_or_404
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from django.template.context_processors import csrf
from website.models import Parameters
from django.views.generic import View
from random import randint
import random
import string
from django.core.mail import send_mail
from .commands.sms.send_sms import sendSMS
import json

# Create your views here.
global_otp = []


def random_with_N_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


def sms_user():
    otp = random_with_N_digits(4)
    return otp


def send_sms_user(request):
    number = request.GET.get('number')
    generate_otp = sms_user()
    resp = sendSMS('vV4ixMZmyok-YTys5TMHMljOCzBrfZDYc6aQzUED2B', '91' + number,
                   'TXTLCL', 'OTP to login ' + str(generate_otp))
    global_otp.append(generate_otp)
    return HttpResponse('')


def logout(request):
    auth.logout(request)
    return render(request, 'login.html', {})


def send_registration_confirmation(username):
    # user = request.user
    user = User.objects.get(username=username)
    confirmation_code = ''.join(
        random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for x in range(33))
    ccc = ConfirmationCode(confirmation_code=confirmation_code, user=user)
    ccc.save()
    p = ccc
    title = "Thanks for registration"
    content = "http://192.168.0.79:8000/confirmation/" + str(p.confirmation_code) + "/" + user.username
    send_mail(title, content, 'bharath@iungoadvantec.com', [user.email], fail_silently=False)


def confirmation(request, confirmation_code, username):
    try:
        username = User.objects.get(username=username)
        ccc = ConfirmationCode(confirmation_code=confirmation_code, user=username)
        if ccc.confirmation_code == confirmation_code and username.date_joined > timezone.make_aware(
                datetime.datetime.now() - datetime.timedelta(days=1)):
            username.is_active = True
            username.save()
            username.backend = 'django.contrib.auth.backends.ModelBackend'
            auth.login(request, username)
        return HttpResponseRedirect('/client/welcome')
    except:
        return HttpResponseRedirect('/client/client_register')


def welcome(request):
    context = {}
    return render(request, 'welcome.html', context)

def client_register(request):
    if request.method == "GET":
        context = {}
        context.update(csrf(request))
        context['form'] = RegistrationForm()
        return render_to_response('register.html', context)

    if request.method == 'POST':
        context = {}
        form = RegistrationForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.is_active = 1
            obj.email = form.cleaned_data["email"]
            obj.username = form.cleaned_data['email'].split('@')[0]
            obj.save()
            obj.portfolio.mobile_phone = form.cleaned_data["mobile_phone"]
            obj.portfolio.client = 1
            # send_registration_confirmation(obj.username)
            obj.save()
            return redirect('/client/client_login')
        else:
            return render(request, 'register.html', {'form': form})


def auth_view(request):
    username = request.POST.get('username', '')
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')
    otp = request.POST.get('OTP', '')
    if username and password:
        number = User.objects.get(portfolio__mobile_phone=username)
        if number:
            user = auth.authenticate(username=number.username,password=password)
            try:
                userobj = User.objects.get(portfolio__mobile_phone=username)
            except Portfolio.DoesNotExist:
                messages.error(request, 'Phone number does not exist, please register and try again.')
                return render(request, 'login.html')
        else:
            messages.error(request, 'Phone number does not exist, please register and try again.')
            return render(request, 'login.html')
    elif email and password:
        user_email = User.objects.get(email=email)
        if user_email:
            user = auth.authenticate(username=user_email.username, email=email, password=password)
            try:
                userobj = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, 'Email does not exist, Please register and try again.')
                return render(request, 'login.html')
        else:
            messages.error(request, 'Email does not exist, Please register and try again.')
            return render(request, 'login.html')
    elif username and global_otp:
        if otp == str(global_otp[0]):
            number = User.objects.get(portfolio__mobile_phone=username)
            if number:
                user = auth.authenticate(username=number.username, portfolio__mobile_number=username)
                try:
                    userobj = User.objects.get(portfolio__mobile_phone=username)
                    if userobj.is_active is True:
                        auth.login(request, user)
                        global_otp.remove(global_otp[0])
                        return HttpResponseRedirect('/client/portfolio')
                except User.DoesNotExist:
                    messages.error(request, 'Phone number does not exist, please register and try again.')
                    return render(request, 'login.html')
            else:
                messages.error(request, 'Phone number does not exist, please register and try again.')
                return render(request, 'login.html')
        else:
            messages.error(request, 'Invalid OTP')
            return render(request, 'login.html')
    else:
        user = None
    if user is not None and userobj.is_active is True:
        auth.login(request, user)
        return HttpResponseRedirect('/client/portfolio')
    else:
        messages.error(request, 'Invalid Username or password')
        return render(request, 'login.html')


def client_login(request):
    if request.method == 'GET':
        context = {}
        return render(request, 'login.html', context)

    if request.method == 'POST':
        context = {}
        return render(request, 'login.html', context)


class Dashboard(View):
    template_name = "client_dashboard.html"

    def get(self, request):
        context = {}
        context['user'] = request.user
        return render(request, self.template_name, context)

    def post(self, request):
        context = {}
        return render(request, self.template_name, context)


def dates_to_check(start_date, end_date):
    dates = []
    delta = end_date - start_date

    for i in range(delta.days + 1):
        dates.append(start_date + datetime.timedelta(days=i))
    return dates


def Overview(request):
    if request.method == 'GET':
        context = {}
        id = request.GET.get('id')
        if id:
            today = date.today()
            week_ago = today - datetime.timedelta(days=6)
            dates = dates_to_check(week_ago, today)
            final_list = []
            for date_check in dates:
                if id == "1":
                    click_dict = {}
                    no_of_clicks = Parameters.objects.filter(user=request.user, date_time=date_check)
                    clicks = []
                    if len(no_of_clicks) > 0:
                        for i in no_of_clicks:
                            clicks.append(int(i.clicks))
                        clicks_total = sum(clicks)
                    else:
                        clicks_total = 0
                    click_dict['clicks'] = clicks_total
                    click_dict['date'] = date_check.strftime("%Y-%m-%d")
                    final_list.append(click_dict)
                if id == "2":
                    views_dict = {}
                    no_of_views = Parameters.objects.filter(user=request.user, date_time=date_check)
                    views = []
                    if len(no_of_views) > 0:
                        for i in no_of_views:
                            views.append(int(i.views))
                        views_total = sum(views)
                    else:
                        views_total = 0
                    views_dict['views'] = views_total
                    views_dict['date'] = date_check.strftime("%Y-%m-%d")
                    final_list.append(views_dict)
                    # feedback_dict = {}
                    # no_of_feedbacks = FeedBackRating.objects.filter(user=request.user, date_time=date_check)
                    # feedback_dict['feebacks'] = len(no_of_feedbacks)
                    # feedback_dict['date'] = date_check.strftime("%Y-%m-%d")
                    # final_list.append(feedback_dict)
                # if id == "3":
                #     design_dict = {}
                #     invoice_dict = {}
                #     proposals_dict = {}
                #     no_of_invoices = InvoicesProposalsUploads.objects.filter(user=request.user,
                #                                                              date_time=date_check).values('invoices')
                #     no_of_proposals = InvoicesProposalsUploads.objects.filter(user=request.user,
                #                                                               date_time=date_check).values('proposals')
                #     no_of_designs = DeisgnUploads.objects.filter(user=request.user, date_time=date_check)
                #     design_dict['designs'] = len(no_of_designs)
                #     design_dict['date'] = date_check.strftime("%Y-%m-%d")
                #     invoice_dict['invoices'] = len(no_of_invoices)
                #     invoice_dict['date'] = date_check.strftime("%Y-%m-%d")
                #     proposals_dict['proposals'] = len(no_of_proposals)
                #     proposals_dict['date'] = date_check.strftime("%Y-%m-%d")
                #     final_list.append(design_dict)
                #     final_list.append(invoice_dict)
                #     final_list.append(proposals_dict)
                # if id == "4":
                #     appointment_dict = {}
                #     no_of_appointment = Appointment.objects.filter(user=request.user, date_time=date_check)
                #     appointment_dict['appointments'] = len(no_of_appointment)
                #     appointment_dict['date'] = date_check.strftime("%Y-%m-%d")
                #     final_list.append(appointment_dict)
            final_dates = []
            for date_str in dates:
                final_dates.append(date_str.strftime("%Y-%m-%d"))
            context["dates"] = json.dumps(final_dates)
            context['json_list'] = json.dumps(final_list)
            context["id"] = str(id)
            return render(request, 'overview_line_chart.html', context)
        else:
            return render(request, 'overview.html', context)


class AppointmentScheduler(View):
    template_name = "appointment_scheduler.html"

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)

    def post(self, request):
        context = {}
        return render(request, self.template_name, context)


def upload_details(request):
    if request.method == 'GET':
        type = request.GET.get('type')
        if type == '1':
            user = request.user
            design_number = request.GET.get('number')
            design = Design.objects.filter(design_number=design_number)
            data = {'design_name': design[0].design_name, 'design_type': design[0].design_type}
            form = DesignUploadsForm(initial=data)
            return render(request, 'edit_form.html', {'form': form, 'type': type, 'user': user, 'design': design})
        if type == '2':
            user = request.user
            project_number = request.GET.get('number')
            project = Project.objects.filter(project_number=project_number)
            data = {'project_name': project[0].project_name, 'project_type': project[0].project_type}
            form = ProjectUploadsForm(initial=data)
            return render(request, 'edit_form.html', {'form': form, 'type': type, 'user': user, 'project': project})
    if request.method == 'POST':
        type = request.POST.get('type')
        if type == '1':
            user = request.user
            design_number = request.POST.get('design_number')
            form = DesignUploadsForm(request.POST, request.FILES)
            files = request.FILES.getlist('design_images')
            if form.is_valid():
                obj = form.save(commit=False)
                for f in files:
                    Design.objects.create(user=request.user, design_type=form.cleaned_data['design_type'],
                                          design_name=form.cleaned_data['design_name'], design_images=f,
                                          design_number=design_number)
                return render(request, 'designUploading.html', {'form': form, 'type': type, 'user': user})
            else:
                return render(request, 'edit_form.html', {'form': form, 'type': type, 'user': user})
        if type == '2':
            user = request.user
            project_number = request.POST.get('project_number')
            form = ProjectUploadsForm(request.POST, request.FILES)
            files = request.FILES.getlist('project_images')
            if form.is_valid():
                obj = form.save(commit=False)
                for f in files:
                    Project.objects.create(user=request.user, project_type=form.cleaned_data['project_type'],
                                           project_name=form.cleaned_data['project_name'], project_images=f,
                                           project_number=project_number)
                return render(request, 'designUploading.html', {'form': form, 'type': type, 'user': user})
            else:
                return render(request, 'edit_form.html', {'form': form, 'type': type, 'user': user})
    else:
        return render(request, 'designUploading.html', {})


def delete_design(request):
    number = request.GET.get('number')
    type = request.GET.get('type')
    if type == '1':
        Design.objects.filter(user=request.user, design_number=number).delete()
    elif type == '2':
        Project.objects.filter(user=request.user, project_number=number).delete()
    return redirect('/client/design_upload')


def load_upload_form(request):
    detail = request.GET.get('detail')
    user = request.user
    if detail:
        if detail == 'design':
            if request.method == 'GET':
                type = 1
                form = DesignUploadsForm()
                designs = Design.objects.filter(user_id=request.user.id)
                total_user_designs = []
                numbers = []
                for number in designs:
                    numbers.append(number.design_number)
                numbers = list(set(numbers))
                for design in designs:
                    for number in numbers:
                        if int(number) == int(design.design_number):
                            particular_design = Design.objects.filter(user_id=request.user.id, design_number=number)
                            total_user_designs.append(particular_design)
                            numbers.remove(number)
                return render(request, 'upload_form.html',
                              {'form': form, 'type': type, 'user': user,
                               'total_user_designs': list(total_user_designs)})
        elif detail == 'project':
            if request.method == 'GET':
                type = 2
                form = ProjectUploadsForm()
                projects = Project.objects.filter(user_id=request.user.id)
                total_user_projects = []
                numbers = []
                for number in projects:
                    numbers.append(number.project_number)
                numbers = list(set(numbers))
                for project in projects:
                    for number in numbers:
                        if int(number) == int(project.project_number):
                            particular_project = Project.objects.filter(user_id=request.user.id, project_number=number)
                            total_user_projects.append(particular_project)
                            numbers.remove(number)
                return render(request, 'upload_form.html',
                              {'form': form, 'type': type, 'user': user, 'total_user_projects': total_user_projects})
        else:
            error = 1
            return render(request, 'designUploading.html', {'error': error, 'user': user})
    else:
        error = 1
        return render(request, 'designUploading.html', {'error': error, 'user': user})


def design_upload(request):
    user = request.user
    form = DesignUploadsForm()
    type = 1
    if request.method == 'POST':
        type = 1
        form = DesignUploadsForm(request.POST, request.FILES)
        files = request.FILES.getlist('design_images')
        if form.is_valid():
            obj = form.save(commit=False)
            designs = list(Design.objects.all().values('design_number'))
            if designs:
                design_numbers = []
                for design in designs:
                    design_numbers.append(int(design['design_number']))
                design_number = max(set(design_numbers)) + 1
            else:
                design_number = 1
            for f in files:
                Design.objects.create(user=request.user, design_type=form.cleaned_data['design_type'],
                                      design_name=form.cleaned_data['design_name'], design_images=f,
                                      design_number=design_number)
            return render(request, 'designUploading.html', {'form': form, 'type': type, 'user': user})
        else:
            return render(request, 'upload_form.html', {'form': form, 'type': type, 'user': user})
    return render(request, 'designUploading.html', {'form': form, 'type': type, 'user': user})


def project_upload(request):
    user = request.user
    form = ProjectUploadsForm()
    type = 2
    if request.method == 'POST':
        type = 2
        form = ProjectUploadsForm(request.POST, request.FILES)
        files = request.FILES.getlist('project_images')
        if form.is_valid():
            obj = form.save(commit=False)
            projects = list(Project.objects.all().values('project_number'))
            if projects:
                project_numbers = []
                for project in projects:
                    project_numbers.append(int(project['project_number']))
                project_number = max(set(project_numbers)) + 1
            else:
                project_number = 1
            for f in files:
                Project.objects.create(user=request.user, project_type=form.cleaned_data['project_type'],
                                       project_name=form.cleaned_data['project_name'], project_images=f,
                                       project_number=project_number)
            return render(request, 'designUploading.html', {'form': form, 'type': type, 'user': user})
        else:
            return render(request, 'upload_form.html', {'form': form, 'type': type, 'user': user})
    return render(request, 'designUploading.html', {'form': form, 'type': type, 'user': user})


class PortfolioView(View):
    template_name = "profileSeting.html"

    def get(self, request):

        user = request.user
        data = {'id': user.id, 'userName': user.first_name + ' ' + user.last_name, 'gender': user.portfolio.gender,
                'experience': user.portfolio.experience, 'qualification': user.portfolio.qualification,
                'about_me': user.portfolio.about_me, 'prefix': user.portfolio.prefix,
                'budget': user.portfolio.budget, 'category': user.portfolio.category,
                'profile_pic': user.portfolio.profile_pic,
                'sub_category': user.portfolio.sub_category, 'secondary_phone': user.portfolio.secondary_phone}
        form = PortfolioForm(initial=data)
        return render(request, self.template_name, {'form': form, 'user': user})

    def post(self, request):

        form = PortfolioForm(request.POST, request.FILES)
        user = request.user
        if form.is_valid():
            user_details = User.objects.get(id=request.user.id)
            if request.POST.get('userName'):
                username = request.POST.get('userName').split(' ')
                user_details.first_name = username[0]
                username.pop(0)
                if username:
                    user_details.last_name = " ".join(username)
                user_details.save()
            if form.cleaned_data['profile_pic']:
                user_details.portfolio.profile_pic = form.cleaned_data['profile_pic']
            user_details.portfolio.budget = form.cleaned_data['budget']
            user_details.portfolio.gender = form.cleaned_data['gender']
            user_details.portfolio.experience = form.cleaned_data['experience']
            user_details.portfolio.qualification = form.cleaned_data['qualification']
            user_details.portfolio.about_me = form.cleaned_data['about_me']
            user_details.portfolio.category = form.cleaned_data['category']
            user_details.portfolio.sub_category = form.cleaned_data['sub_category']
            user_details.portfolio.prefix = form.cleaned_data['prefix']
            user_details.portfolio.secondary_phone = form.cleaned_data['secondary_phone']
            user_details.save()
            user = request.user
            data = {'id': user.id, 'userName': user.first_name + ' ' + user.last_name, 'gender': user.portfolio.gender,
                    'experience': user.portfolio.experience, 'qualification': user.portfolio.qualification,
                    'about_me': user.portfolio.about_me, 'prefix': user.portfolio.prefix,
                    'budget': user.portfolio.budget, 'category': user.portfolio.category,
                    'profile_pic': user.portfolio.profile_pic,
                    'sub_category': user.portfolio.sub_category, 'secondary_phone': user.portfolio.secondary_phone}
            form = PortfolioForm(initial=data)

        return render(request, self.template_name, {'form': form, 'user': user})


def load_sub_category(request):
    category_id = request.GET.get('category')
    sub_categories = sub_category.objects.filter(category_id=category_id).order_by('name')
    return render(request, 'sub_categories.html', {'sub_categories': sub_categories})
