#!/usr/bin/env bash
docker run \
    -d \
    --hostname hostname.for.rabbitmq \
    --name rabbitmq-server \
    -e RABBITMQ_DEFAULT_USER=user \
    -e RABBITMQ_DEFAULT_PASS=password \
    -p 15671:15671 \
    -p 15672:15672 \
    -p 4369:4369 \
    -p 5671:5671 \
    -p 5672:5672 \
    -p 25672:25672 \
    --restart always \
    rabbitmq:3-management


docker build \
    -t neo4j_apoc \
    -f docker_images/neo4j_apoc .
docker run \
    -d \
    --name neo4j_apoc \
    --publish=7474:7474 \
    --publish=7687:7687 \
    --volume=$HOME/data:/data \
    --env=NEO4J_AUTH=neo4j/password \
    --env=dbms.connectors.default_listen_address=0.0.0.0 \
    --env=NEO4J_CACHE_MEMORY=512M \
    --env=NEO4J_HEAP_MEMORY=512M \
    --restart always \
    neo4j_apoc
