def interpretation_bai(score: float) -> str:
    if score <= 7:
        return 'اضطراب کم'
    elif 8 <= score <= 15:
        return 'اضطراب خفیف'
    elif 16 <= score <= 25:
        return 'اضطراب متوسط'
    else:
        return 'اضطراب شدید'


def interpretation_bdi(score: float) -> str:
    if score <= 13:
        return 'افسردگی کم'
    elif 14 <= score <= 19:
        return 'افسردگی خفیف'
    elif 20 <= score <= 28:
        return 'افسردگی متوسط'
    else:
        return 'افسردگی شدید'


def interpretation_ders(score: float) -> str:
    pass


def interpretation_qli(score: float) -> str:
    pass
