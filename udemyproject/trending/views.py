from django.shortcuts import render, redirect
from .models import Trending
from news.models import News
from category.models import Category
from subcategory.models import SubCategory
from main.models import Main
from datetime import datetime


# Create your views here.
def trending_list(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('login')
    # login check end
    trending = Trending.objects.all()
    if request.method == 'POST':
        txt = request.POST.get('trending')
        if not txt:
            error = "All fields required"
            return render(request, 'back/trending_list.html', {'error': error, 'trending': trending})

        trending_to_add = Trending(txt=txt)
        trending_to_add.save()
        return redirect('trending_list')

    return render(request, 'back/trending_list.html', {'trending': trending})


def trending_del(request, pk):
    # login check start
    if not request.user.is_authenticated:
        return redirect('login')
    # login check end
    trending_to_del = Trending.objects.filter(pk=pk)
    trending_to_del.delete()
    return redirect('trending_list')


def trending_edit(request, pk):
    # login check start
    if not request.user.is_authenticated:
        return redirect('login')
    # login check end
    if len(Trending.objects.filter(pk=pk)) == 0:
        return redirect('trending_list')

    trending_to_edit = Trending.objects.get(pk=pk)
    if request.method == 'POST':
        txt = request.POST.get('trending')
        if not txt:
            error = "All fields required"
            return render(request, 'back/trending_list.html', {'error': error, 'trending': trending_to_edit})
        trending_to_edit.txt = txt
        trending_to_edit.save()
        return redirect('trending_list')

    return render(request, 'back/trending_list.html', {'trending': trending_to_edit})
