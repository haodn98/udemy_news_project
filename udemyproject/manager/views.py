import re
from django.shortcuts import render, get_object_or_404, redirect
from .models import Manager
from main.models import Main
from news.models import News
from category.models import Category
from subcategory.models import SubCategory
from trending.models import Trending
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType


# Create your views here.
def manager_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    # login check end
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser": perm = 1
    if perm == 0:
        error = "Access denied"
        return render(request, 'back/error.html', {'error': error})

    users = Manager.objects.all().exclude(utxt="admin")

    return render(request, 'back/manager.html', {'users_list': users})


def manager_del(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    # login check end
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser": perm = 1
    if perm == 0:
        error = "Access denied"
        return render(request, 'back/error.html', {'error': error})

    users = Manager.objects.all()
    uname = Manager.objects.get(pk=pk).utxt
    user_to_del = User.objects.filter(username=uname)
    user_to_del.delete()
    return render(request, 'back/manager.html', {'users_list': users})


def manager_group(request):
    if not request.user.is_authenticated:
        return redirect('login')
    # login check end
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser": perm = 1
    if perm == 0:
        error = "Access denied"
        return render(request, 'back/error.html', {'error': error})

    groups = Group.objects.all().exclude(name="masteruser")

    return render(request, 'back/manager_group.html', {'groups': groups})


def manager_group_add(request):
    if not request.user.is_authenticated:
        return redirect('login')
    # login check end
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser": perm = 1
    if perm == 0:
        error = "Access denied"
        return render(request, 'back/error.html', {'error': error})
    groups = Group.objects.all()
    if request.method == 'POST':
        group_name = request.POST.get('group_add')
        if len(Group.objects.filter(name=group_name)):
            error = f"Group {group_name} already exists"
            return render(request, 'back/manager_group.html', {'error': error, 'groups': groups})

        if group_name == "":
            error = f"Required field"
            return render(request, 'back/manager_group.html', {'error': error, 'groups': groups})

        group_to_add = Group(name=group_name)
        group_to_add.save()
        return redirect('manager_group')

    return render(request, 'back/manager_group.html', {'groups': groups})


def manager_group_del(request, pk):
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

    group_to_del = Group.objects.filter(pk=pk)
    group_to_del.delete()
    return redirect('manager_group')


def user_groups(request, pk):
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

    groups = Group.objects.all()
    manager = Manager.objects.get(pk=pk)
    user = User.objects.get(username=manager.utxt)
    ugroups = []
    for i in user.groups.all():
        ugroups.append(i.name)
    return render(request, 'back/user_groups.html', {'ugroups': ugroups, 'groups': groups, 'pk': pk})


def add_users_to_groups(request, pk):
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

    if request.method == 'POST':
        gname = request.POST.get('gname')
        group = Group.objects.get(name=gname)
        manager = Manager.objects.get(pk=pk)
        user = User.objects.get(username=manager.utxt)
        user.groups.add(group)
        return redirect('user_groups', pk=pk)

    return redirect('user_groups', pk=pk)


def del_users_from_groups(request, pk, name):
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

    manager = Manager.objects.get(pk=pk)
    user = User.objects.get(username=manager.utxt)
    group = Group.objects.get(name=name)
    user.groups.remove(group)
    return redirect('user_groups', pk=pk)


def manager_permissions(request):
    if not request.user.is_authenticated:
        return redirect('login')
    # login check end

    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser": perm = 1

    if perm == 0:
        error = "Access denied"
        return render(request, 'back/error.html', {'error': error})

    perms = Permission.objects.all()

    return render(request, 'back/manager_permission.html', {'perms': perms})


def manager_perms_del(request, pk):
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

    perm_to_del = Permission.objects.filter(pk=pk)
    perm_to_del.delete()
    return redirect('manager_permissions')


def manager_perms_add(request):
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser": perm = 1
    if perm == 0:
        error = "Access denied"
        return render(request, 'back/error.html', {'error': error})
    perms = Permission.objects.all()
    if request.method == 'POST':
        name = request.POST.get("perm_add")
        cname = request.POST.get("perm_code_name")

        if len(Permission.objects.filter(codename=cname)) == 0:
            content_type = ContentType.objects.get(app_label='main', model='main')
            permission = Permission.objects.create(codename=cname, name=name, content_type=content_type)
        else:
            error = f"Permission {cname} already exists"
            return render(request, 'back/manager_permission.html', {'error': error, 'perms': perms})

    return redirect('manager_permissions')


def user_permissions(request, pk):
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

    perms = Permission.objects.all()
    manager = Manager.objects.get(pk=pk)
    user = User.objects.get(username=manager.utxt)
    permissions = Permission.objects.filter(user=user)
    uperms = []
    for i in permissions:
        uperms.append(i.name)

    return render(request, 'back/user_perms.html', {'uperms': uperms, 'perms': perms, 'pk': pk})


def del_users_perm(request, pk, name):
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

    manager = Manager.objects.get(pk=pk)
    user = User.objects.get(username=manager.utxt)
    perm = Permission.objects.get(name=name)
    user.user_permissions.remove(perm)
    return redirect('user_perms', pk=pk)


def add_perm_to_user(request, pk):
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

    if request.method == 'POST':
        pname = request.POST.get('pname')
        perm = Permission.objects.get(name=pname)
        manager = Manager.objects.get(pk=pk)
        user = User.objects.get(username=manager.utxt)
        user.user_permissions.add(perm)
        return redirect('user_perms', pk=pk)

    return redirect('user_perms', pk=pk)


def group_permissions(request, name):
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

    group = Group.objects.get(name=name)
    perms = group.permissions.all()
    all_perms = Permission.objects.all()
    return render(request, 'back/group_perms.html', {'perms': perms, 'name': name, 'all_perms': all_perms})


def group_permissions_add(request, name):
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
    if request.method == 'POST':
        pname = request.POST.get('pname')
        group = Group.objects.get(name=name)
        perm = Permission.objects.get(name=pname)
        group.permissions.add(perm)
    return redirect('group_perms', name=name)


def group_permissions_del(request, gname, name):
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
    group = Group.objects.get(name=gname)
    perm = Permission.objects.get(name=name)
    group.permissions.remove(perm)
    return redirect('group_perms', name=gname)
