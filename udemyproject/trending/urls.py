from django.urls import path
from . import views

urlpatterns = [
    path('panel/trending/list/', views.trending_list, name='trending_list'),
    path('panel/trending_del/<int:pk>/', views.trending_del, name='trending_del'),
    path('panel/trending/edit/<int:pk>/', views.trending_edit, name='trending_edit'),
]
