from django.shortcuts import render, redirect

from manager.models import Manager
from .models import Comment
from news.models import News
import datetime


def news_comment_add(request, pk):
    if request.method == "POST":
        cm = request.POST.get('msg')

        if request.user.is_authenticated:
            manager = Manager.objects.get(utxt=request.user)
            comment = Comment(cm=cm, name=manager.name, email=manager.email, news_id=pk,
                              date=datetime.datetime.now().strftime("%Y/%m/%d | %H:%M:%S"))
            comment.save()
        else:
            name = request.POST.get('name')
            email = request.POST.get('email')
            comment = Comment(cm=cm, name=name, email=email, news_id=pk,
                              date=datetime.datetime.now().strftime("%Y/%m/%d | %H:%M:%S"))
            comment.save()
    news_name = News.objects.get(pk=pk).name
    return redirect('news_detail', word=news_name)


def comments_list(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('login')
    # login check end
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser": perm = 1
    if perm == 0:
        error = "Access denied"
        return render(request, 'back/error.html', {'error': error})

    all_comments = Comment.objects.all()
    return render(request, 'back/comment_list.html', {'comments': all_comments})

def comment_del(request,pk):
    # login check start
    if not request.user.is_authenticated:
        return redirect('login')
    # login check end
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser": perm = 1
    if perm == 0:
        error = "Access denied"
        return render(request, 'back/error.html', {'error': error})
    comment_to_del = Comment.objects.get(pk=pk)
    comment_to_del.delete()
    return redirect('comments_list')

def comment_confirm(request,pk):
    # login check start
    if not request.user.is_authenticated:
        return redirect('login')
    # login check end
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser": perm = 1
    if perm == 0:
        error = "Access denied"
        return render(request, 'back/error.html', {'error': error})
    comment_to_confirm = Comment.objects.get(pk=pk)
    comment_to_confirm.status=1
    comment_to_confirm.save()
    return redirect('comments_list')