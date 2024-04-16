from django.shortcuts import render
from django.http import HttpResponse
from django.db import connections

# Create your views here.
def index(request):
    return render(request,"index.html")

def home(request):
    cur = connections['default'].cursor()
    username = request.POST.get("username")
    password = request.POST.get("password")
    cur.execute("SELECT * from Credentials WHERE email = \'{}\'".format(username))
    u,p = cur.fetchall()[0]
    if p!=password:
        return render(request,"index.html")
    
    
    cur.close()
    return HttpResponse("Success!")