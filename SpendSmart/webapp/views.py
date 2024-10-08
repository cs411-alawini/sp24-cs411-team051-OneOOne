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

def home1(request):
    context = {}
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

    cur.execute("""SELECT SUM(amount) AS Income 
                   FROM Transaction
                   WHERE userId = {} AND type = 'income' AND YEAR(timestamp) = YEAR(CURRENT_DATE()) AND Month(timestamp) = MONTH(CURRENT_DATE());
                   """.format(id))
    inflow = cur.fetchall()[0][0]

    cur.execute("""SELECT SUM(amount) AS Expense 
                   FROM Transaction
                   WHERE userId = {} AND type = 'expense' AND YEAR(timestamp) = YEAR(CURRENT_DATE()) AND Month(timestamp) = MONTH(CURRENT_DATE());
                   """.format(id))
    outflow = cur.fetchall()[0][0]

    cur.execute("""SELECT SUM(amount) AS owes
                   FROM Borrows
                   WHERE Borrows.borrowerId = {} AND Borrows.isPaid = False;
                   """.format(id))
    owes = cur.fetchall()[0][0]
    
    cur.execute("""SELECT SUM(Borrows.amount) as owed
                   FROM Split JOIN Borrows on Split.splitId = Borrows.splitId
                   WHERE lenderId = {} AND isPaid = False;
                   """.format(id))
    owed = cur.fetchall()[0][0]

    cur.execute("""SELECT SUM(amount)
                   FROM MonthlyCategoryBudget
                   WHERE userId = {} AND Year(month) = YEAR(CURRENT_DATE()) AND Month(month) = MONTH(CURRENT_DATE());
                   """.format(id))
    tot_bud = cur.fetchall()[0][0]

    cur.execute("""SELECT SUM(amount) AS Expense
                   FROM Transaction
                   WHERE userId = {} AND type = 'expense' AND YEAR(timestamp) = YEAR(CURRENT_DATE()) AND Month(timestamp) = MONTH(CURRENT_DATE()) AND categoryId IN ( SELECT categoryId
                                                                            FROM MonthlyCategoryBudget
                                                                            WHERE userId = {} );

                   """.format(id,id))
    tot_spe = cur.fetchall()[0][0]    

    cur.execute("""SELECT title,timestamp,amount
                   FROM Transaction
                   WHERE userId = {}
                   ORDER BY timestamp DESC
                   LIMIT 5;
                   """.format(id,id))
    txns = cur.fetchall() 
    


    tot_rem = tot_bud - tot_spe
    context["inflow"] = inflow
    context["outflow"] = outflow
    context["owes"] = owes
    context["owed"] = owed
    context["tot_bud"] = tot_bud
    context["tot_spe"] = tot_spe
    context["tot_rem"] = tot_rem
    context["tot_rat"] = (tot_spe / tot_bud) * 100
    context["txns"] = txns

    cur.close()

    return render(request,"home1.html",context)