import math
import random

# user welcome prompt and instruction 
# with open("calc_instructions.txt") as f:
#     for line in f:
#         #do something with line
#         print(line)

# stringParse() start 
def stringParse(input):
    # no  parentheses, operator precedence, or numbers without spaces around the operators

    """splits by spaces so if there's no spaces or
    there are non-space characters where the spaces are supposed to be then the input
    string cant be split and is treated as one giant string, thus throwing an error """
    parsed_string = str(input).split(' ')

    if len(parsed_string) != 3:
        print(len(parsed_string))
        raise ValueError("Input should be in the format: 'number1 operation number2'")

    xTr, operator, yTr = parsed_string
    x = float(xTr)
    y = float(yTr)

    if operator == '+':
        return add(x, y)
    elif operator == '-':
        return subtract(x, y)
    elif operator == '*':
        return multiply(x, y)
    elif operator == '/':
        return divide(x, y)
    elif operator.lower() == 'mod':
        return mod(x, y)
    elif operator.lower() == 'log':
        return log(x, y)
    elif operator.lower() == 'exp':
        return exp(x, y)
    elif operator.lower() == 'abs': 
        return abs(x, y)
    elif operator.lower() == 'factorial':
        return factorial(x, y)
    elif operator.lower() == 'mean':
        return mean(x, y)
    elif operator.lower() == 'median':
        return median(x, y)
    elif operator.lower() == 'mode':
        return mode(x, y)
    elif operator.lower() == 'randomnumsrange':
        return randomnumsrange(x, y)
    elif operator.lower() == 'cubesurfacearea':
        return cubesurfacearea(x, y)
    else:
        print(operator.lower())
        raise ValueError(f"Unsupported operation: {operator}")

# stringParse() end 


# functions area start
def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        raise ValueError("Cannot divide by zero.")
    return x / y

def mod(x, y):
    if y == 0:
        raise ValueError("Cannot mod by zero.")
    return x % y

def log(x,y):
    # value x, base y, works only for int results
    if y == 1 or x <= 0 or y <= 0:
        raise ValueError("x, y must be positive, y shouldn't be 1")
    return round(math.log(x,y))

def exp(x, y):
    if y < 0:
        x = 1/x
        y = -y
    res = 1
    if (x < 0 and y == 0) or (x == 0 and y < 0):
        res = -1

    for i in range(int(y)):
        res *= x
    return res

def abs(x):
    if x < 0:
        x = -x
    return x

def factorial(x, val = {}):
    if x < 0:
        raise ValueError("x must be positive")
    if x in val:
        return val[x]
    if x == 0:
        val[x] = 1
        return 1
    val[x] = x*factorial(x-1, val)
    return val[x]

def mean(list):
    return sum(list) / len(list)

def median(list):
    list.sort()
    n = len(list)
    mid = n // 2
    if n % 2 == 0:  
        return (list[mid - 1] + list[mid]) / 2.0
    else:  
        return list[mid]

def mode(numbers):
    if len(numbers) == 1:
        return numbers  
    frequency = {}
    for number in numbers:
        frequency[number] = frequency.get(number, 0) + 1
    max_freq = max(frequency.values())
    modes = [key for key, val in frequency.items() if val == max_freq]
    if len(modes) == len(numbers):
        return "No mode" 
    return modes

def randomnumsrange(x, y):
    num1 = int(x)
    num2 = int(y)
    if (num1 < 0 or num2 < 0):
        raise ValueError("number1 and number2 muust both be greater than or equal to zero.")

    else:
        random_nums = []
        for i in range(num2):
            random_num = random.randint(0, num1)
            random_nums.append(random_num)
    # print(f'You have chosen to generate random numbers in between 0 and {num1}, {num2} times:\n{random_nums}')
    return random_nums

def cubesurfacearea (x):
    # x = surface area, length of the side of the cube 
    if (x <= 0):
        raise ValueError("number1 and number2 muust both be greater than zero.")
    return 6 * (exp(x, x))



# functions area end 

