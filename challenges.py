'''products = [
    {"item": "laptop", "price": 75000},
    {"item": "pen", "price": 20},
    {"item": "phone", "price": 15000}
]

def check_status(product):
    if product['price'] > 50000:
        status = "Expensive"
    elif product['price'] > 1000:
        status = "Moderate"
    else:
        status = "Cheap"
    print(f"Product: {product['item']} | Price: ₹{product['price']} | Status: {status}")

for product in products:
    check_status(product)

attempts = 3
password = "artik123"

while True:
    if attempts == 0:
        print("Account locked. Contact support.")
        break
    
    user_input = input("Enter the password: ").strip()
    
    if user_input == password:
        print("Naveen logged in successfully")
        break
    else:
        attempts = attempts - 1
        print(f"Invalid password. {attempts} attempts remaining")

        '''

customers = [
    {"name": "Naveen", "items": [150, 200, 100]},
    {"name": "Abi", "items": []},
    {"name": "Rex", "items": [500, 400, 300]}
]

for customer in customers:
    total = sum(customer['items'])
    if total > 0 :
        result = "Thank you for shopping"
    else :
        result = "Your cart is empty"
    print(f"{customer['name']} - Total {total} {result}")
