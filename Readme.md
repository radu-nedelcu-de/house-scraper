This is a Right Move House Scraper that was built over a weekend and we used to get a sense for the market.

It will scrape Right Move every night, save data in Neo4J and then send an e-mail out with the latest viable properties.

I wrote the code as I was interested in creating an entire system using [Celery](http://www.celeryproject.org/), [RabbitMQ](https://www.rabbitmq.com/) and [Neo4J](https://neo4j.com). The scraper uses Gmail.

It scrapes London Stations every night and then sends an e-mail based on pre-defined parameters:
- help to buy
- price

To set up:
- add the e-mail account to send e-mails from by editing gmail_mail_sender.py.
- modify error@error_email.com in ./celery_worker/scraper_tasks/tasks.py to add the email of the admin
- modify the hostname in bash/server_docker_cmds.sh from hostname.for.rabbitmq to somethign you want

To build the images do: ./bash/docker_compose_build.sh
To run it do: ./bash/docker_compose_start
To stop it do: ./bash/docker_compose_stop

If you want to do a quick test edit manually_scrape.py and change your e-mail address.

