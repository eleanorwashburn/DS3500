"""
Demo of static methods and class variables
"""

class Calculator:

    # Shared class variable
    allocated = 0

    def __init__(self, name):
        self.name = name
        Calculator.allocated += 1

    # Says no longer need to call 'self' in this function
    @staticmethod
    def add(x, y):
        return x + y

def main():
    c1 = Calculator("calcy the calculator")
    # Call method of object that doesnt require a state reference at all
    # Need to declare this method as a static method
    result = c1.add(2, 3)
    print(result)

    result2 = Calculator.add(3,4)
    print(result2)

    c2 = Calculator("hp 41cv")

    c3 = Calculator("TI 30")

    print("# of calculators:", Calculator.allocated)
    print(c1.allocated, c2.allocated, c3.allocated)

    Calculator.allocated = 99
    print(c1.allocated, c2.allocated, c3.allocated)

# State variables are unique to each object instance of the classes
# Class variables are is same for all variables across all instances

if __name__ == '__main__':
    main()