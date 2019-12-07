class MethodDecorator:

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print(self.func.__name__)
        return self.func(*args, **kwargs)


method_decorator = MethodDecorator

