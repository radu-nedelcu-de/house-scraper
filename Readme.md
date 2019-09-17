This is a Right Move House Scraper that was built over a few hours in a weekend and we used to look for a property.

It will scrape Right Move every night, save data in Neo4J and then send an e-mail out with the latest viable properties, pictures, price, description, distance to station and a link back to Rightmove.

I wrote the code as I was interested in creating an entire system using [Celery](http://www.celeryproject.org/), [RabbitMQ](https://www.rabbitmq.com/) and [Neo4J](https://neo4j.com). The scraper uses Gmail.

It scrapes London Stations every night and then sends an e-mail based on pre-defined parameters:
- minimum and maximum price and minimum number of bedrooms (rightmovescraper.py)
- help to buy - one of these words are mentioned: help_to_buy_filters = ['new', 'luxury', 'help']

To set up (sorry, did not consider multiple users at the time):
- add the e-mail account to send e-mails from by editing gmail_mail_sender.py.
- modify error@error_email.com in ./celery_worker/scraper_tasks/tasks.py to add the email of the admin
- modify the hostname in bash/server_docker_cmds.sh from hostname.for.rabbitmq to something you want
- modify [get_station_based_initial_search_urls](rightmove_scraper.py) with your property parameters.

To build the images do: ./bash/docker_compose_build.sh
To run it do: ./bash/docker_compose_start
To stop it do: ./bash/docker_compose_stop

If you want to do a quick test edit manually_scrape.py and change your e-mail address.

