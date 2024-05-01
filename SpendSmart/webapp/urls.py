from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name="index"),
     path("login",views.login,name="login"),
    path("home",views.home,name="home"),
    path("home1",views.home1,name="home1"),
    path("register",views.register,name="register"),
    path("logout",views.logout,name="logout"),
    path("analysis",views.analysis,name="analysis"),
    path("transactions",views.transactions,name="transactions"),
    path("submitTransaction",views.submitTransaction,name="submitTransaction"),
    path("budget",views.budget,name="budget"),
    path("submitBudget",views.submitBudget,name="submitBudget"),
    path("splits",views.splits,name="splits")
]