import random
from django.shortcuts import render, get_object_or_404, redirect
from comments.models import Comment
from .models import News
from main.models import Main
from django.core.files.storage import FileSystemStorage
from datetime import datetime, timedelta
from category.models import Category
from subcategory.models import SubCategory
from trending.models import Trending
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from itertools import chain

mysearch = ""


def news_detail(request, word):
    site = Main.objects.get(pk=2)
    direct_news = News.objects.get(name=word)
    news = News.objects.all().order_by('-pk')
    categories = Category.objects.all()
    sub_category = SubCategory.objects.all()
    trending = Trending.objects.all().order_by('-pk')[:5]

    lastnews = News.objects.filter(act=1).order_by('-pk')[:3]
    popnews = News.objects.all().order_by('-show')
    popnews2 = News.objects.all().order_by('-show')[:3]

    tagname = News.objects.get(name=word).tag
    tag = tagname.split(',')

    my_news = News.objects.get(name=word)
    my_news.show += 1
    my_news.save()

    code = News.objects.get(name=word).pk
    comments = Comment.objects.filter(news_id=code, status=1).order_by("-pk")

    link = f"/urls/{News.objects.get(name=word).rand}"

    return render(request, 'front/news_detail.html',
                  {'directnews': direct_news, 'site': site, 'news': news, 'categories': categories,
                   'subcategories': sub_category, 'lastnews': lastnews, 'popnews': popnews, 'popnews2': popnews2,
                   'tag': tag, 'trending': trending, 'code': code, 'comments': comments, 'link': link,
                   })


def news_list(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('login')
    # login check end
    if request.user.groups.filter(name="masteruser"):
        data = News.objects.all()
        paginator = Paginator(data, 3)
        page = request.GET.get('page')

        try:
            data = paginator.page(page)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)
        except PageNotAnInteger:
            data = paginator.page(1)
    else:
        data = News.objects.filter(writer=request.user)

    return render(request, 'back/news_list.html', {'data': data})


def news_add(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('login')
    # login check end
    categories = SubCategory.objects.all()
    date = str(datetime.now().year) + str(datetime.now().month) + str(datetime.now().day)
    randint = str(random.randint(1000, 9999))
    rand = int(date + randint)

    if request.method == "POST":
        news_title = request.POST.get('newstitle')
        news_txt_short = request.POST.get('newstxtshort')
        news_txt = request.POST.get('newstxt')
        news_date = datetime.now().strftime("%Y/%m/%d | %H:%M:%S")
        news_cat_id = request.POST.get('newscat')
        news_tag = request.POST.get('tag')

        if news_title == "" or news_txt_short == "" or news_txt == "" or news_cat_id == "":
            error = "All fields required"
            return render(request, 'back/news_add.html', {'error': error, 'categories': categories})

        try:
            my_file = request.FILES['newsimg']
            fs = FileSystemStorage()
            filename = fs.save(my_file.name, my_file)
            url = fs.url(filename)

            if str(my_file.content_type).startswith("image"):

                if my_file.size < 5000000:

                    cat_news_name = SubCategory.objects.get(pk=news_cat_id).name
                    ocatid = SubCategory.objects.get(pk=news_cat_id).catid

                    new_news = News(name=news_title, short_txt=news_txt_short, body_txt=news_txt, catname=cat_news_name,
                                    catid=news_cat_id,
                                    date=news_date, writer=request.user,
                                    picurl=url, picname=filename,
                                    ocatid=ocatid, act=0, tag=news_tag, rand=rand)
                    new_news.save()

                    count = len(News.objects.filter(ocatid=ocatid))
                    cat_count = Category.objects.get(pk=ocatid)
                    cat_count.count = count
                    cat_count.save()

                    return redirect('news_list')
                else:

                    fs = FileSystemStorage()
                    fs.delete(filename)

                    error = "Your file is bigger then 5 Mb"
                    return render(request, 'back/news_add.html', {'error': error, 'categories': categories})
            else:

                fs = FileSystemStorage()
                fs.delete(filename)

                error = "Your file is not supported"
                return render(request, 'back/news_add.html', {'error': error, 'categories': categories})
        except:
            error = "Input your image"
            return render(request, 'back/news_add.html', {'error': error, 'categories': categories})

    return render(request, 'back/news_add.html', {'categories': categories})


def news_delete(request, pk):
    # login check start
    if not request.user.is_authenticated:
        return redirect('login')
    # login check end
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser":
            perm = 1
        else:
            writer = News.objects.get(pk=pk).writer
            if str(writer) != str(request.user):
                error = "Access denied"
                return render(request, 'back/error.html', {'error': error})

    try:
        news_to_delete = News.objects.get(pk=pk)

        fs = FileSystemStorage()
        fs.delete(news_to_delete.picname)

        ocatid = News.objects.get(pk=pk).ocatid

        news_to_delete.delete()

        count = len(News.objects.filter(ocatid=ocatid))
        cat_count = Category.objects.get(pk=ocatid)
        cat_count.count = count
        cat_count.save()

    except:
        return redirect('news_list')

    return redirect('news_list')


def news_edit(request, pk):
    # login check start
    if not request.user.is_authenticated:
        return redirect('login')
    # login check end
    if len(News.objects.filter(pk=pk)) == 0:
        return redirect('news_list')

    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser":
            perm = 1
        else:
            writer = News.objects.get(pk=pk).writer
            if str(writer) != str(request.user):
                error = "Access denied"
                return render(request, 'back/error.html', {'error': error})

    news = News.objects.get(pk=pk)
    category = SubCategory.objects.all()

    if request.method == "POST":
        news_title = request.POST.get('newstitle')
        news_txt_short = request.POST.get('newstxtshort')
        news_txt = request.POST.get('newstxt')
        news_cat_id = request.POST.get('newscat')
        news_tag = request.POST.get('tag')

        if news_title == "" or news_txt_short == "" or news_txt == "" or news_cat_id == "":
            error = "All fields required"
            return render(request, 'back/news_add.html', {'error': error, 'categories': category})

        try:
            my_file = request.FILES['newsimg']
            fs = FileSystemStorage()
            filename = fs.save(my_file.name, my_file)
            url = fs.url(filename)

            if str(my_file.content_type).startswith("image"):

                if my_file.size < 5000000:

                    newsname = SubCategory.objects.get(pk=news_cat_id).name

                    news_to_edit = News.objects.get(pk=pk)

                    fss = FileSystemStorage()
                    fss.delete(news_to_edit.picname)

                    news_to_edit.name = news_title
                    news_to_edit.short_txt = news_txt_short
                    news_to_edit.body_txt = news_txt
                    news_to_edit.picname = filename
                    news_to_edit.picurl = url
                    news_to_edit.writer = '-'
                    news_to_edit.catname = newsname
                    news_to_edit.catid = news_cat_id
                    news_to_edit.tag = news_tag
                    news_to_edit.act = 0

                    news_to_edit.save()

                    return redirect('news_list')
                else:

                    fs = FileSystemStorage()
                    fs.delete(filename)

                    error = "Your file is bigger then 5 Mb"
                    return render(request, 'back/news_add.html', {'error': error, 'categories': category})
            else:

                fs = FileSystemStorage()
                fs.delete(filename)

                error = "Your file is not supported"
                return render(request, 'back/news_add.html', {'error': error, 'categories': category})

        except:
            newsname = SubCategory.objects.get(pk=news_cat_id).name

            news_to_edit = News.objects.get(pk=pk)

            news_to_edit.name = news_title
            news_to_edit.short_txt = news_txt_short
            news_to_edit.body_txt = news_txt
            news_to_edit.writer = '-'
            news_to_edit.catname = newsname
            news_to_edit.catid = news_cat_id
            news_to_edit.tag = news_tag
            news_to_edit.act = 0

            news_to_edit.save()
            return redirect('news_list')

    return render(request, 'back/news_edit.html', {'pk': pk, 'news': news, 'categories': category})


def news_publish(request, pk):
    # login check start
    if not request.user.is_authenticated:
        return redirect('login')
    # login check end
    news_to_publish = News.objects.get(pk=pk)
    news_to_publish.act = 1
    news_to_publish.save()
    catid = news_to_publish.ocatid
    count = News.objects.filter(ocatid=catid, act=1).count()
    category = Category.objects.get(pk=catid)
    category.count = count
    category.save()
    return redirect('news_list')


def news_unpublish(request, pk):
    # login check start
    if not request.user.is_authenticated:
        return redirect('login')
    # login check end
    news_to_unpublish = News.objects.get(pk=pk)
    news_to_unpublish.act = 0
    news_to_unpublish.save()
    catid = news_to_unpublish.ocatid
    count = News.objects.filter(ocatid=catid, act=1).count()
    category = Category.objects.get(pk=catid)
    category.count = count
    category.save()
    return redirect('news_list')


def news_detail_short(request, pk):
    # login check start
    if not request.user.is_authenticated:
        return redirect('login')
    # login check end
    site = Main.objects.get(pk=2)
    direct_news = News.objects.filter(rand=pk)
    news = News.objects.all().order_by('-pk')
    categories = Category.objects.all()
    sub_category = SubCategory.objects.all()
    trending = Trending.objects.all().order_by('-pk')[:5]

    lastnews = News.objects.filter(act=1).order_by('-pk')[:3]
    popnews = News.objects.all().order_by('-show')
    popnews2 = News.objects.all().order_by('-show')[:3]

    tagname = News.objects.get(rand=pk).tag
    tag = tagname.split(',')

    my_news = News.objects.get(rand=pk)
    my_news.show += 1
    my_news.save()

    return render(request, 'front/news_detail.html',
                  {'directnews': direct_news, 'site': site, 'news': news, 'categories': categories,
                   'subcategories': sub_category, 'lastnews': lastnews, 'popnews': popnews, 'popnews2': popnews2,
                   'tag': tag, 'trending': trending
                   })


def news_all_show(request, word):
    catid = Category.objects.get(name=word).pk
    allnews = News.objects.filter(act=1, ocatid=catid)

    site = Main.objects.get(pk=2)
    news = News.objects.filter(act=1).order_by('-pk')
    categories = Category.objects.all()
    sub_category = SubCategory.objects.all()
    popnews = News.objects.filter(act=1).order_by('-show')
    popnews2 = News.objects.filter(act=1).order_by('-show')[:3]
    trending = Trending.objects.all().order_by('-pk')[:5]
    lastnews2 = News.objects.filter(act=1).order_by('-pk')[:4]

    return render(request, "front/all_news.html",
                  {'site': site, 'allnews': allnews, 'news': news, 'categories': categories,
                   'subcategories': sub_category, 'popnews': popnews, 'popnews2': popnews2, 'trending': trending,
                   'lastnews2': lastnews2})


def all_news(request):
    all_news = News.objects.all()

    site = Main.objects.get(pk=2)
    news = News.objects.filter(act=1).order_by('-pk')
    categories = Category.objects.all()
    sub_category = SubCategory.objects.all()
    popnews = News.objects.filter(act=1).order_by('-show')
    popnews2 = News.objects.filter(act=1).order_by('-show')[:3]
    trending = Trending.objects.all().order_by('-pk')[:5]
    lastnews2 = News.objects.filter(act=1).order_by('-pk')[:4]

    paginator = Paginator(all_news, 3)
    page = request.GET.get('page')

    try:
        all_news = paginator.page(page)
    except EmptyPage:
        all_news = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        all_news = paginator.page(1)

    return render(request, "front/all_news.html",
                  {'site': site, 'allnews': all_news, 'news': news, 'categories': categories,
                   'subcategories': sub_category, 'popnews': popnews, 'popnews2': popnews2, 'trending': trending,
                   'lastnews2': lastnews2})


def all_news_search(request):
    global mysearch
    if request.method == "POST":

        txt = request.POST.get("txt")
        catid = request.POST.get("category")
        mysearch = txt
        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")
        if from_date <= to_date:
            all_news = News.objects.filter(name__contains=txt, ocatid=catid, date__gte=from_date, date__lte=to_date)

        if catid == "0":
            all_news = News.objects.filter(name__contains=txt)
        else:
            all_news = News.objects.filter(name__contains=txt, ocatid=catid)
    else:
        all_news = News.objects.filter(name__contains=mysearch)

    site = Main.objects.get(pk=2)
    news = News.objects.filter(act=1).order_by('-pk')
    categories = Category.objects.all()
    sub_category = SubCategory.objects.all()
    popnews = News.objects.filter(act=1).order_by('-show')
    popnews2 = News.objects.filter(act=1).order_by('-show')[:3]
    trending = Trending.objects.all().order_by('-pk')[:5]
    lastnews2 = News.objects.filter(act=1).order_by('-pk')[:4]

    paginator = Paginator(all_news, 3)
    page = request.GET.get('page')
    try:
        all_news = paginator.page(page)
    except EmptyPage:
        all_news = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        all_news = paginator.page(1)

    return render(request, "front/all_news_2.html",
                  {'site': site, 'allnews': all_news, 'news': news, 'categories': categories,
                   'subcategories': sub_category, 'popnews': popnews, 'popnews2': popnews2, 'trending': trending,
                   'lastnews2': lastnews2})
