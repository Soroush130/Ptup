from django.db.models import QuerySet


def read_message(message: QuerySet) -> bool:
    try:
        message.is_read = True
        message.save()
        return True
    except:
        return False
