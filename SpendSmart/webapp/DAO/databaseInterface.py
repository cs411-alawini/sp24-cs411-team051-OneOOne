from django.db import connections

def getAllTransactionsForUser(id):
    if id is None:
        return []
    else:
        cur = connections['default'].cursor()
        cur.execute("""SELECT title,timestamp,amount
                   FROM Transaction
                   WHERE userId = {}
                   ORDER BY timestamp DESC
                   LIMIT 5;
                   """.format(id,id))
        txns = cur.fetchall() 
        return txns
    
