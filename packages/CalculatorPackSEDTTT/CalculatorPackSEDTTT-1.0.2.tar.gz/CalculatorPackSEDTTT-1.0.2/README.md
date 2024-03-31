# Python Package Exercise
[![log github events](https://github.com/software-students-spring2024/3-python-package-exercise-team-dtttt/actions/workflows/event-logger.yml/badge.svg)](https://github.com/software-students-spring2024/3-python-package-exercise-team-dtttt/actions/workflows/event-logger.yml)


## Team members

Deniz Qian: https://github.com/dq2024 \
Somyung Kim: https://github.com/troy-skim \
Terrance Chen: https://github.com/tchen0125 \
Kim Young: https://github.com/Kyoung655

## Project Description

This project is a calculator app that is able to execute multiple functions. The availible 
functions are add, subtract, multiply, divide, mod, log, exp, randomnumsrange, stringParse,
abs, factorial, mean, median, and mode. 

## Project Instructions 

### Pipenv Installation:
Ensure pipenv is installed:
if not:
'''
pip install pipenv
'''


### Integration of project into your existing code 

If you want to integrate our project code into your code, you can do so by...

#### Installation

You can install calculator project by using pip:

'''
pipenv install CalculatorPackSEDTTT==2.0
'''

Install Dependecies if needed:
'''
pipenv install
'''

#### Usage
To use it in your code, please import functions needed
'''
from calc import add, subtract, multiply, divide, mod, stringParse, log, exp, abs, factorial, mean, median, mode, randomnumsrange, cubesurfacearea
'''

Below is documentation for methods to be used in code


#### Documentation of out project's functions 

Our project has the following functions:
**add(x,y)**: this functions takes two numbers, adds them together, then returns their sum. 
This function is **only** to be used within the stringParse() function. Example here:

**substract(x,y)**: this functions takes two numbers, subtracts them from eachother, then returns their difference. This function is **only** to be used within the stringParse() function. Example here:

**multiply(x,y)**: this functions takes two numbers, multiplies them together, then returns their product. 
This function is **only** to be used within the stringParse() function. Example here:

**divide(x,y)**: this functions takes two numbers, divides them by eachother, then returns their quotient. 
This function is **only** to be used within the stringParse() function. Example here:

**mod(x,y)**: this functions takes two numbers, calls the modulus operator, then returns the remainder. 
This function is **only** to be used within the stringParse() function. Example here:

**log(x,y)**: this functions takes two numbers, adds them together, then returns the natural logarithm. 
This function is **only** to be used within the stringParse() function. Example here:

**exp(x,y)**: this functions takes two numbers. x is multiplied by itself y times. The code then returns the product. This function is **only** to be used within the stringParse() function. Example here:

**randomnumsrange(x,y)**: this functions takes two numbers. random numbers are generated in between 0 and x, y times. The code then returns the list of random number generated. This function is **only** to be used within the stringParse() function. Example here:

**stringParse(input)**: this function takes two numbers and any of the following functions previously
mentioned: add, subtract, multiply, divide, mod, log, exp, and randomnumsrange. The format for stringParse(input)
must be stringParse("number1 operation number2"). Examples here: 

**abs(x)**: this function takes a single number and converts it into its absolute value. Example here:

**factorial(x, val = {})**: this function takes in a number and returns its factorial value. Example here: 

**mean(list)**: this function takes in a list of numbers, sums them up, then divides them by the number
of numbers in the array, returning the average. Example here: 

**median(list)**: this function takes in a list of numbers, ordering the data points, and then finding the midddle number or taking the mean of the middle two numbers. Example here: 

**mode(numbers)**: this function takes in a list of numbers and returns the number that appears most 
often. Example here: 

**cubesurfacearea(x)**: this function takes in a number, calls our exp function with x, then multiplies the value 
returned by our exp function by 6 to get the surface area of a cube. 


#### Example Usage
Please look at [example.py](example.py)



### Contribution

#### Create a fork then clone:
'''
git clone https://github.com/software-students-spring2024/3-python-package-exercise-team-dtttt.git
'''

Ensure pipenv is installed according to above instructions

#### Start Virtual Environment:
'''
pipenv shell
'''

#### Dependecies:
'''
pipenv install
'''
#### Build
Ensure Build is installed if not:
'''
pipenv install build
'''

Run:
'''
python -m build
'''
on Windows
 
'''
python3 -m build
'''
on Mac

#### Running Tests
'''
pytest
'''

pytest will run the tests you can add more to tests under [tests](tests/test_Basics.py)

To modify functions in calculator please view calc folder with [calculator.py](calc/calculator.py)

#### Commit 
Please commit to a feature branch and submit a merge request for any edits

## Link to Project on PyPI Website 
(PyPI)[https://pypi.org/project/CalculatorPackSEDTTT/1.0.2/]