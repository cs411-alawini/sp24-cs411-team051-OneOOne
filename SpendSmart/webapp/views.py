from django.shortcuts import render
from django.http import HttpResponse
from django.db import connections

# Create your views here.
def index(request):
    return render(request,"index.html")

def home(request):
    cur = connections['default'].cursor()
    email = request.POST.get("email")
    password = request.POST.get("password")
    p =None
    if cur.execute("SELECT * from Credentials WHERE email = \'{}\'".format(email)):
        u,p = cur.fetchall()[0]
    if p!=password:
        return render(request,"index.html")
    cur.execute("SELECT userid FROM User WHERE email = \'{}\'".format(email))
    id = cur.fetchall()[0][0]

    

    cur.execute("SELECT txnId,title,timestamp,amount,note,paymentMethod,type,categoryName FROM Transaction T JOIN Category C ON T.categoryId = C.categoryId WHERE T.userId = {}".format(id))
    data = cur.fetchall()

    print(len(data))
    context = {'txns':data}
    cur.close()

    return render(request,"home.html",context)