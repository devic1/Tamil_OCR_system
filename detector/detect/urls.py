from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload',views.uploaded,name='uploaded'),
    path('textd',views.textd,name='textd'),
    path('text',views.text,name='text'),
]
