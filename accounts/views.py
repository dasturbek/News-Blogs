from django.shortcuts import redirect, render, get_object_or_404
from .forms import RegisterForm
from django.contrib import auth
from .decorators import authentication_not_required, authentication_required, author_req
from .models import AccountModel
from django.contrib.auth import authenticate
from news.models import NewsModel

# Create your views here.

@authentication_not_required
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.set_password(form.cleaned_data['password1'])
            instance.save()
            return redirect('sign_in')
        else:
            print('error creation')
    else:
        form = RegisterForm()
    return render(request, template_name='./accounts/signup.html')

@authentication_not_required
def user_login(request):
    if request.method == 'POST':
        user = auth.authenticate(request, username=request.POST.get('username'), 
        password=request.POST.get('password'))
        print(user)
        if user is not None:
            auth.login(request, user)
            print("Logged in Successfully!")
            return redirect("home")
        else:
            print("Invalid credentials, wrong username or password")
    return render(request, template_name='./accounts/signin.html') 

def logoutView(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect('home') 

@authentication_required
def personal_posts(request, username):
    three_article = NewsModel.objects.filter(status=3).order_by('-date_posted')[:3]
    person = get_object_or_404(AccountModel, username=username)
    return render(request=request, template_name='./accounts/personal_posts.html', context={'three_article':three_article, 'person':person})

@authentication_required
@author_req
def personal_articles(request, username):
    three_article = NewsModel.objects.filter(status=3).order_by('-date_posted')[:3]
    person = get_object_or_404(AccountModel, username=username)
    return render(request=request, template_name='./accounts/personal_articles.html', context={'three_article':three_article, 'person':person})

@authentication_required
def personal_settings(request):
    three_article = NewsModel.objects.filter(status=3).order_by('-date_posted')[:3]
    person = get_object_or_404(AccountModel, username=request.user.username)
    return render(request=request, template_name='./accounts/personal_settings.html' , context={'three_article':three_article, 'person':person})

@authentication_required
def personal_details(request, username):
    three_article = NewsModel.objects.filter(status=3).order_by('-date_posted')[:3]
    person = get_object_or_404(AccountModel, username=username)
    return render(request=request, template_name='./accounts/personal_details.html', context={'three_article':three_article, 'person':person})

# edit so'rovlar
@authentication_required
def details(request):
    three_article = NewsModel.objects.filter(status=3).order_by('-date_posted')[:3]
    person = get_object_or_404(AccountModel, username=request.user.username)
    if request.POST:
        person.last_name = request.POST.get('last_name')
        person.first_name = request.POST.get('first_name')
        if request.FILES.get('image') != None:
            person.image = request.FILES.get('image')
        person.username = request.POST.get('username')
        person.bio = request.POST.get('bio')
        person.job = request.POST.get('job')
        person.staj = request.POST.get('staj')
        person.save()
        return redirect(person.get_absolute_url())
    return render(request=request, template_name='./accounts/personal_settings.html' , context={'three_article':three_article, 'person':person})

@authentication_required
def phone_number(request):
    three_article = NewsModel.objects.filter(status=3).order_by('-date_posted')[:3]
    person = get_object_or_404(AccountModel, username=request.user.username)
    if request.POST:
        person.phone_number = request.POST.get('phone')
        if request.POST.get('phone'):
            person.save()
            return redirect(person.get_absolute_url())
        return redirect('settings_profile')
    return render(request=request, template_name='./accounts/personal_settings.html' , context={'three_article':three_article,'person':person})

@authentication_required
def change_password(request):
    person = get_object_or_404(AccountModel, username=request.user.username)
    if request.POST: 
        user = auth.authenticate(username=person.username, password=request.POST.get('password'))
        try:
            if user is not None:
                if str(request.POST.get('new_password1')) == str(request.POST.get('new_password2')):
                    # person.password = request.POST.get('new_password2')
                    person.set_password(request.POST.get('new_password2'))
                    person.save()
                    user = authenticate(username=person.username, password=request.POST.get('new_password2'))
                    auth.login(request, user)
                    return redirect(person.get_absolute_url())
            else: 
                return redirect('settings_profile')
        except:
            return redirect('settings_profile')
        
    return redirect('settings_profile')

@authentication_required
def change_email(request):
    three_article = NewsModel.objects.filter(status=3).order_by('-date_posted')[:3]
    person = get_object_or_404(AccountModel, username=request.user.username)
    if request.POST:
        if request.POST.get('email'):
            otp = OTP(request.POST.get('email'))
            code = otp.send_code_2()
            print(code)
            return redirect(person.get_absolute_url())
        return redirect('settings_profile')
    return render(request=request, template_name='./accounts/personal_settings.html' , context={'three_article':three_article, 'person':person})

import math
import random
import smtplib
from datetime import datetime
import urllib.request


def check_internet(host='https://google.com'):
    try:
        urllib.request.urlopen(host)  # Python 3.x
        return True
    except:
        return False


class OTP:
    send_email = str()

    def __init__(self, email):
        self.send_email = email

    def send_code(self):
        digits = "0123456789"
        one_time_password = ""
        for i in range(6):
            one_time_password += digits[math.floor(random.random() * 10)]
        msg = 'Your OTP Verification for app is ' + one_time_password + ' Note..  Please enter otp within 2 minutes ' \
                                                                        'and 3 attempts, ' \
                                                                        'otherwise it becomes invalid '

        my_email = "dasturbek.com@gmail.com"
        password = "shogofyzxfrbxfmb"
        if check_internet():
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.ehlo()
            s.starttls()
            s.login(my_email, password)
            s.sendmail(my_email, self.send_email, msg)

            return one_time_password
        else:
            return "no internet"

    def send_code_2(self):
        digits = "0123456789"
        one_time_password = ""
        now_time = datetime.now()
        hour = now_time.hour
        minute = now_time.minute
        second = now_time.second

        for i in range(6):
            one_time_password += digits[math.floor(random.random() * 10)]
        k = int(one_time_password) + hour + minute + second
        one_time_password = str(k)
        msg = 'Your OTP Verification for app is ' + one_time_password + ' Note..  Please enter otp within 2 minutes ' \
                                                                        'and 3 attempts, ' \
                                                                        'otherwise it becomes invalid '

        my_email = "dasturbek.com@gmail.com"
        password = "shogofyzxfrbxfmb"
        if check_internet():
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.ehlo()
            s.starttls()
            s.login(my_email, password)
            s.sendmail(my_email, self.send_email, msg)

            return one_time_password
        else:
            return "no internet"

