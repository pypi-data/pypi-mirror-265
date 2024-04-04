from django.db import transaction


def conditional_transaction(func):
    def inner_func(*args, **kwargs):
        from django_gem.toolkit import gem_settings

        if not gem_settings.GEM_DIRTY_UPDATE_ENABLED:
            with transaction.atomic():
                return func(*args, **kwargs)
        return func(*args, **kwargs)

    return inner_func
