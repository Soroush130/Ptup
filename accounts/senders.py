from kavenegar import *


class SmsSender:
    def __init__(self):
        pass

    @classmethod
    def send(cls, code: str, phone: str):
        api = KavenegarAPI(
            '326D6C724876336A574F71325468506955775749707731665A61316630554E53347471334A675069424C633D'
        )
        message = f"Otp-Code: {code}"
        params = {
            'sender': '10008663',
            'receptor': phone,
            'message': message
        }
        response = api.sms_send(params)
        return response