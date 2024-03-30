from .Base import Base
from . import config as cfg
from .utils.decorators import catch
import requests
import json


class Client(Base):

    def __init__(self, region, domain, access_key):
        super().__init__(region, domain, access_key)

    @catch()
    def get_databases(self, headers=None):
        return requests.get(url=cfg.ONE_S_DATABASES.format(domain=self.domain), headers=headers).json()

    @catch()
    def get_db_employees(self, db_name, headers=None):
        return requests.get(url=cfg.ARM_EMPLOYEES.format(domain=self.domain, db_name=db_name), headers=headers).json()

    @catch()
    def post_taxation_organ(self, out_dict, headers=None):
        return requests.post(url=cfg.FETCH_TAXATION_ORGANS.format(domain=self.domain),
                             data=json.dumps({'taxation_organs': out_dict}), headers=headers)

    @catch()
    def get_alert(self, params, headers=None):
        return requests.get(cfg.GET_ALERT.format(domain=self.domain), params=params, headers=headers)

    @catch()
    def post_alerts(self, params, headers=None):
        return requests.post(url=cfg.POST_ALERTS.format(domain=self.domain), params=params, headers=headers)

    @catch()
    def resolve_alert(self, params, headers=None):
        return requests.put(url=cfg.RESOLVE_ALERT.format(domain=self.domain), params=params, headers=headers)

    @catch()
    def resolve_all_alerts(self, entity_id, keys, headers=None):
        return requests.delete(url=cfg.RESOLVE_ALL_ALERTS.format(domain=self.domain),
                               json={'entity_id': entity_id, 'keys': keys}, headers=headers)
