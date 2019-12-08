from functools import partial


class MethodDecorator:

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print(self.func.__name__)
        return self.func(*args, **kwargs)

    def __get__(self, instance, owner):
        print(instance, owner)
        return partial(self.func, instance)


method_decorator = MethodDecorator

