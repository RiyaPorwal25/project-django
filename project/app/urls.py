from django.urls import path
from . import views
from django.contrib import admin
from app.views import index
from app.views import about
from app.views import contact
from app.views import features

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index, name='index'),
    path('results/about/',about, name='about'),
    path('results/contact/',contact, name='contact'),
    path('results/features/',features, name='features'),
    path('results/', views.results, name='results'),
    path('generate_word_file/', views.generate_word_file, name='generate_word_file'),
]
