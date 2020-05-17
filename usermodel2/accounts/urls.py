from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns=[
    path('register/', views.register, name='register'),
    path('user_login/', views.user_login, name='user_login'),
    path('profile/<int:pk>',views.view_profile, name='view_profile'),
    path('edit/<int:pk>',views.edit_profile,name='edit'),
    path('change-password/',views.change_password,name='change_password'),
    path('patient-list/',views.patient_list,name='patient_list'),
    path('patient-detail/<int:id>/',views.patient_detail,name='patient_detail'),
    path('patient-create/',views.patient_create,name='patient_create'),
    path('patient-delete/<int:id>/',views.patient_delete,name='patient_delete'),
    path('patient-update/<int:id>/',views.patient_update,name='patient_update'),
]
