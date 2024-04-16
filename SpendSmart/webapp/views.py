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
    p =None
    if cur.execute("SELECT * from Credentials WHERE email = \'{}\'".format(username)):
        u,p = cur.fetchall()[0]
    if p!=password:
        return render(request,"index.html")
    cur.execute("SELECT userid FROM User WHERE email = \'{}\'".format(username))
    id = cur.fetchall()[0][0]
    print(id)
    cur.execute("SELECT txnId,title,timestamp,amount,note,paymentMethod,type,categoryId FROM Transaction WHERE userId = {}".format(id))
    data = cur.fetchall()
    # print(len(data),len(data[0]))
    # data = []
    context = {'txns':data}
    cur.close()

    return render(request,"home.html",context)