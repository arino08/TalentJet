from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('create/', views.create_job, name='create_job'),
    path('<int:pk>/', views.job_detail, name='job_detail'),
    path('<int:pk>/delete/', views.delete_job, name='delete_job'),
]
