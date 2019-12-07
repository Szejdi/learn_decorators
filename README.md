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


>>> help(foo)
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
## Lets do this again. But using class.
Let's comeback to the "first class object" meaning.
If functions are objects, we can use object instead of the function.
Lets try to translate following piece of code into class approach.

### From the beginning
Once more lets try to implement very simple decorator, which print
`__name__` attribute of original function.
```python
@mydecorator
def foo():
    ...
```
We know the actual call behind this. Just as reminder.
```python
def foo():
    ...
foo = mydecorator(foo)
```
Thinking about `mydecorator` as an object, we should implement the 
`__init__` method, which will take our original function.
```python
class MyDecorator:
    def __init__(self, func):
        ...
```
But to execute our new function, we have to use `()` syntax one more time.
Lets forget about the decorators and try to think what next code snippet
will exactly do
```python
class Baz:
    ...
b = Baz()
b()
```
It's pretty obvious that `b = Baz()` will invoke `__init__` function.
The second line `b()` will invoke `__call__` method.  
So the original function lands in `__init__` method and the actual execution
is done in `__call__`. In this case we need to assign the original function
to instance attribute, to be able to refer to it from the `__call__` method.
```python
class mydecorator:
    def __init__(self, func):
        self.func = func
    
    def __call__(self, *args, **kwargs):
        print(self.func.__name__)
        return self.func(*args, **kwargs)
```
### Lets improve! Parametrization.
Once again our goal is to parametrize our decorator.
Just to recall what we want to achieve, we want our decorator to print
all listed attributes in decorator argument.
```python
@mydecorator(['__name__', '__module__'])
def foo():
    ...
```
We know that this code is equal to:
```python
def foo():
    pass
mydecorator(['__name__', '__module__'])(foo)
```
So in this case the `['__name__', '__module__']` argument is going to
`__init__` method, and the `foo` function goes to the `__call__`.
Right now we are missing the way to pass original argument of the `foo` function.  
Executing our new function will be 3rd use of `()` on our object, so the
return value of the `__call__` should be `callable`! Lets then return a new function
declared inside of `__call__` method.
```python
class mydecorator:
    def __init__(self, attrs_to_print):
        self.attrs_to_print = attrs_to_print
    
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            for attr in self.attrs_to_print:
                print(getattr(func, attr, ''))
            return func(*args, **kwargs)
        return wrapper
```
And it's almost all.
### Hey you! You lost metadata again!
Unfortunately there are two separate approaches.
#### Unparameterized
In this case we need to use `functools.update_wrapper()` function, as there
is no wrapper function that we can wrap with `functools.wraps()` which we already
know.
```python
import functools


class mydecorator:
    def __init__(self, func):
        self.func = func    
        functools.update_wrapper(self, func)
    
    def __call__(self, *args, **kwargs):
        print(self.func.__name__)
        return self.func(*args, **kwargs)
```
#### Parametrized
This is easier one, we have the `wrapper()` function so we do it in old way,
using `@functools.wraps()` decorator on that.
```python
import functools


class mydecorator:
    def __init__(self, attrs_to_print):
        self.attrs_to_print = attrs_to_print
    
    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attr in self.attrs_to_print:
                print(getattr(func, attr, ''))
            return func(*args, **kwargs)
        return wrapper
```
### My IDE is screaming to me about PEP8 incompatibility!
The PEP8 requires that class names should be in CamelCase, but on the other
hand de decorators are usually in snake_case. How we can bring together those two
rules which are excluding themselves? Here is the trick:
```python
class MyDecorator:
    ...

my_decorator = MyDecorator
```
And the thing which you are actually importing to other files should be 
`my_decorator` variable

## Hmmm, that's nice, but I mostly use the OOP rather then pure functions.
And I am happy that you do! In this section we will talk about building decorators
for methods and even for the whole classes!
### How to decorate single method?
To decorate methods I'll use the class based approach.
Let's try to reuse on of our previous decorators. Lets start with the simple
one.  
Lets try to execute following piece of code:
```python
import functools


class mydecorator:
    def __init__(self, func):
        self.func = func    
        functools.update_wrapper(self, func)
    
    def __call__(self, *args, **kwargs):
        print(self.func.__name__)
        return self.func(*args, **kwargs)


class Foo:
    @mydecorator
    def baz(self):
        print('Hallo folks.')

foo = Foo()
foo.baz()
```
This will raise an error.
```
TypeError: baz() missing 1 required positional argument: 'self'
```
So we've missed the `self` argument... That's pretty bad.  
But of course there is a cure for that and it's name is... Descriptor.
Descriptors are special objects which have to implement 3 methods:
* `__get__`
* `__set__`
* `__delete__`

Those objects are defining the dot `.` operator behaviour.  
Lets see when particular method will be called:
* `__get__`: `foo.baz()`
* `__set__`: `foo.baz = 5`
* `__delete__`: `del foo.baz`

In context of decorators we should be interested only in `__get__` method,
because it's the one that get invoked on actual method call.  
The signature of this method is following: `__get__(self, obj, objtype)`, where `obj`
