#!/bin/bash

docker-compose up -d --build
docker-compose run back python manage.py migrate
docker-compose up