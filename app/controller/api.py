from aplus_client.client import AplusTokenClient
from ..config import Config

api = AplusTokenClient('ce8f8944888582d532f5344ae63318e92f48b41f')
api.set_base_url_from('http://172.20.0.3:8000/api/v2/')
