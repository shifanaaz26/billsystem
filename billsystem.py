
# Shopping Bill with Discount

print("===== SHOPPING BILL =====")

# Get customer details
customer = input("Enter customer name: ")

# Get product details
product = input("Enter product name: ")
quantity = int(input("Enter quantity: "))
price = float(input("Enter price per item: "))

# Calculate total amount
total = quantity * price

# Calculate discount
if total >= 5000:
    discount = total * 0.20
elif total >= 3000:
    discount = total * 0.15
elif total >= 1000:
    discount = total * 0.10
else:
    discount = 0

# Calculate final amount
final_amount = total - discount

# Display shopping bill
print("\n======= FINAL BILL =======")
print("Customer Name :", customer)
print("Product Name  :", product)
print("Quantity      :", quantity)
print("Price         : Rs.", price)
print("Total Amount  : Rs.", total)
print("Discount      : Rs.", discount)
print("--------------------------")
print("Final Amount  : Rs.", final_amount)
print("==========================")
