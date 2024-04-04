from django_gem.entities.context import gem_cutting_context


class OverrideAnvil:
    def __init__(self, anvil):
        self.anvil = anvil
        self.original_anvil = gem_cutting_context.anvil

    def __enter__(self):
        gem_cutting_context.set_anvil(self.anvil)

    def __exit__(self, exc_type, exc_value, exc_traceback):
        gem_cutting_context.set_anvil(self.original_anvil)
