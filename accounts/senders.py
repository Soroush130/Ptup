import requests
from Ptup.settings import KAVENEGAR_API_KEY


class SmsSender:
    def __init__(self):
        pass

    @classmethod
    def send_sms(cls, code: str, phone: str):
        api_key = KAVENEGAR_API_KEY
        template = "Ptup"
        request = requests.get(
            f'https://api.kavenegar.com/v1/{api_key}/verify/lookup.json?receptor={phone}&token={code}&template={template}')

        return request.status_code
