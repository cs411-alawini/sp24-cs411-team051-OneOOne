from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name="index"),
    path("home",views.home,name="home"),
    path("home1",views.home1,name="home1")
]