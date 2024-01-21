from django.shortcuts import render, redirect

from newsletter.models import Newsletter
from .models import ContactForm
from news.models import News
from category.models import Category
from subcategory.models import SubCategory
from main.models import Main
from datetime import datetime
from trending.models import Trending


# Create your views here.

def feedback_get(request):
    news = News.objects.all().order_by('-pk')
    categories = Category.objects.all()
    sub_category = SubCategory.objects.all()
    popnews = News.objects.all().order_by('-show')[:3]
    site = Main.objects.get(pk=2)
    date = datetime.now().strftime("%Y/%m/%d | %H:%M:%S")
    trending = Trending.objects.all().order_by('-pk')[:5]

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('msg')

        if not all([name, email, message]):
            error = "All fields required"
            return render(request, 'front/contact.html',
                          {'error': error, 'site': site, 'news': news, 'categories': categories,
                           'subcategories': sub_category,
                           'popnews2': popnews, 'trending': trending})

        feedback_to_get = ContactForm(name=name, email=email, message=message, date=date)
        feedback_to_get.save()

        success = "Thank you for your message"
        return render(request, 'front/msgbox.html',
                      {'success': success, 'site': site, 'news': news, 'categories': categories,
                       'subcategories': sub_category,
                       'popnews2': popnews, })
    return render(request, 'front/contact.html', {'site': site, 'news': news, 'categories': categories,
                                                  'subcategories': sub_category,
                                                  'popnews2': popnews, })


def contact_show(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('login')
    # login check end
    messages = ContactForm.objects.all()

    return render(request, 'back/contact_list.html', {'messages': messages})


def contact_del(request, pk):
    # login check start
    if not request.user.is_authenticated:
        return redirect('login')
    # login check end
    message_to_delete = ContactForm.objects.filter(pk=pk)
    message_to_delete.delete()
    return redirect('messages')


def check_mychecklist(request):

    if request.method == "POST":
        # emails = Newsletter.objects.filter(status=1)
        # for i in emails:
        #     x = request.POST.get(str(i.pk))
        #     if x == "on":
        #         email_to_del = Newsletter.objects.get(pk=i.pk)
        #         email_to_del.delete()
        check = request.POST.getlist("checks_array")
        for i in check:
            email = Newsletter.objects.get(pk=i)
            email.delete()

    return redirect('news_email')
