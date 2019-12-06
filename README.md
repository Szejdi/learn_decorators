# Decorators
TODO: Write something here.
## Unraveling decorators darkest secret.
You've probably encountered similar piece of code in the past.
Usually we use built-in decorators and we don't spend much time
thinking how they works and what they are.  

```python
@decorator
def foo():
    pass
```

But what this syntax really means?  
It's equivalent to below piece of code.  
```python
def foo():
    pass
foo = decorator(foo)
```
In python functions are first class objects, it's mean, that those
can be referenced and passed to other function like other arguments,
which is mandatory for above construction.

So know, where we know, that decorators are not something magic,
that is just a syntax sugar, we can start to build over own!
  
## My very first decorator.
Building our first decorator we encounter 2 other approaches.
* Function Based Decorators
* Class Based Decorators 
 
For the first time, I'd recommend using first approach, which uses
function. It's a bit easier to do and don't introduce that much 
confusion on the beginning.

For this example we will build the decorator, 
which on function execution will print its name.

So for now we know 2 things
* Our decorator will be a function
* Our decorator has take another function as argument.

So lets start!
### Simple decorator
```python
def my_decorator(func: callable):
    ...
```
Okey, but what it should return? We always still can call decorated 
function, so `callable` sounds like a good idea!
```python
def my_decorator(func: callable) -> callable:
    ...
```
Hm, so we have to return a function, but where we can get one?  
Here is a moment when we have to use another advantage of 
functions being object, that we can create them inside other.  
We will call it `wrapper` as it will just wrap our function.  
We also know that it should print the function name 
and execute the original function logic.  
We want to return that wrapper, as our new function.
```python
def mydecorator(func: callable) -> callable:
    def wrapper(*args, **kwargs):
        print(func.__name__)
        return func(*args, **kwargs)
    return wrapper
```
So what happened here?
We've created an internal function `wrapper`:
* It takes *args *kwargs as parameters. 
    Those will be passed to our original function.
* `print()` statement is executing our additional logic, 
    which we wanted to implement.
* In last line we are returning actual call of original function.  

At the end of our whole decorator we are returning our `wrapper`
function as the new one!  
Execution will look like this:
```python
@mydecorator
def foo():
    print('I am real body of foo!')


>>> foo()
'foo'
'I am real body of foo!'
```
### How we can improve?
Lets say that the name of function in our case is not enough.
Moreover for different function we want to print other
attributes of different functions.
We can accomplish this challenge by parametrizing our decorator.  
Expected usage:
```python
@mydecorator(['__name__', '__module__'])
def foo():
    ...
```
Problem is that we change semantic of our code.
This call is equal to the following: 2
```python
mydecorator(['__name__', '__module__'])(foo)
```
And this is the place where things are starting to be more complex.
We just called our decorator twice!  
The solution to this case is pretty obvious, we need another function.  
Lets take our decorator and try to improve it.
```python
def mydecorator(func: callable) -> callable:
    def wrapper(attrs_to_print):
        def wrapped(*args, **kwargs):
            for attr in attrs_to_print:
                print(getattr(func, attr, ''))
            return func(*args, **kwargs)
        return wrapped
    return wrapper
```
Hm, so we have one more nested function `wrapped`.
Here is what we've done:
* We create another function, called wrapped and shifted
decorator logic there modyfing it to iterate through
arguments and print them.
* Function `wrapper` is now taking parameters for decorator.
* `*args, **kwargs` where shifted to `wrapped` function.
### What did we missed?
Building our decorators, we've forgot about 1 thing.
Maybe not crucial, but still very helpful - original function metadata.  
What does it mean? For example type hints and docstring 
and other attributes of original function
```python
def mydecorator(func: callable) -> callable:
    def wrapper(*args, **kwargs):
        print(func.__name__)
        return func(*args, **kwargs)
    return wrapper

@mydecorator
def foo():
    """It's a foo function that basically does nothing."""
    print('I am real body of foo!')


>> help(foo)
Help on function wrapper in module __main__:

wrapper(*args, **kwargs)
``` 
So we can see that there is no docstring anymore, 
which should be revealed by `help` function.  
No worries. there is a solution for that problem too.
It comes from `functools` module and it's a... DECORATOR! 
(Yes you might experience some kind of inception here).  
To fix our code we need to decorate (xD) our wrapper function
with `@functools.wraps(func)` where we pass original function.
```python
import functools
def mydecorator(func: callable) -> callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(func.__name__)
        return func(*args, **kwargs)
    return wrapper
```
