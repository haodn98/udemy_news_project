import re

from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect

from django.conf import settings
from .models import Newsletter


def news_letter(request):
    if request.method == 'POST':
        txt = request.POST.get('txt')
        if txt.find("@") != -1:
            news_letter = Newsletter(txt=txt, status=1)
            news_letter.save()
        else:
            try:
                int(txt)
                news_letter = Newsletter(txt=txt, status=2)
                news_letter.save()
            except:
                return redirect('home')
    return redirect('home')


def news_emails(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('login')
    # login check end
    emails = Newsletter.objects.filter(status=1)
    return render(request, 'back/emails.html', {'emails': emails})


def news_phone_num(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('login')
    # login check end
    phones = Newsletter.objects.filter(status=2)
    return render(request, 'back/phone_numbers.html', {'phones': phones})


def news_letter_del(request, pk):
    # login check start
    if not request.user.is_authenticated:
        return redirect('login')
    # login check end
    news_letter_to_del = Newsletter.objects.get(pk=pk)
    news_letter_to_del.delete()
    if news_letter_to_del.status == 1:
        return redirect('news_email')
    return redirect('news_phones')


def send_email(request):
    if request.method == "POST":
        txt = request.POST.get("txt")
        emails_to_send = []
        for i in Newsletter.objects.filter(status=1):
            emails_to_send.append(i.txt)

        subject = "Answer form"
        message = txt
        email_from = settings.EMAIL_HOST_USER
        emails = emails_to_send
        send_mail(subject, message, email_from, emails)

    return redirect('news_email')
