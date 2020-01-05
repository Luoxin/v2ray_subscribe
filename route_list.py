from api.gateway import gateway
from api.registered import registered
from api.test_interface import test_interface_api
from api.time_info import time_info

ROUTE_LIST = [
    test_interface_api,
    gateway,
    registered,
    time_info,
]
