from django.db.models import QuerySet


def normalize_data_filter_customer(customers: QuerySet) -> dict:
    """
        This function used to convert data queryset to json
    :param customers:
    :return:
    """
    customers_dict = {}
    for customer in customers:
        customers_dict[customer.id] = {
            "id": customer.id,
            "phone": customer.phone,
            "nick_name": customer.nick_name,
            "age": customer.age,
            "gender": customer.gender,
            "permission_start_treatment": customer.permission_start_treatment,
        }
    return customers_dict