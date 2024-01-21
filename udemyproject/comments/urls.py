from django.urls import path
from . import views

urlpatterns = [
    path('comment/add/<int:pk>', views.news_comment_add, name='comment_add'),
    path('panel/comment/list', views.comments_list, name='comments_list'),
    path('panel/comment/del/<int:pk>', views.comment_del, name='comment_del'),
    path('panel/comment/conform/<int:pk>', views.comment_confirm, name='comment_confirm'),
]
