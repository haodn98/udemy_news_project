from django.urls import path
from . import views

urlpatterns = [
    path('panel/blacklist', views.blacklist, name='blacklist'),
    path('panel/blacklist/add', views.blacklist_add, name='blacklist_add'),
    path('panel/blacklist/del/<int:pk>', views.blacklist_del, name='blacklist_del'),
]
