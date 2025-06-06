"""
URL configuration for talentjet project.

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
	path('signup/', views.signup, name='signup'),
	path('login/', views.login_view, name='login'),
	path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
	path('profile/', views.profile, name='profile'),
	path('resume/delete/', views.delete_resume, name='delete_resume'),
	path('profile/update/', views.profile_update, name='profile_update'),
	path('profile/resume/delete/', views.delete_resume, name='delete_resume'),
]
