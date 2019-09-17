#!/usr/bin/env bash

docker build \
    -t rightmove_scraper_celery_worker \
    -f docker_images/celery_worker .
docker run \
    -d \
    -it \
    --restart always \
    --name scraper_celery_worker \
    rightmove_scraper_celery_worker

docker build \
    -t rightmove_scraper_celery_beat \
    -f docker_images/celery_beat .
docker run \
    -d \
    -it \
    --restart always \
    --name scraper_celery_beat \
    rightmove_scraper_celery_beat

