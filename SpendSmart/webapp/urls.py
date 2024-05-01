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
    path("splits",views.splits,name="splits"),
    path("get-users",views.get_users,name="get-users"),
    path("search-user",views.search_user,name="search-user"),
    path("add-split",views.add_split,name="add-split"),
    path("pay",views.pay,name="pay"),
    path("createUser",views.createUser,name="createUser"),
    path("deleteTransaction",views.deleteTransaction,name="deleteTransaction")
    
]