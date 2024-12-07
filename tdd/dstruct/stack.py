"""
File: stack.py

An object-oriented implementation of a STACK
with support for push and pop operations.

"""
class Stack:

    def __init__(self):
        """ Stack constructor """
        self.items = []  # stack is implemented as a list
                         # with TOP element on the right (last)

    def size(self):
        """ # of elements in the stack """
        return len(self.items)

    def top(self):
        """ Return the top element from the stack
        return - Top element, or None if stack is empty """

        if self.size() == 0:
            return None
        else:
            return self.items[-1]

    def push(self, x):
        """ Push element x onto the stack """
        self.items.append(x)

    def pop(self):
        """ Return the top element off of the stack """
        try:
            x = self.items.pop()
            return x

        except Exception:
            return None



