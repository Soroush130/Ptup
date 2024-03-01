from django.db.models import QuerySet


def read_message(message: QuerySet) -> bool:
    try:
        message.is_read = True
        message.save()
        return True
    except:
        return False


def show_errors_SendMessage(erros):
    """
    This function used to for show send messages
    :param erros:
    :return: message_error
    """
    message_error = []
    for field, errors in erros.items():
        error = f"{[error for error in errors][0]}"
        message_error.append(error)

    return "  ||   ".join(message_error)