from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.db import connections
from django.contrib.auth.forms import AuthenticationForm
import plotly.express as px
import pandas as pd
import calendar
import json



# Create your views here.
def index(request):
    # print(request)
    c = request.COOKIES.get('id')
    if c is None:
        # print("COOKIES IS NON")
        return render(request,"index.html", {'user': { 'is_authenticated': False}})
    else:
        # print("COOKIE + ", c)
        return redirect('home')

def login(request):
    if request.method == 'GET':
        return redirect('index')
    cur = connections['default'].cursor()
    c = request.COOKIES.get('id')
    # if c is not None:
    #     return redirect('home')
    # else:
    #     print("COOKIE + ", c)
    #     return redirect('home1')
    email = request.POST.get("username")
    password = request.POST.get("password")
    p =None
    if cur.execute("SELECT * from Credentials WHERE email = \'{}\'".format(email)):
        u,p = cur.fetchall()[0]
    if p!=password:
        return render(request,"index.html", {'alert_type':'danger', 'alert_message':"Login Failed"})
    cur.execute("SELECT userid FROM User WHERE email = \'{}\'".format(email))
    id = cur.fetchall()[0][0]
    
    
    context = {}
    # print("ID = ",c)
    # id = request.GET.get(id)

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
    context['user'] = { 'is_authenticated': True}
    response =  redirect("home")
    response.set_cookie("id", id)
    return response

def home(request):
    c = request.COOKIES.get('id')
    if c is None:
        # print("COOKIES IS NON")
        return render(request,"index.html", {'user': { 'is_authenticated': False}})
    context = {'user': { 'is_authenticated': True}}
    id = c
    transactions = getAllTransactionsForUser(id)
    # print(transactions)
    context["transactions"] = transactions
    return render(request,"home.html",context)

def home1(request):
    c = request.COOKIES.get('id')
    if c is None:
        # print("COOKIES IS NON")
        return render(request,"index.html", {'user': { 'is_authenticated': False}})
    else:
        # print("COOKIE + ", c)
        id = c
    # print(request)
    context = {}
    cur = connections['default'].cursor()
    # email = request.POST.get("email")
    # password = request.POST.get("password")
    # p =None
    # if cur.execute("SELECT * from Credentials WHERE email = \'{}\'".format(email)):
    #     u,p = cur.fetchall()[0]
    # if p!=password:
    #     return render(request,"index.html")
    # cur.execute("SELECT userid FROM User WHERE email = \'{}\'".format(email))
    # id = request.GET.get("id")
    # id = request.GET.get(id)

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

def register(request):
    return render(request,"register.html",)

def logout(request):
    response = render(request,"index.html", {'user': { 'is_authenticated': False}})
    
    # Clear session cookies
    if request.session:
        request.session.flush()
    
    # Clear any other cookies you may have set
    response.delete_cookie('id')
    
    # Redirect to a different page after logout
    return response


def getAllTransactionsForUser(id):
    if id is None:
        return []
    else:
        cur = connections['default'].cursor()
        cur.execute("""SELECT title,timestamp,amount
                   FROM Transaction
                   WHERE userId = {}
                   ORDER BY timestamp DESC;
                   """.format(id,id))
        txns = cur.fetchall() 
        return txns

def analysis(request):
    cur = connections['default'].cursor()
    id = 1
    cur.execute("CALL GetMonthlyExpensePerCategorySortedNew({})".format(id))
    data = cur.fetchall()
    data = pd.DataFrame(data,columns=["Year","Month","Expense","Id","Category"])
   

    year = request.POST.get("year")
    month = request.POST.get("month")
    year2 = request.POST.get("year2")

    context = {}
    context["Chart"] = None
    context["Chart2"] = None

    if year != None and month != None:
        year = int(year)
        month = int(month)
        df = data.loc[(data['Year'] == year) & (data['Month'] == month)]
        fig = px.pie(df, names="Category", values="Expense", hole=0.5,hover_name="Category")
        chart = fig.to_html()
        context["Chart"] = chart
    
        if year2 == None:
            year2 = year
        year2 = int(year2)
        df = data.loc[(data['Year'] == year2)]
        print(data.loc[(data['Year'] == 2024)])
        df = df.groupby(["Month"],as_index=False).sum()
        df['Month'] = df['Month'].apply(lambda x: calendar.month_abbr[x])

        fig = px.bar(df,x="Month",y="Expense")
        fig.update_xaxes(type='category')
        chart2 = fig.to_html()
        context["Chart2"] = chart2

    context['year'] = year
    context['month'] = month
    context['year2'] = year2

    return render(request,"analysis.html",context)
    
def transactions(request):
    c = request.COOKIES.get('id')
    if c is None:
        # print("COOKIES IS NON")
        return render(request,"index.html", {'user': { 'is_authenticated': False}})
    context = {'user': { 'is_authenticated': True}}
    id = c
    transactions = getAllTransactionsForUser(id)
    categories = getCategoriesForUser(id)
    # print(categories)
    parentCategories = [[tup[0], tup[1]] for tup in categories if tup[2] is None]
    grouupedCategories = {}
    for tup in categories:
        if tup[2] not in grouupedCategories:
            grouupedCategories[tup[2]] = []
        grouupedCategories[tup[2]].append([tup[0], tup[1]])

    # Convert the dictionary to a list of tuples
    result = [(key, value) for key, value in grouupedCategories.items()]

    # print(result)
    # print(parentCategories)
    # print(transactions)
    context["transactions"] = transactions
    context["parentCategories"] = parentCategories
    context["grouupedCategories"] = json.dumps(grouupedCategories)
    # context['user']
    return render(request,"transactions.html",context)

def submitTransaction(request):
    # print("here")
    if request.method == 'GET':
        return redirect('')
    else:
        userId = getUserId(request)
        if userId is None:
            redirect('')
        else: 
            print("FOMRM")
            print(request.POST)
            description = request.POST['description']
            amount = request.POST['amount']
            date = request.POST['date']
            type = request.POST['type']
            category = request.POST['category']
            subcategory = request.POST['sub-category']
            note = request.POST['note']
            paymentMethod = request.POST['paymentMethod']
            print(date)
            print(amount)
            type = "'"+type+"'"
            paymentMethod = "'"+paymentMethod+"'"
            note = "'"+note+"'" if note != '' else 'NULL'
            description = "'"+description+"'" if description != '' else 'NULL'
            date = "'"+date+"'" if date != '' else 'NULL'
            category = "'"+subcategory+"'" if subcategory != '' else "'"+category+"'" if category != '' else 'NULL'
            # subcategory =  'NULL'
            insertTransaction(description,amount,type,userId,category,note,paymentMethod,date)
            return redirect('transactions')
        

def getUserId(request):
    return request.COOKIES.get('id')
     

def getCategoriesForUser(userId):
    cur = connections['default'].cursor()
    cur.execute("""call GetCategories({});""".format(userId))
    return cur.fetchall()
    
def insertTransaction( p_title, p_amount, p_type, p_userId, p_categoryId, p_note, p_paymentMethod, p_transactionDate):
    cur = connections['default'].cursor()
    query = """CALL InsertTransaction({}, {}, {}, {}, {}, {}, {}, {});""".format(p_title, p_amount, p_type, p_userId, p_categoryId, p_note, p_paymentMethod, p_transactionDate)
    print(query)
    cur.execute("""CALL InsertTransaction({}, {}, {}, {}, {}, {}, {}, {});"""
                .format(p_title, p_amount, p_type, p_userId, p_categoryId, p_note, p_paymentMethod, p_transactionDate))
    return cur.fetchall()