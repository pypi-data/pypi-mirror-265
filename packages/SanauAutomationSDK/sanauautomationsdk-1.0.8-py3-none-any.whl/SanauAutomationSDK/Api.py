from .Base import Base
from . import config as cfg
from .utils.decorators import catch
import requests
import urllib.request


class Api(Base):

    def __init__(self, region, domain, access_key):
        super().__init__(region, domain, access_key)

    @catch()
    def get_currency_rates(self, currency_date, headers=None):
        return urllib.request.urlopen(url=cfg.NATIONAL_BANK.format(currency_date=currency_date))

    @catch()
    def get_domains(self, headers=None):
        return requests.get(url=cfg.DOMAINS, headers=headers).json()['domains']
