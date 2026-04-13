from injector import Module

from app.core.repositories.api_config_repository import ApiConfigRepository
from app.core.repositories.scrapper_config_repository import ScrapperConfigRepository


class RepositoriesModule(Module):
    def configure(self, binder):
        binder.bind(ApiConfigRepository, to=ApiConfigRepository)
        binder.bind(ScrapperConfigRepository, to=ScrapperConfigRepository)
