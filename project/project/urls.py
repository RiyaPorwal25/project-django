"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.urls import include
from app.views import index
from app.views import about
from app.views import contact
from app.views import features
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index, name='index'),
    path('about/',about, name='about'),
    path('contact/',contact, name='contact'),
    path('features/',features, name='features'),
    path('results/', views.results, name='results'),
    path('generate_word_file/', views.generate_word_file, name='generate_word_file'),  # Ensure this line exists
]

