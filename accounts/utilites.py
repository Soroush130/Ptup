import random
import string


def phone_number_encryption(phone_number: str) -> str:
    my_dict = {
        0: "a",
        1: "b",
        2: "c",
        3: "d",
        4: "e",
        5: "f",
        6: "g",
        7: "h",
        8: "i",
        9: "j",
    }
    phone_char_old = [char for char in phone_number]
    phone_char_new = [my_dict[int(char)] for char in phone_char_old]
    return ''.join(phone_char_new)


def phone_number_decryption(phone_number: str) -> str:
    my_dict = {
        "a": 0,
        "b": 1,
        "c": 2,
        "d": 3,
        "e": 4,
        "f": 5,
        "g": 6,
        "h": 7,
        "i": 8,
        "j": 9,
    }
    phone_char_old = [char for char in phone_number]
    phone_char_new = [str(my_dict[char]) for char in phone_char_old]
    return ''.join(phone_char_new)


def generate_otp_code(length: int) -> str:
    return ''.join(random.choice(string.digits) for _ in range(length))
