def add_numbers(a, b):
    sum_value = a + b
    return sum_value

def multiply_numbers(a, b):
    product = 0
    for _ in range(b):  # Inefficient multiplication using a loop
        product += a
    return product

num1 = int(input("Enter first number: "))
num2 = int(input("Enter second number: "))

sum_result = add_numbers(num1, num2)
product_result = multiply_numbers(num1, num2)

print("Sum is: " + str(sum_result))
print("Product is: " + str(product_result))
