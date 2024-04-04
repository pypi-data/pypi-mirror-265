from importlib import import_module

from django.apps import apps

from django_gem.toolkit.gem_migration.constants import GEM_MIGRATIONS_MODULE_NAME


class Loader:
    disk_migrations_locations = None

    def __init__(self):
        self.load_disk()

    @classmethod
    def migrations_module(cls, app_label):
        app_package_name = apps.get_app_config(app_label).name
        return f"{app_package_name}.{GEM_MIGRATIONS_MODULE_NAME}"

    def load_disk(self):
        self.disk_migrations_locations = {}
        for app_config in apps.get_app_configs():
            module_name = self.migrations_module(app_config.label)
            try:
                module = import_module(module_name)
            except:
                continue
            self.disk_migrations_locations[app_config.label] = module.__path__[0]
