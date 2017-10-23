
#### ________  SQL : Exercise1  _______ ####
print("\n\nSTARTING SQL SOLUTION\n\n")
print("Exercise 1\n")

import sqlite3
conn = sqlite3.connect('northwind.db')
conn.text_factory = lambda x: str(x, 'latin1')

query = """
SELECT Customers.CustomerID, Orders.OrderID, Products.ProductName
    FROM Customers 
    INNER JOIN Orders ON Orders.CustomerID = Customers.CustomerID
    INNER JOIN [Order Details] ON [Order Details].OrderID = Orders.OrderID
    INNER JOIN Products ON Products.ProductID = [Order Details].ProductID
WHERE Orders.CustomerID = 'ALFKI'; 
"""

print("Customer ID\t Order ID\t Product Name\n")
for row in conn.execute(query):
    print(row)
    
#### ________  SQL : Exercise2  _______ ####
print("\nExercise 2\n")
query =  """SELECT Orders.OrderID, Products.ProductName 
            FROM Customers 
            INNER JOIN Orders ON Orders.CustomerID = Customers.CustomerID
            INNER JOIN [Order Details] ON [Order Details].OrderID = Orders.OrderID
            INNER JOIN Products ON Products.ProductID = [Order Details].ProductID
          WHERE [Order Details].OrderID IN 
            ( /* Subquery that outputs orders with at least 2 products */
                    SELECT Orders.OrderID
                        FROM Customers 
                        INNER JOIN Orders ON Orders.CustomerID = Customers.CustomerID
                        INNER JOIN [Order Details] ON [Order Details].OrderID = Orders.OrderID
                    WHERE Orders.CustomerID = 'ALFKI'
                    GROUP BY [Order Details].OrderID
                    HAVING COUNT([Order Details].OrderID) > 1   
            ); """
    
for row in conn.execute(query):
    print(row)



#### _______  MONGODB : Exerise1 _________ ####

print("\n\nSTARTING PYMONGO SOLUTION\n\n")
print("Exercise 1\n")
from pymongo import MongoClient; import pprint
client = MongoClient('localhost', 27017)
db = client.Northwind

orders = db['orders']
order_details = db['order-details']
products = db['products']

# 1) Finding ALFKI's orders
order_ids = []
for order in orders.find({"CustomerID" : "ALFKI"}, {'OrderID': 'true'}):
    order_ids.append(order['OrderID'])
    
    
# 2) Finding product ids from orders
product_ids = []; i=0;  ord2prod = {}
while i < len(order_ids): 
    temp = []
    for  entry in order_details.find({'OrderID': order_ids[i]}):
        temp.append(entry['ProductID'])
    ord2prod[str(order_ids[i])] = temp
    i = i +1
        
    
# 3) Finding product names from product ids
orders = list(ord2prod.keys())
product_ids = list(ord2prod.values())

#unpacking list of lists
flat_list=[]
for entry in product_ids:
    for element in entry:
        flat_list.append(element)
       
product_names = []; i=0        
while i < len(flat_list): 
    for entry in products.find({'ProductID' : flat_list[i]}):
        product_names.append(entry['ProductName']) 
    i = i+1
 
# Creating dictionary: {productID : productName}
id2name = {k:v for k,v in list(zip(flat_list, product_names))}    

# Creating final dictionary: {orderID : productName}    
new_values = []
for i in range(len(orders)):
    temp = []
    for j in range(len(product_ids[i])):
        temp.append(id2name[product_ids[i][j]])
    new_values.append(temp)
    
order2name = {k:v for k,v in list(zip(orders, new_values))}
pprint.pprint(order2name)   


#### _______  MONGODB : Exerise2 _________ ####
print("\nExercise 2\n")

#__( NOTE: This dict comprehension only works in Python 3 )__#

# We create a new dict that only includes orders with more than 1 product
ex2_dict = { k:v for k,v in order2name.items() if len(v)>1 }  
pprint.pprint(ex2_dict)  
    
#print(client.database_names())


#### _______  TEACH SQL : Exerise3 _________ ####
print("\n\nSTARTING TEACH SQL SOLUTION: Exercise 3\n\n")

query = """
SELECT Customers.CustomerID, Orders.OrderID, [Order Details].Discount,
        CASE
            WHEN [Order Details].Discount == 0 THEN "No Discount"
            ELSE "Some Discount" 
        END as "Save me some money"
    FROM Customers 
    INNER JOIN Orders ON Orders.CustomerID = Customers.CustomerID
    INNER JOIN [Order Details] ON [Order Details].OrderID = Orders.OrderID
    INNER JOIN Products ON Products.ProductID = [Order Details].ProductID
WHERE Orders.CustomerID = 'ALFKI' AND "Save me some money" = "Some Discount";
"""

for row in conn.execute(query):
    print(row)


#### _______  TEACH MONGODB : Exerise3 _________ ####
print("\n\nSTARTING TEACH MONGO SOLUTION: Exercise 3\n\n")

# First we print the  prices before the update
print("Prices Before Update\n")
for i in range(len(order_ids)):
   pprint.pprint([l for l in order_details.find({'OrderID': order_ids[i]}, {"UnitPrice":1, "_id":0})])

# Then we print them after the Euro to Dollar update (1 euro = 1.18 usd)
print("\nPrices After Update\n")
for i in range(len(order_ids)):
    order_details.update_many({'OrderID': order_ids[i]},{"$mul": {"UnitPrice": 1.18}})
    pprint.pprint([l for l in order_details.find({'OrderID': order_ids[i]}, {"UnitPrice":1, "_id":0})])

