import imp
from multiprocessing.spawn import import_main_path
from django.urls import path

from .views import HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home')
]