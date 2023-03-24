## PyBT

`PyBT` is a library for property based testing in python. Here is an example: 

```python
from pybt.core.core import pybt


def factorial(x):
    # a function that computes the factorial of some integer x 
    fac = 1
    for i in range(1, x + 1):
        fac = fac * i
    return fac


@pybt(hypotheses={"x": lambda x: 1 <= x <= 100})
def test_factorial(x: int):
    # the test case of factorial - factorial should always meet this requirement
    a = factorial(x)
    pred = factorial(x - 1)
    assert(a == x * pred)


# call the test case - pybt will generate 1000 test cases for factorial
test_factorial()
```

Here, we test a function called `factorial`, using a "universally quantified proposition" which is expressed as a function. 

```Coq
∀ x, 1 ≤ x ≤ 100, factorial(x) == x * factorial(x - 1)
```

`PyBT` will automatically generate inputs based on the type of `factorial`'s arguments, and any hypotheses provided by the user. 

## Using PyBT for coercion checking

Here is another test for our `factorial` function. Here, we assert that passing a string to our function 
throws a type error. This can be useful if you want to make sure that arguments will not be automagically 
coerced by python and give some non-sensical output. 
```python
from unittest import TestCase


@pybt 
def test_factorial_coerce(x : str):
    test_case = TestCase()
    with test_case.assertRaises(Exception) as context:
        factorial(x)
    
    assert(context.exception is not None)
```
