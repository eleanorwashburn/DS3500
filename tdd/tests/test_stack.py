import pytest
from dstruct.stack import Stack

# Fixtures are required when tests take parameters
# This fixutre injects an empty stack into the "s"
# parameter of certain unit tests that use "s" as a parameter.

@pytest.fixture
def s():
    s = Stack()
    return s

# in TDD, we typically try to write our tests FIRST
def test_constructor():

    s = Stack()
    assert isinstance(s, Stack), "Did not construct a stack"
    assert s.size() == 0, "Stack should be empty"

def test_top(s):
    assert s.top() is None, "Stack should be empty"
    s.push("x")
    s.push("y")
    assert s.top() == "y", "Expected top value to be y"
    assert s.top() == "y", "Expected top value to still be y"

def test_push(s):
    """ Unit test for the push method on a stack """
    s.push(3)
    assert s.size() == 1, "Expected size to be 1"
    assert s.top() == 3, "Expected top element to be 3"

    s.push(5)
    assert s.size() == 2, "Expected size to be 2"
    assert s.top() == 5, "Expected top element to be 5"

def test_pop(s):
    """ Unit test for the pop method """
    s.push("a")
    s.push("b")

    assert s.pop() == "b", "Wrong value popped, expected 'b'"
    assert s.pop() == "a", "Wrong value popped, expected 'a'"
    assert s.pop() is None, "Expected None to be returned from empty stack"


