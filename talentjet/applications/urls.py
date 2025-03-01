from django.urls import path
from . import views

urlpatterns = [
    path('apply/<int:job_id>/', views.apply_for_job, name='apply_for_job'),
    path('my/', views.my_applications, name='my_applications'),
    path('manage/', views.manage_applications, name='manage_applications'),
    path('accept/<int:application_id>/', views.accept_application, name='accept_application'),
    path('reject/<int:application_id>/', views.reject_application, name='reject_application'),
]
