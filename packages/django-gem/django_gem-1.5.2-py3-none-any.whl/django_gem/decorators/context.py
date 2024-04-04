from django_gem.context.cutting_always_eager import CuttingAlwaysEager
from django_gem.context.override_anvil import OverrideAnvil


def cutting_always_eager(func):
    def inner_func(*args, **kwargs):
        with CuttingAlwaysEager():
            return func(*args, **kwargs)

    return inner_func


def override_anvil(anvil):
    def outer_func(func):
        def inner_func(*args, **kwargs):
            with OverrideAnvil(anvil=anvil):
                return func(*args, **kwargs)

        return inner_func

    return outer_func
