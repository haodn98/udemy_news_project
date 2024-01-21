from django.urls import path
from . import views

urlpatterns = [
    path('newsletter/add', views.news_letter, name='news_letter'),
    path('panel/newsletter/emails', views.news_emails, name='news_email'),
    path('panel/newsletter/phones', views.news_phone_num, name='news_phones'),
    path('panel/newsletter/del/<int:pk>', views.news_letter_del, name='news_letter_to_del'),
    path('send/email', views.send_email, name='send_email'),
]
