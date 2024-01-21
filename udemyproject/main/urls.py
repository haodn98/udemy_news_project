from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('panel/', views.panel, name='panel'),
    path('login/', views.my_login, name='login'),
    path('logout/', views.my_logout, name='logout'),
    path('panel/settings/', views.site_settings, name='site_settings'),
    path('panel/about/settings/', views.about_settings, name='about_settings'),
    path('contact/', views.contact, name='contact'),
    path('panel/change/pass', views.change_pass, name='change_pass'),
    path('registration/', views.my_registration, name='registration'),
    path('panel/answer/<int:pk>/', views.contact_answer, name='contact_answer'),
    # path('show/data/', views.show_data, name='show_data'),
]
