import importlib
import typing

from django_gem.entities.source import CutSource
from django_gem.logger import logger
from django_gem.toolkit import gem_settings
from django_gem.toolkit.anvils.base import BaseAnvil
from django_gem.toolkit.chest import Chest


class Smith:
    """Handles data collection and initiates cut process"""

    chest = Chest()
    anvil: typing.Optional[typing.Type[BaseAnvil]] = None

    def add_item(self, natural_key: str, object_ids: list, gem_fields: list):
        self.chest.add_chest_item(natural_key, object_ids, gem_fields)

    def add_source(self, natural_key: str, source: CutSource):
        self.chest.add_cut_source(natural_key, source)

    def load(self):
        if anvil_import := gem_settings.GEM_ANVIL:
            try:
                anvil_module, anvil_class = anvil_import.rsplit(".", 1)
            except ValueError:
                logger.error("Error importing %s: Anvil import misconfigured", anvil_import)
                return
            try:
                anvil: typing.Type[BaseAnvil] = getattr(
                    importlib.import_module(anvil_module), anvil_class
                )
            except ImportError as e:
                logger.error("Error importing %s: %s", anvil_import, e)
                return
            if not anvil:
                logger.error("Error configuring %s: %s not found", anvil_import, anvil_class)
                return
            self.anvil = anvil

    def initiate_cutting(self, override_anvil: typing.Optional[BaseAnvil] = None):
        if self.chest.is_empty():
            return

        sealed_chest = self.chest.get_sealed_chest()
        sealed_sources = self.chest.get_sealed_sources()
        (override_anvil or self.anvil).cut(sealed_chest, sealed_sources)
        self.chest.reset()


smith = Smith()
