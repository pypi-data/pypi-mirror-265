import contextlib


def suppress_exceptions(*exceptions):
    def outer_func(func):
        def inner_func(*args, **kwargs):
            with contextlib.suppress(*exceptions):
                return func(*args, **kwargs)

        return inner_func

    return outer_func
