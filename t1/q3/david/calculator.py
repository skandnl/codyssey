# david/calculator.py

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Error: Division by zero."
    return a / b

if __name__ == "__main__":
    try:
        a = int(input("Enter first number: "))
    except ValueError:
        print("Invalid input. Please enter an integer.")
        exit()

    try:
        b = int(input("Enter second number: "))
    except ValueError:
        print("Invalid input. Please enter an integer.")
        exit()

    operator = input("Enter operator (+, -, *, /): ")

    if operator == "+":
        result = add(a, b)
    elif operator == "-":
        result = subtract(a, b)
    elif operator == "*":
        result = multiply(a, b)
    elif operator == "/":
        result = divide(a, b)
    else:
        result = "Invalid operator."

    print(f"Result: {result}")



def add(a,b):
    return a+b
def minus(a,b):
    return a-b
def gop(a,b):
    return a*b
def nanu(a,b):
    if b == 0
        print("ZeroDivisonErro")
        return None
    return a/b


if __name__ =="__main__"
    try a=int(input("Enter the first Number:").split)
    b=int(input("Enter the secound Numbrt:").split)
    op=input("Enter the operater:").split

        if op=+
        if op=-
        if op=/
        if op=*