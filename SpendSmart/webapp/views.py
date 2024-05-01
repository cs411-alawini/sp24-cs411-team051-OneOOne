from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.db import connections
from django.contrib.auth.forms import AuthenticationForm
import plotly.express as px
import pandas as pd
import calendar
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json


import datetime

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
    # id = request.GET.get(id

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
    ie = getCurrentExpenseAndIncome(id)
    # print(ie[0][0])
    context["income"] = ie[0][0]
    context["expense"] = ie[0][1]
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
    
def getTransactionsForUser(id):
    if id is None:
        return []
    else:
        cur = connections['default'].cursor()
        cur.execute("""call GetTransactionsByUserId({})
                   """.format(id))
        txns = cur.fetchall() 
        return txns

def analysis(request):
    c = request.COOKIES.get('id')
    if c is None:
        print("COOKIES IS NON")
        return render(request,"index.html", {'user': { 'is_authenticated': False}})
    context = {'user': { 'is_authenticated': True}}
    # context['user.is_authenticated'] = True
    cur = connections['default'].cursor()
    id = c
    cur.execute("CALL GetMonthlyExpensePerCategorySortedNew({})".format(id))
    data = cur.fetchall()
    data = pd.DataFrame(data,columns=["Year","Month","Expense","Id","Category"])
   

    year = request.POST.get("year")
    month = request.POST.get("month")
    year2 = request.POST.get("year2")

    
    context["Chart"] = None
    context["Chart2"] = None

    if year != None and month != None:
        year = int(year)
        month = int(month)
        df = data.loc[(data['Year'] == year) & (data['Month'] == month)]
        fig = px.pie(df, names="Category", values="Expense", hole=0.5,hover_name="Category")
        chart = fig.to_html()
        context["Chart"] = chart
    
        if year2 == '':
            year2 = year
        year2 = int(year2)

        df = data.loc[(data['Year'] == year2)]

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
    transactions = getTransactionsForUser(id)
    # print(transactions)
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

def deleteTransaction(request):
    if request.method == 'GET':
        return redirect('index')
    else:
        userId = getUserId(request)
        if userId is None:
            return redirect('index')
        else: 
            print("DELETEEE")
            print(request.POST)
            txnId = None
            if 'txnId2' in request.POST:
                txnId = request.POST['txnId2']
                print(txnId)
                deleteTransactionSql(txnId)
            return redirect('transactions')

def deleteTransactionSql(txnId):
    cur = connections['default'].cursor()
    print("""delete from Transaction where txnId = {};""".format(txnId))
    cur.execute("""delete from Transaction where txnId = {};""".format(txnId))
    return cur.fetchall()

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
            txnId = None
            if 'txnId1' in request.POST:
                txnId = request.POST['txnId1']
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
            description = "\""+description+"\"" if description != '' else 'NULL'
            date = "'"+date+"'" if date != '' else 'NULL'
            category = "'"+subcategory+"'" if (subcategory != '') else "'"+category+"'" if category != '' else 'NULL'
            # subcategory =  'NULL'
            print(txnId)
            if txnId is not None:
                updateTransaction(txnId, description,amount,type,userId,category,note,paymentMethod,date)
            else :
                insertTransaction(description,amount,type,userId,category,note,paymentMethod,date)
            return redirect('transactions')
        

def getUserId(request):
    return request.COOKIES.get('id')
     

def getCategoriesForUser(userId):
    cur = connections['default'].cursor()
    cur.execute("""call GetCategories({});""".format(userId))
    return cur.fetchall()

def getCurrentExpenseAndIncome(userId):
    cur = connections['default'].cursor()
    cur.execute("""call GetIncomeAndExpenseOfCurrentMonth({});""".format(userId))
    return cur.fetchall()
    
def updateTransaction(txnId, p_title, p_amount, p_type, p_userId, p_categoryId, p_note, p_paymentMethod, p_transactionDate):
    cur = connections['default'].cursor()
    query = """CALL UpdateTransaction({},{}, {}, {}, {}, {}, {}, {});""".format(txnId, p_amount, p_type, p_transactionDate, p_title, p_categoryId, p_note, p_paymentMethod)
    print(query)
    cur.execute("""CALL UpdateTransaction({},{}, {}, {}, {}, {}, {}, {});"""
                .format(txnId, p_amount, p_type, p_transactionDate, p_title, p_categoryId, p_note, p_paymentMethod))
    return cur.fetchall()

def insertTransaction( p_title, p_amount, p_type, p_userId, p_categoryId, p_note, p_paymentMethod, p_transactionDate):
    cur = connections['default'].cursor()
    query = """CALL InsertTransaction({}, {}, {}, {}, {}, {}, {}, {});""".format(p_title, p_amount, p_type, p_userId, p_categoryId, p_note, p_paymentMethod, p_transactionDate)
    print(query)
    cur.execute("""CALL InsertTransaction({}, {}, {}, {}, {}, {}, {}, {});"""
                .format(p_title, p_amount, p_type, p_userId, p_categoryId, p_note, p_paymentMethod, p_transactionDate))
    return cur.fetchall()

def budget(request):
    c = request.COOKIES.get('id')
    if c is None:
        print("COOKIES IS NON")
        return render(request,"index.html", {'user': { 'is_authenticated': False}})
    context = {'user': { 'is_authenticated': True}}
    id = c

    categories = getCategoriesForUser(id)
    # print(categories)
    parentCategories = [[tup[0], tup[1]] for tup in categories if tup[2] is None]
    grouupedCategories = {}
    for tup in categories:
        if tup[2] not in grouupedCategories:
            grouupedCategories[tup[2]] = []
        grouupedCategories[tup[2]].append([tup[0], tup[1]])

    # Convert the dictionary to a list of tuples
    # result = [(key, value) for key, value in grouupedCategories.items()]

    # print(result)
    # print(parentCategories)
    # print(transactions)
    context["parentCategories"] = parentCategories
    context["grouupedCategories"] = json.dumps(grouupedCategories)

    year = request.POST.get("year")
    month = request.POST.get("month")
    today = datetime.date.today()
    cur = connections['default'].cursor()
    if month == None and year == None:
        month = int(today.month)
        year = int(today.year)
    print(year,month)
    cur.execute('''SELECT categoryName, amount, m.categoryId
                   FROM MonthlyCategoryBudget m JOIN Category c ON m.categoryId = c.categoryId
                   WHERE m.UserId = {} and MONTH(month) = {} and YEAR(month) = {};'''.format(id,month,year))
    data = cur.fetchall()
    res = []
    for i in range(len(data)):
        d = list(data[i])
        cur.execute("Call MonthlyCategoryExpense({},{},{},{})".format(id,d[2],year,month))

        l = cur.fetchall()
        if l == ():
            l =0
        else:
            l = l[0][0]
        
        d.append(l)
        d.append(d[1]-l)
        res.append(d)
    
    # print(res)
        
    context['data'] = res

    return render(request,"budget.html",context)

def submitBudget(request):
    # print("here")
    if request.method == 'GET':
        return redirect('')
    else:
        userId = getUserId(request)
        if userId is None:
            redirect('')
        else: 
            print(request.POST)
            description = request.POST['description']
            amount = request.POST['amount']
            date = request.POST['date']
            category = request.POST['category']
            subcategory = request.POST['sub-category']
            print(date)
            print(amount)

            # subcategory =  'NULL'
            description = "'"+ description + "'"
            date = "'" + date + "'"
            insertBudget(description,amount,date,category,userId)
            return redirect('budget')

def insertBudget( p_description, p_amount, p_date, p_categoryId, p_userId):
    cur = connections['default'].cursor()
    query = """INSERT INTO MonthlyCategoryBudget (description,amount,month,categoryId,userId) VALUES ({},{},{},{},{});""".format(p_description, p_amount, p_date, p_categoryId, p_userId)
    print(query)
    cur.execute(query)
    return cur.fetchall()

def splits(request):
    cur = connections['default'].cursor()
    c = request.COOKIES.get('id')
    if c is None:
        print("COOKIES IS NON")
        return render(request,"index.html", {'user': { 'is_authenticated': False}})
    context = {'user': { 'is_authenticated': True}}
    id = c

    query = '''SELECT Split.lenderId, User.userName, User.firstName, User.lastName, SUM(Borrows.amount) AS owed, Borrows.splitId
            FROM Split JOIN User ON Split.lenderId = User.userId JOIN Borrows on Borrows.splitId = Split.splitId
            WHERE Borrows.borrowerId = {} AND Borrows.isPaid = False AND Split.lenderId != {}
            GROUP BY Split.lenderId, User.userName, User.firstName, User.lastName, Borrows.splitId;'''.format(id,id)
    cur.execute(query)
    borrowed_data = cur.fetchall()
    context['borrowed_data'] = borrowed_data

    query = '''SELECT  Borrows.borrowerId, User.userName, User.firstName, User.lastName, SUM(Borrows.amount) as Balance 
            FROM (Split JOIN Borrows ON Split.splitId = Borrows.splitId) JOIN User ON Borrows.borrowerId = User.userId
            WHERE Split.lenderId = {} AND Borrows.isPaid = False AND Borrows.borrowerId != {}
            GROUP BY Borrows.borrowerId, User.userName, User.firstName, User.lastName;'''.format(id,id)
    cur.execute(query)
    owed_data = cur.fetchall()
    context['owed_data'] = owed_data

    
    return render(request,"splits.html",context)


@csrf_exempt
def get_users(request):
    id = request.COOKIES.get('id')
    if id is None:
        print("COOKIES IS NON")
        return render(request,"index.html", {'user': { 'is_authenticated': False}})
    else: 
        # search_text = request.POST.get('user')
        payload = []
    
        # if search_text:
        cur = connections['default'].cursor()
        cur.execute("""
                        SELECT userName from User
                        WHERE userId <> {} AND userName <> 'system'
                        """.format(id))
        results = cur.fetchall()
        # results = [result[0] for result in results]
        # context = {"results": results}
        # return render(request, 'partials/search-result.html', context)

        for result in results:
            payload.append(result[0])
                
        return JsonResponse({
            'status' : True,
            'users' : payload
        })


@csrf_exempt 
def search_user(request):
    id = request.COOKIES.get('id')
    if id is None:
        print("COOKIES IS NON")
        return render(request,"index.html", {'user': { 'is_authenticated': False}})
    else: 
        search_text = request.GET.get('user')
        payload = []
    
        # if search_text:
        cur = connections['default'].cursor()
        cur.execute("""
                        SELECT userName from User
                        WHERE userName = '{}'
                        """.format(search_text))
        results = cur.fetchall()
        
        for result in results:
            payload.append(result[0])
                
        if results:
            return JsonResponse({
                'exists' : True,
                'status' : True,
                'users' : payload
            })
        else:
            return JsonResponse({
                'exists' : False,
                'status' : True,
                'users' : payload
            })

def submitSplit(request):
    # print("here")
    if request.method == 'GET':
        return redirect('')
    else:
        userId = getUserId(request)
        if userId is None:
            redirect('')
        else: 
            print(request.POST)
            description = request.POST['description']
            amount = request.POST['amount']
            date = request.POST['date']
            category = request.POST['category']
            subcategory = request.POST['sub-category']
            print(date)
            print(amount)

            # subcategory =  'NULL'
            description = "'"+ description + "'"
            date = "'" + date + "'"
            insertBudget(description,amount,date,category,userId)
            return redirect('budget')

def pay(request):
    if request.method == 'GET':
        return redirect('')
    else:
        userId = getUserId(request)
        if userId is None:
            redirect('')
        else: 
            print(request.POST)
            cur = connections['default'].cursor()
            splitId = request.POST['splitId']

            query = '''UPDATE Borrows SET isPaid = 1 WHERE SplitId = {} and borrowerId = {};'''.format(splitId,userId)
            cur = connections['default'].cursor()
            cur.execute(query)
            cur.close()
            return redirect('splits')

def createUser(request):
    if request.method == 'GET':
        return redirect('index')
    else:
        print(request.POST)
        cur = connections['default'].cursor()
        username = request.POST['username']
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        email = request.POST['email']
        pwd = request.POST['password']
        cpwd = request.POST['username']
        context = {}
        # if cpwd != pwd:
        #     context['alert_type'] = 'warning'
        #     context['alert_message'] = "Passwords do not match!"
        #     return redirect('register')
        query = '''INSERT INTO Credentials (email,password) VALUE (\'{}\',\'{}\')
                '''.format(email,pwd)
        cur.execute(query)
        query = '''INSERT INTO User (userName,firstName,lastName,email) VALUE (\'{}\',\'{}\',\'{}\',\'{}\')
                   '''.format(username,fname,lname,email)
        cur.execute(query)
        return redirect('index')
    return redirect('')

def get_user_id(user_name):
    cur = connections['default'].cursor()
    cur.execute("""
                SELECT userId from User
                WHERE userName = '{}'; 
                """.format(user_name))

    return cur.fetchall()[0][0]    

@csrf_exempt            
def add_split(request):
    id = request.COOKIES.get('id')
    if id is None:
        print("COOKIES IS NON")
        return render(request,"index.html", {'user': { 'is_authenticated': False}})
    else: 
        if request.method == 'GET':
            return redirect("home")
        else:
            # print(request.body)
            # data = json.loads(request.body)
            # print(data)
            try:
                # Parse JSON data from request body
                data = json.loads(request.body)
                title = data['title']
                note = data['note']
                bill_amount = data['billAmount']
                my_amount = data['myAmount']
                users = data['users']
                user_amounts = data['userAmounts']
                
                # Process the data
                transaction = \
                f'''SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
                        START TRANSACTION;
        
                        INSERT INTO Split(title, amount, note, lenderId)
                        VALUES ('{title}', {bill_amount}, '{note}', {id});
                        SET @split_id = LAST_INSERT_ID();
                        
                        
                        INSERT INTO Transaction(title, amount, note, type, userId) 
                        SELECT '{"Split: " + title}', {my_amount}, '{note}', '{'Expense'}', {id}
                        FROM DUAL
                        WHERE {my_amount} > 0;
                        
                        '''
                
                user_ids = [get_user_id(user) for user in users]
                
                for user, amount in zip(user_ids, user_amounts):
                    transaction += \
                    f'''INSERT INTO Borrows(borrowerId, splitId, Amount, isPaid)
                        VALUES ({user}, @split_id, {amount}, {0});
                                      
                        '''
                
                transaction += \
                    f'''COMMIT;'''
                print(transaction)
                
                cur = connections['default'].cursor()
                cur.execute(transaction)
                
                
                return JsonResponse({'status': 'success', 'message': 'Form data received'})
            except json.JSONDecodeError:
                return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)