# lst = []
# for i in range(10000):
#     lst.append(i)
#
# for j in range(10000):
#     lst.append(j)
#
# lst2 = []
# for i in range(10000):
#     for j in range(10000):
#         lst2.append(j)
#
#
# print(len(lst))
# print(len(lst2))

# Decorators

# Abilities of functions in Python

# Example 1: Treating functions as objects

# def shout(text):
#     return text.upper()
#
# print(shout("hello"))
# yell = shout
# print(yell("kuku"))
# print(yell is shout)

# Example 2: Passing the function as an argument

# def shout(text):
#     return text.upper()
#
# def whisper(text):
#     return text.lower()
#
# def sep(text):
#     return text.split()
#
# def greet(func):
#     greeting = func("Hi. I am created by a function passed as an argument")
#     print(greeting)
#
# greet(shout)
# greet(whisper)
# greet(sep)

# Example 3: Returning functions from another function

# def create_adder(x):
#     def adder(y):
#         return x + y
#
#     return adder
#
# add_15 = create_adder(15)
#
# # print(type(add_15))
#
# print(add_15(10))

# def func():
#     print("How are you?")
#
# func()

# def myDecorator(fn):
#     def inner_function():
#         # print("It is before my function")
#         fn()
#         print("How are you?")
#
#     return inner_function
#
# @myDecorator
# def greet():
#     print("Hello! ", end="")

# greet = myDecorator(greet)

# greet()

# from new.my_decors import *
#
# # define the function to be called inside wrapper
# @hello_decorator
# def functionToBeUsed():
#     print("This is inside the function")


# functionToBeUsed = hello_decorator(functionToBeUsed)

# functionToBeUsed()

# def hello_decorator(func):
#
#     def inner_service():
#         a = 5 + 8
#         print(a)



#     def inner(*args, **kwargs):
#         print("Before execution")
#
#         # getting the returned value
#         returned_value = func(*args, **kwargs)
#
#         print("After execution")
#
#         # returning the value to the original frame
#         return returned_value
#
#     return inner
#
#
# @hello_decorator
# def sum_two_numbers(a, b):
#     print("Inside the function")
#     return a + b
#
# print("Sum = ", sum_two_numbers(2, 3))


# chaining decorators

def quad(func):
    def inner():
        x = func()
        return x * x
    return inner

def mul2(func):
    def inner():
        x = func()
        return 2 * x
    return inner

@quad
@mul2
def num1():
    return 10

# @mul2
# @mul2
# @quad
def num2():
    return 10

print(mul2(quad(num2))())

print(num1())
print(num2())