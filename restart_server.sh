#!/usr/bin/env bash

export HOST_IP=
export HOST_NAME=

git pull

docker stack rm ANSWERLY

sleep 30

docker stack deploy -c docker-compose.yml ANSWERLY
