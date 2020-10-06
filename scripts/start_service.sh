#!/bin/bash

cat<<EOT | pipenv run python librettobot.py
${TELEGRAM_BOT_TOKEN}
/data/botdatabase.db
0.0.0.0
5555
EOT

