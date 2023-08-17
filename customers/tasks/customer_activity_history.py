from datetime import datetime

from django.db.models import QuerySet
from django.db.models import Count
from django.db.models.functions import TruncDate

from customers.models import CustomerActivityHistory


def create_activity_history(customer_id, subject, content) -> QuerySet:
    new_activity = CustomerActivityHistory.objects.create(
        customer_id=customer_id,
        subject=subject,
        content=content
    )

    return new_activity


def get_activity_list(customer: QuerySet) -> dict:
    timeline = {}

    grouped_data = CustomerActivityHistory.objects.filter(
        customer=customer
    ).annotate(
        created_date=TruncDate('created')  # Truncate datetime to date
    ).values('created_date').annotate(
        activity_count=Count('id')
    ).order_by('created_date')

    for date in grouped_data:
        year, month, day = date['created_date'].year, date['created_date'].month, date['created_date'].day
        activities = get_activity(year, month, day, customer)

        timeline[date['created_date'].strftime('%Y-%m-%d')] = list(activities)

    return timeline


def get_activity(year, month, day, customer: QuerySet):
    return CustomerActivityHistory.objects.filter(
        customer=customer,
        created__year=year,
        created__month=month,
        created__day=day
    ).order_by('-created')
