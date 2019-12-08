import types
import functools


class mydecorator:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print(self.func.__name__)
        return self.func(*args, **kwargs)

    def __get__(self, instance, owner):
        return functools.partial(self, instance)


class MyClassDecorator:
    class DecoratedClass:
        def __init__(self, Klass, *args, **kwargs):
            self.original_instance = Klass(*args, **kwargs)

        def __getattribute__(self, item):
            try:
                return super().__getattribute__(item)
            except AttributeError:
                original_attr = self.original_instance.__getattribute__(item)
                if isinstance(original_attr, types.MethodType):
                    return mydecorator(original_attr)
                return original_attr

    def __init__(self, Klass):
        self.Klass = Klass
        functools.update_wrapper(self.DecoratedClass, Klass)

    def __call__(self, *args, **kwargs):
        return self.DecoratedClass(self.Klass, *args, **kwargs)