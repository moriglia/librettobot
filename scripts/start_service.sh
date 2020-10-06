#!/bin/bash

pipenv run python librettobot.py \
  --token ${TELEGRAM_BOT_TOKEN} \
  --dbpath ${DB_PATH} \
  --localhost ${LOCALHOST_IP} \
  --port ${PORT}
