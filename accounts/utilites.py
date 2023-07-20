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