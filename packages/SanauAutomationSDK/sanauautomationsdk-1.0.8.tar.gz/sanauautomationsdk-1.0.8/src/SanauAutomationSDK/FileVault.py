from .Base import Base
from . import config as cfg
from .utils.decorators import catch
import requests


class FileVault(Base):

    def __init__(self, region, domain, access_key):
        super().__init__(region, domain, access_key)

    @catch()
    def get_file(self, params, headers=None):
        return requests.get(url=cfg.FILE_VAULT_DOWNLOAD_FILE.format(domain=self.domain), params=params, headers=headers)
