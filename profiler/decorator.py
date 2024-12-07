"""
File: Decorators - Convenient syntax for wrapping
 functionality around another function.
"""
import time

# Issue here is that the function f() cannot take in any parameters so very limited
def notify_proto(f):
    """Notify the user when they enter
    and exit the function"""
    def wrapper():
        print("Entering:", f.__name__)
        f()
        print("Exiting:", f.__name__)

    return wrapper

# More general decorator to account for limitation above
# Want this to have to ability to be applied to any function/parameters --> USE ARGS AND KWARGS
def notify(f):
    """Notify the user when they enter
    and exit the function"""
    def wrapper(*args, **kwargs):
        print("Entering:", f.__name__)
        result = f(*args, **kwargs)
        print("Exiting:", f.__name__)
        return result

    return wrapper

def do_twice(f):
    def wrapper(*args, **kwargs):
        val = f(*args, **kwargs)
        val = f(*args, **kwargs)
        return val
    return wrapper

def timer(f):
    """ Decorate a function f() with timing info
    and report the lapsed time at the end of the function call"""
    def wrapper(*args, **kwargs):
        start = time.time_ns()
        val = f(*args, **kwargs)
        end = time.time_ns()
        elapsed = end - start
        print("Elapsed Time (sec):", elapsed / 10**9)
        return val

    return wrapper

# Says we want to decorate this function with a notifier
@do_twice
@notify
# Order matters!
# if we reversed this, it would tell us that we ran thru hello world twice but only entered and exited once
def hello_world():
    print("Hello World!")

@timer
def add(x, y):
    return x, y, x + y

@timer
def squares(n):
    return [i**2 for i in range(n)]


def main():
    # No longer need these lines of code since we added decorator tag
    #new_hello_world = notify_proto(hello_world)
    #print(type(new_hello_world))
    #new_hello_world()

    rslt = squares(1000)[-10:-1]
    print(rslt)

    result = add(2, 3)
    print(result)
    hello_world()
if __name__ == '__main__':
    main()