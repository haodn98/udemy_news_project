from django.shortcuts import render, redirect
from .models import Category
import csv
from django.http import HttpResponse


# Create your views here.

def category_list(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('login')
    # login check end
    data = Category.objects.all
    return render(request, 'back/category_list.html', {'data': data})


def category_add(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('login')
    # login check end
    if request.method == 'POST':
        name = request.POST.get('categoryname')
        if name == "":
            error = "All fields required"
            return render(request, 'back/category_add.html', {'error': error})

        if len(Category.objects.filter(name=name)) != 0:
            error = "Category already exist"
            return render(request, 'back/category_add.html', {'error': error})

        category_to_add = Category(name=name)
        category_to_add.save()
        return redirect('category_list')

    return render(request, 'back/category_add.html')


def category_del(request, pk):
    # login check start
    if not request.user.is_authenticated:
        return redirect('login')
    # login check end
    category_to_del = Category.objects.get(pk=pk)
    category_to_del.delete()
    return redirect('category_list')


def export_category_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="cat.csv"'
    writer = csv.writer(response)
    writer.writerow(["Title", "Counter"])
    for i in Category.objects.all():
        writer.writerow([i.name, i.count])
    return response


def import_category_csv(request):
    categories = Category.objects.all()
    if request.method == "POST":
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            error = "Please Input CSV file"
            return render(request, 'back/category_list.html', {'error': error, 'data': categories})

        if csv_file.multiple_chunks():
            error = "File too large"
            return render(request, 'back/category_list.html', {'error': error, 'data': categories})

        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")
        for line in lines:
            fields = line.split(",")
            try:
                if len(Category.objects.filter(name=fields[0])) == 0 and (fields[0] != "Title" and fields[0]):
                    new_category = Category(name=fields[0])
                    new_category.save()
                    print(fields[0], fields[1])
            except:
                print("finish")

    return redirect('category_list')
