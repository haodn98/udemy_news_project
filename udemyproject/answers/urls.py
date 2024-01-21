from django.urls import path
from . import views

urlpatterns = [
    path("panel/answers/list", views.answers_list, name='answers_list'),
    path("panel/answers/del/<int:pk>", views.answer_del, name='answer_del'),
]
