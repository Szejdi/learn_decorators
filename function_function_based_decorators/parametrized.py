def parametrized_decorator(func: callable) -> callable:
    def wrapper(attrs_to_print):
        def wrapped(*args, **kwargs):
            for attr in attrs_to_print:
                print(getattr(func, attr, ''))
            return func(*args, **kwargs)
        return wrapped
    return wrapper
