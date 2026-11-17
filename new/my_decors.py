def hello_decorator(func):
    def inner():
        print("Hello, this is before function execution")
        # calling the actual function now inside the wrapper function
        func()

        print("Bye. This is after function execution")

    return inner
