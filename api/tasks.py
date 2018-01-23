from celery import shared_task

from api.models import Order


@shared_task
def clean_old_orders():
    deleted, _ = Order.objects.exclude(id__in=Order.accountable_orders()).delete()
    return deleted
