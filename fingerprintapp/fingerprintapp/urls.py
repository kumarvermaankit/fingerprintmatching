from matchingapp import views as views_matchingapp
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views_matchingapp.matching, name='matching'),
    ]
