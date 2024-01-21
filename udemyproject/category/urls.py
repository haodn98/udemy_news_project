from django.urls import path
from . import views

urlpatterns = [
    path('panel/category/list', views.category_list, name='category_list'),
    path('panel/category/add', views.category_add, name='category_add'),
    path('panel/category/del/<int:pk>', views.category_del, name='category_del'),
    path('export/category/csv', views.export_category_csv, name='export_category_csv'),
    path('import/category/csv', views.import_category_csv, name='import_category_csv'),
]
