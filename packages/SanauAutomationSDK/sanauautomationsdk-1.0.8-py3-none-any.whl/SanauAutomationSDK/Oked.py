from .Base import Base
from . import config as cfg
from .utils.decorators import catch
import requests


class Oked(Base):

    def __init__(self, region, domain, access_key):
        super().__init__(region, domain, access_key)

    @catch()
    def get_all_okeds(self, headers=None):
        return requests.get(url=cfg.OKEDS.format(domain=self.domain), headers=headers).json()
