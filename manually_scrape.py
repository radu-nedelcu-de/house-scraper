from celery_worker.scraper_tasks.tasks import main_task

if __name__ == '__main__':
    main_task.delay(
        1,
        'test_stations_list.json',
        ['someone@some_mail.com', 'someone_else@some_other_mail.com']
    )
