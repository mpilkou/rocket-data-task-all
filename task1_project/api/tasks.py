from django.db.models import F
from api.models import Chain

from celery import shared_task
from celery.utils.log import get_task_logger

import random

logger = get_task_logger(__name__)

@shared_task()
def test_task():
    logger.info('TEST TASK')
    return 'TEST'

@shared_task()
def increase_debt():
    f = F('debt')
    for chain in Chain.objects.all():
        chain.debt = f + random.randrange(5, 500)
        chain.save()
    return 'Debt increased'

@shared_task()
def decrease_debt():
    f = F('debt')
    for chain in Chain.objects.all():
        chain.debt = f - random.randrange(100, 10000)
        chain.save()
    return 'Debt decreased'
