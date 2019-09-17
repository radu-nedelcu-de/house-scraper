import os
from celery import Celery

rabbitmq_server = os.environ['RABBITMQ_SERVER']

app = Celery(
    'tasks',
    backend='rpc://',
    broker=f'pyamqp://user:password@{rabbitmq_server}//',
    include=['celery_worker.scraper_tasks.tasks']
)

app.autodiscover_tasks([
    'celery_worker.scraper_tasks'
])

