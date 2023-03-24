## PyBT

`PyBT` is a library for property based testing in python. Here is an example: 

```python
from pybt.core.core import pybt


def rev(l):
    return l[::-1]


@pybt
def test_rev(l: list[str | int | bool | list[bool | str | list[str]  | list[dict[str, list[dict[str,str]]]]]]):
    assert rev(rev(l)) == l
```

Here, we test a function called `rev`, using a "universally quantified proposition" which is expressed as a function. 

```Adga
∀ l, rev(rev(l)) = l 
```

`PyBT` will automatically generate inputs based on the type of `rev`'s arguments, and any hypotheses provided by the user. 


## Using PyBT for coercion checking

Here is another test for a function named `factorial`. Here, we assert that passing a string to our function 
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
