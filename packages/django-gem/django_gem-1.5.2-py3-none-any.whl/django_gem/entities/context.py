import threading

from django_gem.constants import GemCuttingMode

_thread_locals = threading.local()


class GemContext:
    return_eager_value: bool = False
    cutting_mode: str = GemCuttingMode.TRANSACTION
    anvil = None


class CurrentGemContext:
    __default_context = GemContext()

    @property
    def current_context(self):
        return getattr(_thread_locals, "gem_current_context", None)

    @classmethod
    def reset(cls):
        if hasattr(_thread_locals, "gem_current_context"):
            del _thread_locals.gem_current_context

    def set_current_context(self):
        if not self.current_context:
            _thread_locals.gem_current_context = GemContext()

    def set_return_eager_value(self, return_eager_value: bool):
        self.set_current_context()
        self.current_context.return_eager_value = return_eager_value

    def set_cutting_mode(self, cutting_mode: str):
        self.set_current_context()
        self.current_context.cutting_mode = cutting_mode

    def set_anvil(self, anvil):
        self.set_current_context()
        self.current_context.anvil = anvil

    @property
    def return_eager_value(self):
        return (
            self.current_context.return_eager_value
            if self.current_context
            else self.__default_context.return_eager_value
        )

    @property
    def cutting_mode(self):
        return (
            self.current_context.cutting_mode
            if self.current_context
            else self.__default_context.cutting_mode
        )

    @property
    def anvil(self):
        return self.current_context.anvil if self.current_context else self.__default_context.anvil


gem_cutting_context = CurrentGemContext()
