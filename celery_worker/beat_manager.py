from celery.schedules import crontab

from celery_worker import app


app.conf.beat_schedule = {
    'try': {
        'task': 'celery_worker.scraper_tasks.tasks.main_task',
        'schedule': crontab(hour=0, minute=0),
        'args': (
            1,
            'stations_list.json',
            ['someone@some_mail.com', 'someone_else@some_other_mail.com']
        )
    }
}
