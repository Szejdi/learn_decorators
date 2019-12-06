import functools


def decorator_with_metadata(func: callable) -> callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(func.__name__)
        return func(*args, **kwargs)
    return wrapper