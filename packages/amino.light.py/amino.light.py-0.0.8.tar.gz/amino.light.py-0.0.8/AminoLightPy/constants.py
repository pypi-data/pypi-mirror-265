from time import time
from json import dumps
from requests import Session
from .lib.util import signature, gen_deviceId
from .lib.util.exceptions import CheckException

# add by August Light

api = "http://service.aminoapps.com:80/api/v1"
device_id = gen_deviceId()

class CustomSession(Session):
    def __init__(self) -> None:
        super().__init__()
        self.headers.update({
            "NDCDEVICEID": device_id,
            "User-Agent": "Apple iPhone13,1 iOS v16.5 Main/3.19.0"
        })

    def request(self, method, url, *args, **kwargs):

        headers = kwargs.setdefault("headers", {})

        if method.lower() == "post":
            if "json" in kwargs:
                data = kwargs.get("json")
                
                data["timestamp"] = int(time() * 1000)
                data  = dumps(data)
                headers["Content-Type"] = "application/json"
                headers["NDC-MSG-SIG"] = signature(data)

            else:
                headers["Content-Type"] = "application/x-www-form-urlencoded"

        response = super().request(method, url, *args, **kwargs)

        if response.status_code != 200:
            CheckException(response.text)

        return response


def socket_required(func):
    def wrapper(self, *args, **kwargs):
        if not self.socket_enabled:
            raise Exception("Sockets are disabled, this method cannot be used.")
        return func(self, *args, **kwargs)
    return wrapper