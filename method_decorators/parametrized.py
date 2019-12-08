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

    def __get__(self, instance, owner):
        return functools.partial(self, instance)