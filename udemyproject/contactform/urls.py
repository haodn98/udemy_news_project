from django.urls import path
from . import views

urlpatterns = [
    path('contact/submit/', views.feedback_get, name='contact_add'),
    path('panel/messages/', views.contact_show, name='messages'),
    path('panel/contact_del/<int:pk>/', views.contact_del, name='contact_del'),
    path('panel/check/checklist/', views.check_mychecklist, name='check_mychecklist'),

]
