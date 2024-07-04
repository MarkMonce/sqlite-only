import sqlite3

def addorder(person_id, product_id, quantity):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    
    try:
        # Check available quantity in stock
        cursor.execute("SELECT quantityinstock FROM product WHERE id = ?", (product_id,))
        availableqty = cursor.fetchone()[0]
        
        quantity = int(quantity)
        availableqty = int(availableqty)
        
        # Calculate the total cost of the order and check product availability
        cursor.execute("SELECT price FROM product WHERE id = ?", (product_id,))
        product_price = cursor.fetchone()[0]
        total_cost = product_price * float(quantity)
        
        # Check if sufficient quantity is available
        if quantity <= availableqty:
            print(f'The quantity available {availableqty} is sufficient to fulfill the quantity ordered: {quantity}')
        else:
            print(f'The quantity available {availableqty} is NOT sufficient to fulfill the quantity ordered: {quantity}\nEither reduce the quantity or select another product.')
            return
        
        # Check if the customer has sufficient funds to complete the order
        cursor.execute("SELECT accountbalance FROM person WHERE id = ?", (person_id,))
        customer = cursor.fetchone()
        
        if customer is None:
            print(f'No customer found with ID {person_id}')
            return
        
        customer_balance = customer[0]
        
        if customer_balance < total_cost:
            print(f'The customer does not have sufficient funds. Available balance: ${customer_balance}, total cost: ${total_cost}.')
            return
        else:
            print(f'Transaction for ${total_cost} approved. Cost will be deducted from customer balance of ${customer_balance}')
        
        # Update the stock and customer balance
        new_qty = availableqty - quantity
        cursor.execute("UPDATE product SET quantityinstock = ? WHERE id = ?", (new_qty, product_id))
        
        new_balance = customer_balance - total_cost
        cursor.execute("UPDATE person SET accountbalance = ? WHERE id = ?", (new_balance, person_id))
        
        # Insert the order into the orders table
        transaction_date = datetime.now().strftime('%Y-%m-%d')
        cursor.execute(
            "INSERT INTO orders (transaction_date, person_id, product_id, quantity, total_cost) VALUES (?, ?, ?, ?, ?)",
            (transaction_date, person_id, product_id, quantity, total_cost)
        )
        
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

# Example usage
person_id = 1  # Example person ID
product_id = 1  # Example product ID
quantity = 1  # Example quantity

addorder(person_id, product_id, quantity)
