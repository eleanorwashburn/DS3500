print(1, 2, 3, 4, 5, "hello", True, [1, 2, 3])

def add(x, y, *args, msg="hello", **kwargs):
    print(x, y, args, msg, kwargs)
    print(type(args))
    print(type(kwargs))

    print(msg, "John")

    total = x + y
    for z in args:
        total += z
    return total

print(add(3, 5,2, 3, 7, -1, 6, 7, 8, msg="Hey", foo="bar", z=42, is_this_fun=True))

#args
#a catch-all for positional parameters --> here it is 2, 3, 7, -1, 6, 7, 8 in the final print statement
#in this example it is x + y + any other positional parameters (args --> a tuple)
#args does not have to be called args it just needs the *

#kwargs
#example code--> def make_sankey(df, src, targ, cals=None, pad=50, thickness=100)
#In sankey code, if we do this then it becomes very cumbersome
#this is where we use kwargs (key word arguments) and indicated by **, kwargs is a dictionary
#here it is foo="bar", z=42, is_this_fun=True in the final print statement
#catch-all for additional named parameters, there is now an example in sankey.py

#args vs kwargs
#args = catch-all for positional parameters (parameters receive values in order of the parameters listed)
#allows you not have to specify things like x =___ or y =___
#example: x = 3 and y = 4... x-y = -1 and if you switch x and y values then you will get 1
#args received as a tuple
#kwargs = catch-all for unlimited number of named parameters
#recieved as a dictionary
