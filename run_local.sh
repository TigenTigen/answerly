#!/usr/bin/env bash

export HOST_IP='127.0.0.1'
export HOST_NAME='localhost'

docker-compose build && docker-compose up
