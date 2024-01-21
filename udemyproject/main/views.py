import datetime
import json
import re

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from answers.models import Answer
from contactform.models import ContactForm
from newsletter.models import Newsletter
from .models import Main
from news.models import News
from category.models import Category
from subcategory.models import SubCategory
from trending.models import Trending
from manager.models import Manager
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User, Group, Permission
from datetime import datetime
from ipware import get_client_ip
from ip2geotools.databases.noncommercial import DbIpCity
from django.core.mail import send_mail
from django.conf import settings
from zeep import Client
import requests
from rest_framework import viewsets
from .serializer import NewsSerializer


def home(request):
    site = Main.objects.get(pk=2)
    news = News.objects.filter(act=1).order_by('-pk')
    categories = Category.objects.all()
    sub_category = SubCategory.objects.all()
    lastnews = News.objects.filter(act=1).order_by('-pk')[:3]
    popnews = News.objects.filter(act=1).order_by('-show')
    popnews2 = News.objects.filter(act=1).order_by('-show')[:3]
    trending = Trending.objects.all().order_by('-pk')[:5]
    lastnews2 = News.objects.filter(act=1).order_by('-pk')[:4]

    # Soup
    # client = Client("xxx.wsdl")
    # result = client.service.funcname(1,2,3)
    # print(result)

    # Curl
    # url = "xxxxx"
    # payload = {"a": "b", "c": "d"}
    # result = requests.post(url, params=payload)

    # Json
    # url = "xxxxxx"
    # data = {'a': "b", 'c': "d"}
    # headers = {'Content-Type': "application.json", "API_KEY": "xxxx"}
    # result = request.post(url, data=json.dumps(data), headers=headers)
    # print(result)

    return render(request, 'front/home.html',
                  {'site': site, 'news': news, 'categories': categories, 'subcategories': sub_category,
                   'lastnews': lastnews, 'popnews': popnews, 'popnews2': popnews2, 'trending': trending,
                   'lastnews2': lastnews2})


def about(request):
    news = News.objects.all().order_by('-pk')
    categories = Category.objects.all()
    sub_category = SubCategory.objects.all()
    popnews = News.objects.all().order_by('-show')[:3]
    trending = Trending.objects.all().order_by('-pk')[:5]

    site = Main.objects.get(pk=2)

    return render(request, 'front/about.html',
                  {'site': site, 'news': news, 'categories': categories, 'subcategories': sub_category,
                   'popnews2': popnews, 'trending': trending})


def panel(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('login')
    # login check end
    perm = 0
    perms = Permission.objects.filter(user=request.user)
    for i in perms:
        if i.codename == "master_user": perm = 1
    if perm == 0:
        error = "Access denied"
        return render(request, 'back/error.html', {'error': error})
    # # test = ['!', '@', '#']
    # # rand = ""
    # # for i in range(4):
    # #     rand += random.choice(string.ascii_letters)
    # #     rand += random.choice(test)
    # #     rand += str(random.randint(0, 9))
    #
    # rand = News.objects.all()[random.randint(0, News.objects.count() - 1)]

    return render(request, 'back/home.html')


def my_login(request):
    if request.method == 'POST':
        user_name = request.POST.get('username')
        user_password = request.POST.get('password')

        if user_name != "" and user_password != "":
            user = authenticate(username=user_name, password=user_password)
            if user != None:
                login(request, user)
                return redirect('panel')
    return render(request, 'front/login.html')


def my_registration(request):
    if request.method == 'POST':
        user_name = request.POST.get('name')
        user_username = request.POST.get('username')
        user_email = request.POST.get('email')
        user_password = request.POST.get('password')
        user_password_verify = request.POST.get('password-verify')

        if len(User.objects.filter(username=user_username)) or len(
                User.objects.filter(email=user_email)):
            error = "User or email already exists"
            return render(request, 'front/msgbox.html',
                          {'error': error, })

        if user_password != user_password_verify:
            error = "Password Verification Error"
            return render(request, 'front/msgbox.html',
                          {'error': error, })

        expression = r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z])(?=.*[\W]).{8,}$'
        if not re.match(expression, user_password):
            error = "New passwort is not strong enough. Use at least 8 characters, upper and lower case characters, at least 1 digit and 1 special symbol"
            return render(request, 'front/msgbox.html', {'error': error})

        ip = get_client_ip(request)[0]
        if ip is None:
            ip = "0.0.0.0"

        try:
            response = DbIpCity.get(ip, api_key="free")
            country = response.country + " " + response.city

        except:
            country = "Unknown"

        user = User.objects.create_user(username=user_username, email=user_email, password=user_password)
        user_add = Manager(name=user_name, utxt=user_username, email=user_email, ip=ip, country=country)
        user_add.save()
        success = "User was created"
        return render(request, 'front/msgbox.html', {'success': success})

    return render(request, 'front/login.html')


def my_logout(request):
    logout(request)

    return redirect('login')


def site_settings(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('login')
    # login check end

    site = Main.objects.get(pk=2)

    if request.method == "POST":
        name = request.POST.get('name')
        site_about = request.POST.get('about')
        tell = request.POST.get('tell')
        fb = request.POST.get('fb')
        tw = request.POST.get('tw')
        yt = request.POST.get('yt')
        link = request.POST.get('link')
        seo_txt = request.POST.get('seotxt')
        seo_key_words = request.POST.get('seokeywords')

        if fb == "": fb = "#"
        if tw == "": tw = "#"
        if yt == "": yt = "#"
        if link == "": link = "#"

        if not all([name, tell, site_about]):
            error = "All field required"
            return render(request, 'back/settings.html', {'error': error, 'site': site})
        try:
            my_file = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(my_file.name, my_file)
            url = fs.url(filename)
            picurl = url
            picname = filename

        except:
            picurl = "-"
            picname = "-"

        try:
            my_file2 = request.FILES['myfile2']
            fs2 = FileSystemStorage()
            filename2 = fs2.save(my_file2.name, my_file2)
            url2 = fs2.url(filename2)
            picurl2 = url2
            picname2 = filename2

        except:
            picurl2 = "-"
            picname2 = "-"

        site_to_edit = Main.objects.get(pk=2)
        site_to_edit.name = name
        site_to_edit.about = site_about
        site_to_edit.tell = tell
        site_to_edit.fb = fb
        site_to_edit.yt = yt
        site_to_edit.tw = tw
        site_to_edit.link = link
        site_to_edit.seo_txt = seo_txt
        site_to_edit.seo_key_words = seo_key_words
        if picurl != "-": site_to_edit.picurl = picurl
        if picname != "-": site_to_edit.picname = picname
        if picurl2 != "-": site_to_edit.picurl2 = picurl2
        if picname2 != "-": site_to_edit.picname2 = picname2

        site_to_edit.save()

        return redirect('panel')

    return render(request, 'back/settings.html', {'site': site})


def about_settings(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('login')
    # login check end
    about = Main.objects.get(pk=2).about
    short_about = Main.objects.get(pk=2).short_about
    if request.method == 'POST':
        txt = request.POST['about']
        short_txt = request.POST['short_about']
        if not all([txt, short_txt]):
            error = "All fields required"
            return render(request, 'back/about_settings.html',
                          {'error': error, 'about': about, 'short_about': short_about})
        site_to_edit = Main.objects.get(pk=2)
        site_to_edit.about = txt
        site_to_edit.short_about = short_txt
        site_to_edit.save()
        return redirect('panel')

    return render(request, 'back/about_settings.html', {'about': about, 'short_about': short_about})


def contact(request):
    news = News.objects.all().order_by('-pk')
    categories = Category.objects.all()
    sub_category = SubCategory.objects.all()
    popnews = News.objects.all().order_by('-show')[:3]
    trending = Trending.objects.all().order_by('-pk')[:5]

    site = Main.objects.get(pk=2)
    return render(request, 'front/contact.html',
                  {'site': site, 'news': news, 'categories': categories, 'subcategories': sub_category,
                   'popnews2': popnews, 'trending': trending})


def change_pass(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('login')
    # login check end
    if request.method == 'POST':
        oldpass = request.POST.get('oldpass')
        newpass = request.POST.get('newpass')

        if not all([oldpass, newpass]):
            error = "All fields required"
            return render(request, 'back/change_pass.html', {'error': error})

        user = authenticate(username=request.user, password=oldpass)

        if user != None:
            expression = r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z])(?=.*[\W]).{8,}$'
            if not re.match(expression, newpass):
                error = "New passwort is not strong enough. Use at least 8 characters, upper and lower case characters, at least 1 digit and 1 special symbol"
                return render(request, 'back/change_pass.html', {'error': error})
            user = User.objects.get(username=request.user)
            user.set_password(newpass)
            user.save()
            return redirect('logout')

        else:
            error = "Your passwort is not correct"
            return render(request, 'back/change_pass.html', {'error': error})

    return render(request, 'back/change_pass.html')


def contact_answer(request, pk):
    if request.method == "POST":
        txt = request.POST.get("answer")
        to_email = ContactForm.objects.get(pk=pk).email

        subject = "Answer form"
        message = txt
        email_from = settings.EMAIL_HOST_USER
        emails = [to_email, ]
        send_mail(subject, message, email_from, emails)

        answer_to_save = Answer(to_email=to_email, answer_txt=message,
                                date=datetime.now().strftime("%Y/%m/%d | %H:%M:%S"))
        answer_to_save.save()

    return render(request, 'back/answer_cm.html', {"pk": pk})


# def show_data(request):
#
#     count = Newsletter.objects.filter(status=1).count()
#     data = {"count": count}
#
#     return JsonResponse(data)


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
