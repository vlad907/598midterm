
from django.contrib import admin
from django.urls import path
from app1 import views as app1_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', app1_views.home),
    path('rules/', app1_views.rules),
    path('about/', app1_views.about),
    path('join/', app1_views.join),
    path('login/', app1_views.user_login),
    path('logout/', app1_views.user_logout),
]
