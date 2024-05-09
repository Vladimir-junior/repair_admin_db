# from django.contrib import admin
from django.urls import path

from users.admin import site

urlpatterns = [
    path('', site.urls),
]
