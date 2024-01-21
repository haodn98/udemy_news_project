from django.shortcuts import render, redirect

from blacklist.models import Blacklist
import re


# Create your views here.

def blacklist(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('login')
    # login check end
    blocked_ips = Blacklist.objects.all()
    return render(request, 'back/blacklist.html', {'blocked_ips': blocked_ips})

def blacklist_add(request):
    ip_to_add = request.POST["ip_to_block"]
    blocked_ips = Blacklist.objects.all()
    if not re.match(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', ip_to_add):
        error = "Wrong IP format"
        return render(request, 'back/blacklist.html', {'blocked_ips': blocked_ips,'error':error})
    ip_to_block = Blacklist(ip=ip_to_add)
    ip_to_block.save()
    return redirect("blacklist")

def blacklist_del(request, pk):
    # login check start
    if not request.user.is_authenticated:
        return redirect('login')
    # login check end
    ip_to_delete = Blacklist.objects.get(pk=pk)
    ip_to_delete.delete()
    return redirect("blacklist")
