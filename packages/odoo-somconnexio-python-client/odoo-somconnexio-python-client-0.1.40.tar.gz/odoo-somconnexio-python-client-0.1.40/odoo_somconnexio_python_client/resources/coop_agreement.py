from odoo_somconnexio_python_client.client import Client
from ..exceptions import ResourceNotFound


class CoopAgreement:
    _url_path = "/coop-agreement/search"

    def __init__(self, name, code):
        self.name = name
        self.code = code

    @classmethod
    def get(cls, code):
        params = {"code": code}
        response_data = Client().get(
            cls._url_path,
            params=params,
        )
        if not response_data:
            raise ResourceNotFound(resource=cls.__name__, filter=params)
        return CoopAgreement(**response_data)
