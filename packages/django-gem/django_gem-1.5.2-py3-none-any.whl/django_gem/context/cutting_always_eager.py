from django_gem.entities.context import gem_cutting_context


class CuttingAlwaysEager:
    def __init__(self):
        self.override_return_eager_value = True
        self.original_return_eager_value = gem_cutting_context.return_eager_value

    def __enter__(self):
        gem_cutting_context.set_return_eager_value(
            return_eager_value=self.override_return_eager_value
        )

    def __exit__(self, exc_type, exc_value, exc_traceback):
        gem_cutting_context.set_return_eager_value(
            return_eager_value=self.original_return_eager_value
        )
