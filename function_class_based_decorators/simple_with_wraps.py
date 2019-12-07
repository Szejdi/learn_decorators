import functools


class mydecorator:
    def __init__(self, func):
        self.func = func
        functools.update_wrapper(self, func)

    def __call__(self, *args, **kwargs):
        print(self.func.__name__)
        return self.func(*args, **kwargs)