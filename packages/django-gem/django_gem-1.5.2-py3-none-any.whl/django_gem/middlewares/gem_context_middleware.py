from django_gem.entities.context import gem_cutting_context

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object


class GemContextMiddleware(MiddlewareMixin):
    def process_request(self, request):
        gem_cutting_context.reset()

    def process_response(self, request, response):
        """
        Delete the current request to avoid leaking memory.
        """
        gem_cutting_context.reset()
        return response
