# Simple Interactive Calculator
# Built with basic logic: no functions, no imports

print("--- STANDOUT PYTHON CALCULATOR ---")
print("Available operations: +, -, *, /, %, **")
print("Type 'exit' to quit the program.")

# Variable to store the memory of the last result
last_result = None

while True:
    print("\n----------------------------------")
    if last_result is not None:
        print("Last Result: " + str(last_result))
    
    user_input = input("Enter operation (e.g., 5 + 10) or 'exit': ")
    
    if user_input.lower() == 'exit':
        print("Goodbye!")
        break
    
    # Simple parsing: splits input by spaces
    parts = user_input.split()
    
    if len(parts) != 3:
        print("Error: Invalid format. Please use 'number operator number' (e.g., 10 + 5)")
        continue
        
    num1 = float(parts[0])
    operator = parts[1]
    num2 = float(parts[2])
    
    # Logic for calculations
    result = 0.0
    valid = True
    
    if operator == '+':
        result = num1 + num2
    elif operator == '-':
        result = num1 - num2
    elif operator == '*':
        result = num1 * num2
    elif operator == '/':
        if num2 == 0:
            print("Error: Cannot divide by zero!")
            valid = False
        else:
            result = num1 / num2
    elif operator == '%':
        result = num1 % num2
    elif operator == '**':
        result = num1 ** num2
    else:
        print("Error: Unknown operator " + operator)
        valid = False
        
    if valid:
        print("Result: " + str(result))
        last_result = result