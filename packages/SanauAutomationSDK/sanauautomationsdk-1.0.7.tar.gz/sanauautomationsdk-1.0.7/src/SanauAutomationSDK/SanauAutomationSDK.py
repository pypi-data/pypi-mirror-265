from .Base import Base
from .Api import Api
from .Client import Client
from .FileVault import FileVault
from .OGD import OGD
from .Oked import Oked


class SanauAutomationSDK(Base):

    def __init__(self, region, domain, access_key):
        super().__init__(region, domain, access_key)
        self.api = Api(region, domain, access_key)
        self.client = Client(region, domain, access_key)
        self.file_vault = FileVault(region, domain, access_key)
        self.ogd = OGD(region, domain, access_key)
        self.oked = Oked(region, domain, access_key)
