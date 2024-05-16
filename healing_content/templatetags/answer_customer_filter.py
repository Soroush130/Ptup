from django import template

register = template.Library()


@register.filter()
def get_answer_customer(values, args):
    for v in values:
        if v.customer == args:
            return v.answer
