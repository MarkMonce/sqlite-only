################################################################################
#
#This is a python script to allow basic R/W functions to the test database
# Date Created: 7/3/24
# By Mark Monce
# See readme.txt in Git Repo for the core function descriptions
#
##################################################################################

##
#   DB Connection section: Assumes the db and tables already exist; if not view test.sql and sqlite.py
#   Files to recreate the necessary DB structures
##

##
import sqlite3

conn = sqlite3.connect('testdb.db')
cursor = conn.cursor()

#################################################
#
# Function Definitions to write to and read from the tables.
#
###################################################


##################     ADD PERSON FUNCTION          #######################################################################

def addperson(fname, lname, age, balance):

    insert_sql = f"INSERT INTO person (firstname, lastname, age, accountbalance) VALUES ('{fname}', '{lname}', '{age}', '{balance}')"

    cursor.execute(insert_sql)


    return

######## ADD PRODUCT FUNCTION          #######################################################################

def addproduct(name, description, stock, price):

    insert_sql = f"INSERT INTO product (productname, description, quantityinstock, price) VALUES ('{name}', '{description}', '{stock}', '{price}')"

    cursor.execute(insert_sql)

    return

####### ADD ORDER FUNCTION       N#######################################################################

def addorder(person_id, product_id, quantity):

    try:
        cursor.execute("SELECT quantityinstock FROM product WHERE id = ?", (product_id,))
        
        product = cursor.fetchone()
        availableqty = product[0]
        quantity = int(quantity)
        availableqty = int(availableqty)
        product = None
        # Calculate the total cost of the order and check product availability

        cursor.execute("SELECT price FROM product WHERE id = ?", (product_id,))
        product= cursor.fetchone()
        product_price = product[0]
        total_cost = product_price * float(quantity)
        product = None
        # print(f'Quantity: {availableqty}')
        ##Calculate If Sufficient Quantity is available in products:


        if quantity <= availableqty:
            print(f'The quantity available {availableqty} is sufficient to fulfill the quantity ordered: {quantity}\n')
        else:
            print(f'The quantity available {availableqty} is NOT sufficient to fulfill the quantity ordered: {quantity}\nEither reduce the quantity or select another product.\n')
            return
        ##Calculate if the customer has sufficient funds to complete the order:
        cursor.execute("SELECT accountbalance FROM person where id =?", (person_id,))
        customer = cursor.fetchone()
        if customer is not None:
            customer_balance = customer[0]
        else:
            print("NO CUSTOMER FOUND!!!!")
        
        if customer_balance < total_cost:
            print(f'The customer does not have sufficient funds$ ${customer_balance}:  to complete the transaction cost ${total_cost}.\n')
        else:
            print(f'Transaction for ${total_cost} approved. Cost will be deducted from customer balance of ${customer_balance}\n')
        
        return
    
    except sqlite3.Error as e:
        print(f"An Error Occured: : {e}")

    # # Get the current date
    # transaction_date = datetime.now().strftime('%Y-%m-%d')

    # # Insert the new order into the orders table
    # insert_sql = """
    # INSERT INTO orders (transaction_date, person_id, product_id, quantity, total_cost)
    # VALUES (?, ?, ?, ?, ?)
    # """
    # cursor.execute(insert_sql, (transaction_date, person_id, product_id, quantity, total_cost))

    # Commit the transaction and close the connection

####### LIST PERSON(CUSTOMER) FUNCTION       #######################################################################

def listcustomers():
    cursor.execute('SELECT * from person')
    rows = cursor.fetchall()
    
    # Convert to list of dictionaries (optional for better readability)
    column_names = [description[0] for description in cursor.description]
    customer_list = [dict(zip(column_names, row)) for row in rows]
    
    # Close the connection
    for customer in customer_list:
        print(customer)

    return 

####### LIST PRODUCT FUNCTION      #######################################################################

def listproducts():
    cursor.execute('SELECT * from product')
    rows = cursor.fetchall()
    
    # Convert to list of dictionaries (optional for better readability)
    column_names = [description[0] for description in cursor.description]
    product_list = [dict(zip(column_names, row)) for row in rows]
    
    for product in product_list:
            print(product)


    return 

####### Get basic customer info while processing a transaction     #######################################################################

def getcustomerinfo(custid):

    cursor.execute("SELECT firstname, lastname, accountbalance from person WHERE id=?", (custid,))

    cust = cursor.fetchone()

    if cust is not None:
        custfname=cust[0]
        custlname=cust[1]
        custbalance=cust[2]
        
        print (f'Customer: {custfname} {custlname}, Funds: {custbalance}')
    else:
        print("No Customer Found")
        return

####### Get product info while processing a transation       #######################################################################

def getproductinfo(prodid):

    cursor.execute("SELECT productname, quantityinstock, price from product WHERE id=?", (prodid,))
    prod = cursor.fetchone()

    if prod is not None:
        prodname=prod[0]
        prodqty=prod[1]
        prodprice=prod[2]
        
        print (f'Product: {prodname} In Stock: {prodqty}, Price: {prodprice}')
    else:
        print("Product Not Found.")
        return 

####### Check the customer's bank balance           #######################################################################

def getcustomerbalance(id):
    mycursor = conn.cursor()
    mycursor.execute("SELECT accountbalance FROM person WHERE id =?", (id,))
    balance = mycursor.fetchone()[0]
    return balance






###################################################
####                             MAIN CODE SECTION ##########################################
###################################################

option = 0
print ('Select DB Action:')
option = input('1: Add Customer:\n2: Add Product\n3: Add Order:\n4: List Customers: \n5: List Products: ')
print (f'Selected Option: {option}\n')

while option != "q":

    if option == '1':

        fname = input('Enter Customer First Name: ')
        lname = input('Enter Customer Last Name: ')
        age = input('Customer Age: ')
        account = input('How much in customer account: ')
        
        addperson(fname, lname, age, account)
        option = input("Next Option? (q to Quit)")

    elif option == '2':

        fname = input('Enter Product Name: ')
        description = input('Enter Description: ')
        units = input('How Many Units?: ')
        price = input('Price: ')
        
        addproduct(fname, description, units, price)
        option = input("Next Option? (q to Quit)")
    
    elif option == '3':

        person = input("Customer ID: ")
        if getcustomerinfo(person) == "error":
            exit()

        product = input("Product ID: ")
        getproductinfo(product)
        qty = input("Quantity: ")

        addorder(person, product, qty)
        option = input("Next Option? (q to Quit)")

    elif option == '4':

        listcustomers()
        option = input("Next Option? (q to Quit)")

    elif option == '5':

        listproducts()
        option = input("Next Option? (q to Quit)")

    elif option == 'b':
        customer_id = input('Input Customer ID for balance: ')
        getcustomerbalance(customer_id)
    else:

        option = input("This Option Is Not Available at this Time. Please Make a Valid Selection or q to quit: ")


conn.commit()
conn.close()




