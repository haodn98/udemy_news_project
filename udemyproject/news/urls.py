from django.urls import path
from . import views

urlpatterns = [
    path('news/detail/<str:word>/', views.news_detail, name='news_detail'),
    path('panel/news/list/', views.news_list, name='news_list'),
    path('panel/news/add_news/', views.news_add, name='news_add'),
    path('panel/news/del/<int:pk>/', views.news_delete, name='news_delete'),
    path('panel/news/edit/<int:pk>/', views.news_edit, name='news_edit'),
    path('panel/news/publish/<int:pk>/', views.news_publish, name='news_publish'),
    path('panel/news/unpublish/<int:pk>/', views.news_unpublish, name='news_unpublish'),
    path('urls/<int:pk>/', views.news_detail_short, name='news_detail_short'),
    path('news/all/<str:word>/', views.news_all_show, name='news_all_show'),
    path('news/all/', views.all_news, name='all_news'),
    path('search/', views.all_news_search, name='all_news_search'),
]
