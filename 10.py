def repeat(num_times):
    def decoratorRepeat(func):
        def wrapperRepeat(*args, **kwargs):
            for _ in range(num_times):
                value = func(*args, **kwargs)
            return value
        return wrapperRepeat
    return decoratorRepeat

# @repeat(4)
# def greet(name):
#     print(f"Hello {name}")
#
# greet("Alexander")

# @repeat(6)
# def factorial(num):
#     cnt = 1
#     for i in range(1,num+1):
#         cnt = cnt * i
#     print(cnt)
# factorial(5)

# @repeat(5)
# def sum2(x, y):
#     print(x+y)
# sum2(3, 4)

import tracemalloc

def measure_memory_usage(func):
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        # Call the original function
        result = func(*args, **kwargs)

        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics("lineno")

        print(f"Memory usage of {func.__name__}:")
        for stat in top_stats[:3]:
            print(stat)
        return result
    return wrapper

# @measure_memory_usage
# def create_list(l):
#     ls = [i**2 for i in range(l)]
#     return ls
# create_list(10)

# @measure_memory_usage
# def factorial(num):
#     cnt = 1
#     for i in range(1,num+1):
#         cnt = cnt * i
#     return cnt
# # factorial(14)
#
# @measure_memory_usage
# def factorial2(n):
#     if n == 0:
#         return 1
#     else:
#         return n * factorial2(n-1)

# print(factorial2(14))
# print(factorial(14))

# def cache_result(func):
#     cache = {}
#
#     def wrapper(*args, **kwargs):
#         key = (*args, *kwargs.items())
#
#         if key in cache:
#             print("Retrieving result from cache...")
#             return cache[key]
#
#         result = func(*args, **kwargs)
#         cache[key] = result
#         return result
#     return wrapper
# @cache_result
# def mul(x, y):
#     print("Calculating the product of two numbers...")
#     return x*y
#
# print(mul(4, 5))
# print(mul(3, 5))
# print(mul(4, 3))
# print(mul(4, 5))
# print(mul(4, 3))


# def decorator(func):
#     def wrap(*args, **kwargs):
#         # Log the function name and an argument
#         print(f"Calling {func.__name__} with args: {args}, kwargs: {kwargs}")
#
#         # Call the original function
#         result = func(*args, **kwargs)
#
#         # Log the return value
#         print(f"{func.__name__} returned: {result}")
#
#         # Return the result
#         return result
#     return wrap

# @decorator
# def multiply_numbers(x, y):
#     return x*y
# print(multiply_numbers(4, 6))

# @decorator
# def personal_info(*args, **kwargs):
#     return *args, *kwargs, *kwargs.values()
#
# y = personal_info("John", "Jack", "mary", surname="Connor", age= 17)
# print(*y, end="\n" "hello world!")


from time import time

def measure_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time()
        result = func(*args, **kwargs)
        end_time = time()
        execution_time = end_time - start_time
        print(f"Function {func.__name__} took {execution_time:.4f} seconds to execute")
        return result
    return wrapper

# @measure_execution_time
# def calculate_multiply(numbers):
#     total = 1
#     for x in numbers:
#         total *= x
#     return total
# lst = [i**2 for i in range(1, 10)]
# result = float(calculate_multiply(lst))
# print("Result:",result)

num = 66000
lst = [1, 1]
@measure_execution_time
def fibo(x):
    for i in range(2, x):
        lst.append(lst[i-2] + lst[i-1])

    return lst[x-1]

fibo(num)