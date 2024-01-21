from django.shortcuts import render, redirect
from .models import SubCategory
from category.models import Category
from django.core.files.storage import FileSystemStorage


# Create your views here.

def subcategory_list(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('login')
    # login check end
    data = SubCategory.objects.all()
    return render(request, 'back/subcategory_list.html', {'data': data})


def subcategory_add(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('login')
    # login check end
    categories = Category.objects.all()
    if request.method == 'POST':
        name = request.POST.get('subcategoryname')
        catid = request.POST.get('category')

        if name == "":
            error = "All fields required"
            return render(request, 'back/subcategory_add.html', {'error': error})

        if len(SubCategory.objects.filter(name=name)) != 0:
            error = "Subcategory already exist"
            return render(request, 'back/subcategory_add.html', {'error': error,'categories':categories})

        category = Category.objects.get(pk=catid).name

        subcategory_to_add = SubCategory(name=name, catname=category, catid=catid)
        subcategory_to_add.save()
        return redirect('subcategory_list')

    return render(request, 'back/subcategory_add.html', {'categories': categories})


def subcategory_delete(request, pk):
    # login check start
    if not request.user.is_authenticated:
        return redirect('login')
    # login check end
    try:
        subcategory_to_delete = SubCategory.objects.get(pk=pk)
        subcategory_to_delete.delete()

    except:

        return redirect('subcategory_list')

    return redirect('subcategory_list')
