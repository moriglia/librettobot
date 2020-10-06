config ?= data/config.txt

run:
		pipenv run python librettobot.py --config $(config)

install:
		pipenv install --three

pylama:
		pylama *.py


.PHONY: pylama
