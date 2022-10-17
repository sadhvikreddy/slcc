import pandas as pd
import re

def getPayload(reqDate):
    # Reading CSV Files
    co = pd.read_csv("./data/commissions.csv")
    ol = pd.read_csv("./data/order_lines.csv")
    o = pd.read_csv("./data/orders.csv")
    # pp = pd.read_csv("./data/product_promotions.csv")
    # prod = pd.read_csv("./data/products.csv")
    # prom = pd.read_csv("./data/promotions.csv")

    # Preprocessing date field in order dataset
    x = pd.to_datetime(o['created_at'])
    x = x.dt.date
    o['date'] = pd.to_datetime(x)
    # Preprocessing date field in commissions dataset
    # y = pd.to_datetime(co['date'])
    # y = y.dt.date
    # co['date'] = pd.to_datetime(y)

    #getting unique datas are client requested per day caluclations.
    udates = o['date'].unique()
    dayorders = []
    for day in udates:
        data = o[o['date'] == day]
        dayorders.append(data)

    payload = {}

    for entry in dayorders:
        # Each iteration if data frame of day
        date, time = str(entry['date'].unique()[0]).split("T")
        #unique customers per day
        customer = len(entry['customer_id'].unique())
        data1 = pd.DataFrame()
        total_amt = 0
        no_of_orders = 0
        
        for orderid in entry['id']:
            #Selecting orderids fromorderlines dataset based on id from orders
            data = ol.loc[ol['order_id'] == orderid]
            data1 = data1.append(data)
            # for average caluclations
            total_amt = total_amt + sum(data['total_amount'])
            no_of_orders += 1

        #Caluclation requested by client
        total_discount_amount= sum(data1['discounted_amount'])
        uni = data1['product_id'].unique()
        uniPros = data1.loc[data1['product_id'].isin(uni)]
        items = sum(uniPros['quantity'])
        order_total_avg = total_amt / no_of_orders
        discount_rate_avg = data1['discount_rate'].mean()
        
        #TODO: Commissions and promotion caluclations
        # data2 = co[co['date'] == entry['date'].unique()[0]]

        # appending data into dictionary
        payload[date] = {
            "customer": customer,
            "total_discount_amount": total_discount_amount,
            "items": items,
            "order_total_avg": order_total_avg,
            "discount_rate_avg": discount_rate_avg
        }
    #Regular expression to match "YYYY-MM-DD"
    dateRegex = "^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"
    rem = re.match(dateRegex,reqDate)
    #returning
    if not rem:
        #Error handling for incorrecr API Call
        return 1,"Check the query format: YYYY-MM-DD", {}
    else:
        #Exception handling for missing data
        try:
            #Successful return of API Call
            if(payload[reqDate]):
                return 0, "Successful api call!"  , payload[reqDate]
        except KeyError as e:
            #Handing Valid date format but data missing
            return 1, str(e) + "is missing date from database", {}
            