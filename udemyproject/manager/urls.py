from django.urls import path
from . import views

urlpatterns = [
    path('panel/manager/list', views.manager_list, name='manager_list'),
    path('panel/manager/del/<int:pk>/', views.manager_del, name='manager_del'),
    path('panel/manager/group/', views.manager_group, name='manager_group'),
    path('panel/manager/group/add/', views.manager_group_add, name='manager_group_add'),
    path('panel/manager/group/del/<int:pk>/', views.manager_group_del, name='manager_group_del'),
    path('panel/user/groups/<int:pk>/', views.user_groups, name='user_groups'),
    path('panel/manager/addtogroup/<int:pk>/', views.add_users_to_groups, name='add_user_to_group'),
    path('panel/manager/delfromgroup/<int:pk>/<str:name>/', views.del_users_from_groups, name='del_user_from_group'),
    path('panel/manager/permissions/', views.manager_permissions, name='manager_permissions'),
    path('panel/manager/permission/del/<int:pk>/', views.manager_perms_del, name='manager_permission_del'),
    path('panel/manager/permission/add/', views.manager_perms_add, name='manager_permission_add'),
    path('panel/user/permission/<int:pk>/', views.user_permissions, name='user_perms'),
    path('panel/manager/delperm/<int:pk>/<str:name>/', views.del_users_perm, name='del_users_perm'),
    path('panel/manager/addpermtouser/<int:pk>/', views.add_perm_to_user, name='add_perm_to_user'),
    path('panel/manager/addpermtogroup/<str:name>/', views.group_permissions, name='group_perms'),
    path('panel/manager/group/delpermfromgroup/<str:gname>/<str:name>/', views.group_permissions_del,
         name='group_perms_del'),
    path('panel/manager/group/addpermtogroup/<str:name>/', views.group_permissions_add,
         name='group_perms_add'),

]
