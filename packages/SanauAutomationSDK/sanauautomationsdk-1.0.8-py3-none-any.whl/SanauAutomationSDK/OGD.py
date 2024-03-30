from .Base import Base
from . import config as cfg
from .utils.decorators import catch
import requests


class OGD(Base):

    def __init__(self, region, domain, access_key):
        super().__init__(region, domain, access_key)

    @catch()
    def get_ogd_excel(self, headers=None):
        return requests.get(url=cfg.OGD_EXCEL)
