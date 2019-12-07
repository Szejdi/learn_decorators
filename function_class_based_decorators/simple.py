class simple_class_based_decorator:

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print(f'Executing {self.func.__name__}')
        return self.func(*args, **kwargs)
