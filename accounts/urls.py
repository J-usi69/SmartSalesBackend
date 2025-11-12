from django.urls import path
from . import views

urlpatterns = [
    # Usuarios
    path('users/', views.list_users, name='list_users'),
    # path('users/<int:user_id>/', views.get_user, name='get_user'),
    path('users/create/', views.create_user, name='create_user'),
    path('users/update/<int:user_id>/', views.update_user, name='update_user'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('users/save-fcm-token/', views.guardar_fcm_token),
    

    # Roles
    path('roles/', views.list_roles, name='list_roles'),
    path('roles/create/', views.create_role, name='create_role'),
    path('roles/update/<int:role_id>/', views.update_role, name='update_role'),
    path('roles/delete/<int:role_id>/', views.delete_role, name='delete_role'),

    # Permisos
    path('permissions/', views.list_permissions, name='list_permissions'),
    path('permissions/create/', views.create_permission, name='create_permission'),
    path('permissions/update/<int:permission_id>/', views.update_permission, name='update_permission'),
    path('permissions/delete/<int:permission_id>/', views.delete_permission, name='delete_permission'),

    # Asignación de roles
    # path('assign-role/<int:user_id>/', views.assign_role, name='assign_role'),
]
