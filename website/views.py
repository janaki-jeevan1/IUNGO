from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.apps import apps
from django.template.loader import render_to_string
from website.send_sms import sendSMS
from .forms import *
from django.http import JsonResponse
from rest_framework.generics import ListAPIView
# from .serializers import PortfolioSerializers
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from django.contrib.auth import authenticate, login
from django.template.context_processors import csrf
from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from random import randint
from django.db.models import Q
from django.core import serializers
from ClientDashboard.models import sub_category, Category, Portfolio, Design, Project
from django.template import loader, Context
import hashlib
import requests

global_otp = []


# Create your views here.
def Home(request):
    res = res = requests.get('https://ipinfo.io/')
    data = res.json()
    city = data['city']
    return render(request, 'index.html', {'city':city})


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
    # import pdb;pdb.set_trace()
    resp = sendSMS('efPEy+Qmmmw-mouME28qYH31Ep8X8hLtXyQjI0b4tL', '91' + number,
                   'TXTLCL', 'OTP to login ' + str(generate_otp))
    print(resp)
    global_otp.append(generate_otp)
    return HttpResponse('')


def clientcreation(request):
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            request.session['user'] = username
            return redirect('userauthentication')

    else:
        form = ClientRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


def userauthentication(request):
    if request.session.has_key('user'):
        username = request.session['user']
        user = User.objects.get(username=username)
        return render(request, 'user.html', {'user': user})
    return redirect('userpage')


def userpage(request):
    if request.method == 'POST':
        password = request.POST['password']
        if request.POST['mobile_phone']:
            mobile_phone = request.POST['mobile_phone']
            user = authenticate(username=mobile_phone, password=password)
        else:
            email = request.POST['email']
            mobile_phone = User.objects.get(email=email).mobile_phone
            user = authenticate(username=mobile_phone, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['user'] = user.username
                return redirect('userauthentication')
            messages.add_message(request, messages.INFO, 'User is Not Active.')
            return redirect('userpage')
        messages.add_message(request, messages.INFO, 'Please Check Your Login Credentials.')
        return redirect('userpage')

    else:
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})


def customercreation(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        password = request.POST['password']
        con_password = request.POST['con_password']
        data = Customer(phone_number=phone_number, email=email, password=password, con_password=con_password)
        data.save()
        return render(request, 'registration/login.html')
    return render(request, 'registration/register1.html')


def customerpage(request):
    global userobj
    res = requests.get('https://ipinfo.io/')
    data = res.json()
    city = data['city']
    phone_number = request.POST.get('phone_number', '')
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')
    otp = request.POST.get('otp', '')
    if phone_number and password:
        user = Customer(phone_number=phone_number, password=password)
        try:
            userobj = Customer.objects.get(phone_number=phone_number)
        except Customer.DoesNotExist:
            messages.error(request, 'Phone number does not exist, please register and try again.')
            return render(request, 'registration/register1.html')
    elif email and password:
        user = Customer(email=email, password=password)
        try:
            userobj = Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            messages.error(request, 'Email does not exist, Please register and try again.')
            return render(request, 'registration/register1.html')
    elif phone_number and email and password:
        user = Customer(phone_number=phone_number, password=password)
        try:
            userobj = Customer.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            messages.error(request, 'Phone number or email does not exist, please register and try again.')
            return render(request, 'registration/register1.html')
    elif phone_number and otp:
        # import pdb;pdb.set_trace()
        if otp == str(global_otp[0]):
            user = Customer(phone_number=phone_number)
            try:
                userobj = Customer.objects.get(phone_number=phone_number)
                # if userobj.is_active is True:
                #     global_otp.remove(global_otp[0])
                #     return redirect('')
            except Customer.DoesNotExist:
                messages.error(request, 'Phone number does not exist, please register and try again.')
                return render(request, 'registration/register1.html')
        else:
            messages.error(request, 'Invalid OTP')
            return render(request, 'registration/login.html')
    else:
        user = None
    if user is not None:

        return render(request, 'index1.html',{'city':city,'user':user})
    else:
        messages.error(request, 'Invalid Username or password')
        return redirect('customerpage')


def search(request):
    res = requests.get('https://ipinfo.io/')
    data = res.json()
    city = data['city']
    if request.method == 'GET':
        query = request.GET.get('q')
        location = request.GET.get('location')
        if query:
            users = Portfolio.objects.filter(Q(sub_category__name__icontains=query) |Q(category__name__icontains=query)).filter(location__icontains=location)

            if users:
                if request.is_ajax():
                    modern = request.GET.get('mordern')
                    traditional = request.GET.get('traditional')
                    bohemin = request.GET.get('bohemian')
                    budet_min = request.GET.get('budget[min]')
                    budget_max = request.GET.get('budget[max]')
                    style_list = []
                    if modern == 'true':
                        style_list.append('modern')
                    if traditional == 'true':
                        style_list.append('traditional')
                    if bohemin == 'true':
                        style_list.append('bohemian')
                    filtered_data = Portfolio.objects.filter(
                        Q(child_sub_category__name__in=style_list) & Q(budget__range=[budet_min, budget_max])).filter(
                                                 Q(sub_category__name__icontains=query) |
                                                 Q(category__name__icontains=query)).filter(location__icontains=location)
                    html = render_to_string(
                        template_name="filter_listingPage.html",
                        context={"users": filtered_data}
                    )
                    data_dict = {"html_from_view": html}

                    return JsonResponse(data=data_dict, safe=False)

                return render(request, 'searchlistpage.html', {'users': users, 'city':city})

            else:
                messages.error(request, 'no results found')

        else:
            users = Portfolio.objects.all().filter(location__icontains=location)
            if request.is_ajax():
                modern = request.GET.get('mordern')
                traditional = request.GET.get('traditional')
                bohemin = request.GET.get('bohemian')
                budet_min = request.GET.get('budget[min]')
                budget_max = request.GET.get('budget[max]')
                style_list = []
                if modern == 'true':
                    style_list.append('modern')
                if traditional == 'true':
                    style_list.append('traditional')
                if bohemin == 'true':
                    style_list.append('bohemian')
                filtered_data = Portfolio.objects.filter(
                    Q(child_sub_category__name__in=style_list) & Q(budget__range=[budet_min, budget_max])).filter(location__icontains=location)
                html = render_to_string(
                    template_name="filter_listingPage.html",
                    context={"users": filtered_data}
                )
                data_dict = {"html_from_view": html}

                return JsonResponse(data=data_dict, safe=False)
            return render(request, 'searchlist1.html', {'users': users, 'city':city})


def user_list(request, category_id, user_type):
    res = requests.get('https://ipinfo.io/')
    data = res.json()
    city = data['city']
    sub_categor = sub_category.objects.get(name=user_type, category=category_id)
    users = Portfolio.objects.filter(sub_category=sub_categor)

    if request.is_ajax():
        modern = request.GET.get('mordern')
        traditional = request.GET.get('traditional')
        bohemin = request.GET.get('bohemian')
        budet_min = request.GET.get('budget[min]')
        budget_max = request.GET.get('budget[max]')
        style_list = []
        if modern == 'true':
            style_list.append('modern')
        if traditional == 'true':
            style_list.append('traditional')
        if bohemin == 'true':
            style_list.append('bohemian')
        filtered_data = Portfolio.objects.filter(Q(child_sub_category__name__in=style_list) & Q(budget__range=[budet_min, budget_max]) & Q(category_id=category_id) & Q(sub_category__name=user_type))
        html = render_to_string(
            template_name="filter_listingPage.html",
            context={"users": filtered_data}
        )
        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)
    return render(request, 'listingPage.html', {'users': users , 'city':city})


def view_profile(request, user_id):
    user1 = Portfolio.objects.get(user_id=user_id)
    users = Project.objects.filter(user_id=user_id)
    project_list = list()
    for user in users:
        if int(user.project_number) not in project_list:
            project_list.append(int(user.project_number))
    project_images_list = list()
    for i in project_list:
        project_images = Project.objects.filter(user_id=user_id, project_number=i)
        project_images_list.append(list(project_images))

    users1 = Design.objects.filter(user_id=user_id)
    design_list = list()
    for user in users1:
        if int(user.design_number) not in design_list:
            design_list.append(int(user.design_number))
    design_images_list = list()
    for i in design_list:
        design_images = Design.objects.filter(user_id=user_id, design_number=i)
        design_images_list.append(list(design_images))

    return render(request, 'viewprofile.html', {'user': user1, 'users': project_images_list,'users1':design_images_list})


def enquiry(request,user_id):
   user=Portfolio.objects.get(user_id=user_id)
   return render(request,'enquiry.html',{'user':user})


def design_photos(request, user_id):
    #import pdb;pdb.set_trace()
    user1 = Design.objects.filter(user_id=user_id)
    design_list = list()
    for user in user1:
        if int(user.design_number) not in design_list:
            design_list.append(int(user.design_number))
    design_images_list = list()
    for i in design_list:
        design_images = Design.objects.filter(user_id=user_id, design_number=i)
        design_images_list.append(list(design_images))

    return render(request, "designphotos.html", {'users': design_images_list})


def filters(request,category_id,user_type):
    category_id = category_id
    sub_category_id = user_type
    modern=request.GET.get('mordern')
    traditional=request.GET.get('traditional')
    bohemin = request.GET.get('bohemian')
    budet_min = request.GET.get('budget[min]')
    budget_max = request.GET.get('budget[max]')
    style_list = []
    if modern == 'true':
        style_list.append('modern')
    if traditional == 'true':
        style_list.append('traditional')
    if bohemin == 'true':
        style_list.append('bohemian')
    filtered_data=Portfolio.objects.filter(Q(child_sub_category__name__in=style_list) & Q(budget__range=[budet_min, budget_max])&Q(category_id=category_id)&Q(sub_category__name=sub_category_id))
    qs_json = serializers.serialize('json', filtered_data)
    return render_to_response('listingPage.html',{'users':filtered_data})


def login_register(request):
    return render(request, 'registration/login.html')


def portfolio(request):

    if request.session.has_key('user'):
        if request.method == 'POST':
            user = request.session['user']
            user = User.objects.get(username=user)
            form = New_PortfolioForm(request.POST, request.FILES)
            if form.is_valid():
                user_portfolio = form.save(commit=False)
                user_portfolio.user = user
                user_portfolio.save()
                return HttpResponse('details saved successfully.')
            return HttpResponse('error')
        else:
            form = New_PortfolioForm()
            return render(request, 'portfolio.html', {'form': form})


def feedback(request):
    form = FeedbackForm()
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
        return redirect('view_profile')
    return render(request, 'viewprofile.html', {'form': form})


def getfeedback(request, user_id):
    feedback_list = FeedBack.objects.filter(user_id=user_id)
    return render(request, 'feedback.html', {'feedback': feedback_list})


def question(request):
    form = QuestionForm()
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
    return render(request, 'Q&A.html', {'form': form})


def answer(request):
    question_id = request.POST('question')
    customer_id = request.POST('customer')
    client_id = request.POST('client')
    answer = request.POST('answer')
    pub_date = request.POST('pub_date')
    Answers(question=question_id, customer=customer_id, client=client_id, answer=answer, pub_date=pub_date).save()
    messages.error(request, 'answer submitted successfully')
    return render(request, 'Q&A.html')


def reply_answer(request, user_id):
    ans = Answers.objects.filter(client_id=user_id)
    return render(request, "Q&A.html", {'ans': ans})
